# aisd_examples/envs/create3_red_ball.py
# ============================================================
# Create3 RedBall Gymnasium Environment
# Create3 红球追踪 Gymnasium 环境
#
# 作者: Peng Wang (041107730)
# Author: Peng Wang (041107730)
#
# 该环境将 ROS 2 节点集成到 Gymnasium 环境中，
# 用于训练 Create 3 机器人旋转以保持红球在视野中心。
# This environment integrates a ROS 2 node into a Gymnasium
# environment, training a Create 3 robot to rotate and keep
# a moving red ball centered in its field of view.
# ============================================================

import math
import gymnasium as gym
from gymnasium import spaces

# ============================================================
# ROS 2 相关导入（仅在 ROS 2 环境中可用）
# ROS 2 imports (only available in a ROS 2 environment)
# ============================================================
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2

# 尝试导入 Create 3 停止状态消息
# Try to import Create 3 stop status message
try:
    from irobot_create_msgs.msg import StopStatus
    HAS_STOP_STATUS = True
except ImportError:
    HAS_STOP_STATUS = False


# ============================================================
# RedBallNode: ROS 2 节点，检测红球并发布 Twist 消息
# RedBallNode: ROS 2 Node that detects the red ball and
#              publishes Twist messages
#
# 改编自 Lab 4/5 的 redball.py:
#   - listener_callback: 检测红球并记录其 x 像素位置
#   - step(): 根据动作发布 Twist 消息
#   - stop_callback: 订阅 /stop_status 判断轮子是否停止
# Adapted from Lab 4/5 redball.py:
#   - listener_callback: detects red ball and records its x-pixel
#   - step(): publishes Twist message based on action
#   - stop_callback: subscribes to /stop_status for wheel stop
# ============================================================
class RedBallNode(Node):
    """
    ROS 2 Node that:
    1. Subscribes to the camera image and detects the red ball
       订阅摄像头图像并检测红球
    2. Publishes Twist messages to rotate the Create 3
       发布 Twist 消息来旋转 Create 3
    3. Subscribes to /stop_status to know when wheels have stopped
       订阅 /stop_status 以知道轮子何时停止
    4. Publishes annotated image to /target_redball topic
       将标注后的图像发布到 /target_redball 话题
    """

    def __init__(self):
        super().__init__('redball')

        # --------------------------------------------------------
        # 摄像头图像订阅（与 Lab 4 redball.py 相同）
        # Camera image subscription (same as Lab 4 redball.py)
        # --------------------------------------------------------
        self.subscription = self.create_subscription(
            Image,
            'custom_ns/camera1/image_raw',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        # --------------------------------------------------------
        # OpenCV <-> ROS 图像转换器
        # OpenCV <-> ROS image converter
        # --------------------------------------------------------
        self.br = CvBridge()

        # --------------------------------------------------------
        # 发布器：标注后的图像 + Twist 速度命令
        # Publishers: annotated image + Twist velocity commands
        # --------------------------------------------------------
        self.target_publisher = self.create_publisher(
            Image, 'target_redball', 10
        )
        self.twist_publisher = self.create_publisher(
            Twist, 'cmd_vel', 10
        )

        # --------------------------------------------------------
        # 停止状态订阅（Create 3 专用）
        # Stop status subscription (Create 3 specific)
        # 当轮子停下时 create3_is_stopped 变为 True
        # create3_is_stopped becomes True when wheels stop
        # --------------------------------------------------------
        self.create3_is_stopped = True
        if HAS_STOP_STATUS:
            self.stop_subscription = self.create_subscription(
                StopStatus,
                '/stop_status',
                self.stop_callback,
                10)

        # --------------------------------------------------------
        # 红球在图像中的 x 像素位置（0-640）
        # Red ball x-pixel position in image (0-640)
        # 320 = 图像中心 / 320 = image center
        # -1 表示未检测到 / -1 means not detected
        # --------------------------------------------------------
        self.redball_position = 320  # default to center / 默认在中心

    def listener_callback(self, msg):
        """
        处理摄像头图像：检测红球并记录其 x 坐标。
        Process camera image: detect red ball and record its x coordinate.

        算法步骤（与 Lab 4 redball.py 相同）:
        Algorithm steps (same as Lab 4 redball.py):
        1. BGR -> HSV 颜色空间转换 / BGR -> HSV color space conversion
        2. 红色掩膜 / Red color mask
        3. 高斯模糊 + 形态学操作 / Gaussian blur + morphological ops
        4. 霍夫圆检测 / Hough circle detection
        """
        frame = self.br.imgmsg_to_cv2(msg)

        # HSV 颜色空间转换（红球在 BGR 中变蓝色调）
        # HSV color space conversion (red ball becomes blue hue in BGR)
        hsv_conv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 红色范围（在 HSV 中红色分布在两端，这里取亮红色范围）
        # Red color range (red spans both ends in HSV, using bright red range)
        bright_red_lower_bounds = (110, 100, 100)
        bright_red_upper_bounds = (130, 255, 255)
        bright_red_mask = cv2.inRange(
            hsv_conv_img, bright_red_lower_bounds, bright_red_upper_bounds
        )

        # 高斯模糊去噪 / Gaussian blur for noise reduction
        blurred_mask = cv2.GaussianBlur(bright_red_mask, (9, 9), 3, 3)

        # 形态学操作（闭运算）去除小噪点
        # Morphological operations (closing) to remove small blobs
        erode_element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilate_element = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
        eroded_mask = cv2.erode(blurred_mask, erode_element)
        dilated_mask = cv2.dilate(eroded_mask, dilate_element)

        # 霍夫圆检测 / Hough circle detection
        detected_circles = cv2.HoughCircles(
            dilated_mask, cv2.HOUGH_GRADIENT, 1, 150,
            param1=100, param2=20, minRadius=2, maxRadius=2000
        )

        if detected_circles is not None:
            for circle in detected_circles[0, :]:
                # 在原图上画绿色圆圈标注 / Draw green circle annotation
                circled_orig = cv2.circle(
                    frame,
                    (int(circle[0]), int(circle[1])),
                    int(circle[2]),
                    (0, 255, 0),
                    thickness=3
                )
                # 记录红球中心的 x 像素坐标
                # Record x-pixel coordinate of red ball center
                self.redball_position = int(circle[0])

            # 发布标注后的图像到 /target_redball
            # Publish annotated image to /target_redball
            self.target_publisher.publish(
                self.br.cv2_to_imgmsg(circled_orig)
            )
        else:
            self.get_logger().info('no ball detected')

    def stop_callback(self, msg):
        """
        回调：当 Create 3 发布停止状态时更新标志。
        Callback: update flag when Create 3 publishes stop status.

        StopStatus.is_stopped == True 表示轮子已停止。
        StopStatus.is_stopped == True means wheels have stopped.
        """
        self.create3_is_stopped = msg.is_stopped

    def step(self, action):
        """
        根据动作值发布 Twist 消息。
        Publish a Twist message based on the action value.

        动作映射 / Action mapping:
          action 范围: 0 ~ 640 / action range: 0 ~ 640
          320 = 不旋转 / 320 = no rotation
          0 = 最大左转 (-PI/2) / 0 = max left turn (-PI/2)
          640 = 最大右转 (+PI/2) / 640 = max right turn (+PI/2)

        公式 / Formula: angular_z = (action - 320) / 320 * PI/2
        """
        twist = Twist()
        # 将离散动作转换为角速度
        # Convert discrete action to angular velocity
        twist.angular.z = (action - 320) / 320.0 * (math.pi / 2.0)
        twist.linear.x = 0.0  # 不前进/后退 / no forward/backward movement

        # 发布 Twist 消息让 Create 3 旋转
        # Publish Twist message to rotate Create 3
        self.twist_publisher.publish(twist)

        # 标记轮子为运动中（等待 stop_callback 更新）
        # Mark wheels as moving (wait for stop_callback to update)
        self.create3_is_stopped = False


# ============================================================
# Create3RedBallEnv: Gymnasium 环境类
# Create3RedBallEnv: Gymnasium environment class
#
# 将 RedBallNode 集成为环境的一部分:
#   - __init__: 初始化 rclpy + 创建 RedBallNode
#   - reset: 重置步数计数器，返回当前观测
#   - step: 执行动作 -> spin_once 直到轮子停止 -> 返回观测
#   - close: 销毁节点 + 关闭 rclpy
#
# Integrates RedBallNode as part of the environment:
#   - __init__: initialize rclpy + create RedBallNode
#   - reset: reset step counter, return current observation
#   - step: execute action -> spin_once until stopped -> return obs
#   - close: destroy node + shutdown rclpy
# ============================================================
class Create3RedBallEnv(gym.Env):
    """
    Gymnasium environment for training a Create 3 robot to track
    a moving red ball by rotating left/right.

    用于训练 Create 3 机器人通过左右旋转追踪移动红球的
    Gymnasium 环境。

    Observation:
        Discrete(641) — 红球中心的 x 像素值 (0 到 640)
        Discrete(641) — x-pixel value of red ball center (0 to 640)

    Action:
        Discrete(641) — 映射到 Twist 角速度
        Discrete(641) — maps to Twist angular velocity
        公式 / Formula: angular_z = (action - 320) / 320 * PI/2
    """

    # 不需要 human 渲染（作业要求）
    # No human rendering needed (per assignment requirements)
    metadata = {"render_modes": [None], "render_fps": 4}

    # --------------------------------------------------------
    # 常量 / Constants
    # --------------------------------------------------------
    IMAGE_WIDTH = 640           # 摄像头图像宽度 / Camera image width
    IMAGE_CENTER = 320          # 图像中心 x 坐标 / Image center x coord
    EPISODE_LENGTH = 100        # 回合步数 / Steps per episode

    def __init__(self, render_mode=None):
        """
        初始化 Gymnasium 环境和 ROS 2 节点。
        Initialize Gymnasium environment and ROS 2 node.

        步骤 / Steps:
        1. 初始化 rclpy（ROS 2 Python 客户端库）
           Initialize rclpy (ROS 2 Python Client Library)
        2. 创建 RedBallNode 实例
           Create RedBallNode instance
        3. 定义观测空间和动作空间
           Define observation and action spaces
        """
        super().__init__()

        # --------------------------------------------------------
        # [Step 1] 初始化 ROS 2（对应旧 main() 中的 rclpy.init）
        # [Step 1] Initialize ROS 2 (corresponds to rclpy.init in old main)
        # --------------------------------------------------------
        rclpy.init()

        # --------------------------------------------------------
        # [Step 2] 创建 ROS 2 节点（对应旧 main() 中的 redball = RedBall()）
        # [Step 2] Create ROS 2 node (corresponds to redball = RedBall() in old main)
        # --------------------------------------------------------
        self.redball = RedBallNode()

        # --------------------------------------------------------
        # [Step 3] 观测空间: 离散 0~640（红球 x 像素位置）
        # [Step 3] Observation space: Discrete 0~640 (red ball x-pixel)
        # --------------------------------------------------------
        self.observation_space = spaces.Discrete(self.IMAGE_WIDTH + 1)

        # --------------------------------------------------------
        # [Step 4] 动作空间: 离散 0~640（映射到角速度）
        # [Step 4] Action space: Discrete 0~640 (maps to angular velocity)
        # --------------------------------------------------------
        self.action_space = spaces.Discrete(self.IMAGE_WIDTH + 1)

        # --------------------------------------------------------
        # [Step 5] 步数计数器（回合在 100 步后终止）
        # [Step 5] Step counter (episode terminates after 100 steps)
        # --------------------------------------------------------
        self.step_count = 0

        self.render_mode = render_mode

    def reward(self, redball_position):
        """
        计算奖励：红球越接近图像中心奖励越高。
        Calculate reward: closer the red ball is to image center,
        the higher the reward.

        公式 / Formula:
            reward = -(|position - 320| / 320)
            范围: [-1, 0]，0 = 完美居中
            Range: [-1, 0], 0 = perfectly centered

        设计理由 / Design rationale:
        - 负奖励鼓励 agent 尽快将球居中
          Negative reward encourages agent to center the ball quickly
        - 距离越大惩罚越大
          Larger distance = larger penalty
        """
        distance = abs(redball_position - self.IMAGE_CENTER)
        return -(distance / self.IMAGE_CENTER)

    def reset(self, seed=None, options=None):
        """
        重置环境：将步数计数器归零，返回当前观测。
        Reset environment: set step counter to 0, return current observation.

        根据作业定义，回合是 100 步的固定长度，
        reset 只需要重置计数器并返回最近的观测。
        Per assignment definition, an episode is a fixed 100 steps,
        reset just needs to reset the counter and return latest observation.
        """
        super().reset(seed=seed)

        # 重置步数计数器 / Reset step counter
        self.step_count = 0

        # 调用 spin_once 获取最新的摄像头图像数据
        # Call spin_once to get the latest camera image data
        rclpy.spin_once(self.redball, timeout_sec=1.0)

        observation = self.redball.redball_position
        info = {}
        return observation, info

    def step(self, action):
        """
        执行一步：发送 Twist 命令 → 等待轮子停止 → 返回观测。
        Execute one step: send Twist command → wait for wheels to stop →
        return observation.

        参数 / Parameters:
            action (int): 0~640 的整数，映射到角速度
                          Integer 0~640, maps to angular velocity

        返回 / Returns:
            observation (int): 红球的 x 像素位置 (0~640)
                               Red ball x-pixel position (0~640)
            reward (float): 基于距离的奖励 [-1, 0]
                            Distance-based reward [-1, 0]
            terminated (bool): 步数达到 100 时为 True
                               True when step count reaches 100
            truncated (bool): 始终为 False
                              Always False
            info (dict): 附加信息 / Additional info
        """
        # 递增步数计数器 / Increment step counter
        self.step_count += 1

        # --------------------------------------------------------
        # [Step 1] 通过 ROS 2 节点发布 Twist 消息
        # [Step 1] Publish Twist message via ROS 2 node
        # --------------------------------------------------------
        self.redball.step(action)

        # --------------------------------------------------------
        # [Step 2] 调用 spin_once 处理消息，直到轮子停止
        # [Step 2] Call spin_once to process messages until wheels stop
        #
        # 注意: spin_once 会处理所有待处理的 ROS 回调，包括:
        #   - listener_callback（更新 redball_position）
        #   - stop_callback（更新 create3_is_stopped）
        # Note: spin_once processes all pending ROS callbacks including:
        #   - listener_callback (updates redball_position)
        #   - stop_callback (updates create3_is_stopped)
        # --------------------------------------------------------
        rclpy.spin_once(self.redball, timeout_sec=1.0)
        while not self.redball.create3_is_stopped:
            rclpy.spin_once(self.redball, timeout_sec=0.1)

        # --------------------------------------------------------
        # [Step 3] 获取观测和计算奖励
        # [Step 3] Get observation and calculate reward
        # --------------------------------------------------------
        observation = self.redball.redball_position
        r = self.reward(observation)
        terminated = (self.step_count >= self.EPISODE_LENGTH)
        truncated = False
        info = {"step_count": self.step_count, "redball_x": observation}

        return observation, r, terminated, truncated, info

    def render(self):
        """
        渲染方法：本环境不支持 human 渲染。
        Render method: this environment does not support human rendering.

        可视化通过 RViz 的 /target_redball 话题实现。
        Visualization is done via the /target_redball topic in RViz.
        """
        pass

    def close(self):
        """
        关闭环境：销毁 ROS 2 节点并关闭 rclpy。
        Close environment: destroy ROS 2 node and shutdown rclpy.

        对应旧 main() 中的:
            redball.destroy_node()
            rclpy.shutdown()
        Corresponds to the old main() method:
            redball.destroy_node()
            rclpy.shutdown()
        """
        if self.redball is not None:
            self.redball.destroy_node()
            self.redball = None
        rclpy.shutdown()
