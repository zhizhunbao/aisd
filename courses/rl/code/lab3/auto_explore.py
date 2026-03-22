#!/usr/bin/env python3
"""Create3 自动巡航 v2 - 带卡住检测和脱困"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import random
import math
import time


class AutoExplorer(Node):
    def __init__(self):
        super().__init__('auto_explorer')

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)
        self.create_subscription(Odometry, '/odom', self.odom_cb, 10)

        self.min_front = 999.0       # 前方最小距离
        self.min_left = 999.0        # 左侧
        self.min_right = 999.0       # 右侧

        self.pos_x = 0.0
        self.pos_y = 0.0
        self.last_x = 0.0
        self.last_y = 0.0
        self.stuck_count = 0

        self.state = 'explore'       # explore / escape
        self.escape_steps = 0

        self.get_logger().info('Auto Explorer v2 启动！带卡住检测')
        self.timer = self.create_timer(0.3, self.step)
        self.stuck_timer = self.create_timer(3.0, self.check_stuck)

    def scan_cb(self, msg):
        if len(msg.ranges) == 0:
            return
        n = len(msg.ranges)
        sixth = max(n // 6, 1)

        def safe_min(ranges):
            valid = [r for r in ranges if 0.01 < r < 10.0]
            return min(valid) if valid else 999.0

        self.min_front = safe_min(list(msg.ranges[:sixth]) + list(msg.ranges[-sixth:]))
        self.min_left = safe_min(list(msg.ranges[sixth:n//2]))
        self.min_right = safe_min(list(msg.ranges[n//2:-sixth]))

    def odom_cb(self, msg):
        self.pos_x = msg.pose.pose.position.x
        self.pos_y = msg.pose.pose.position.y

    def check_stuck(self):
        """每 3 秒检查是否卡住"""
        dx = self.pos_x - self.last_x
        dy = self.pos_y - self.last_y
        dist = math.sqrt(dx*dx + dy*dy)

        if dist < 0.03:  # 3 秒内移动不到 3cm = 卡住了
            self.stuck_count += 1
            if self.stuck_count >= 2:
                self.state = 'escape'
                self.escape_steps = 10  # 脱困 10 步
                self.get_logger().warn(f'检测到卡住！启动脱困模式')
                self.stuck_count = 0
        else:
            self.stuck_count = 0

        self.last_x = self.pos_x
        self.last_y = self.pos_y

    def step(self):
        twist = Twist()

        if self.state == 'escape':
            # 脱困：大角度后退转弯
            twist.linear.x = -0.15
            twist.angular.z = random.choice([-1.5, 1.5])
            self.escape_steps -= 1
            if self.escape_steps <= 0:
                self.state = 'explore'
                self.get_logger().info('脱困完成，继续探索')

        elif self.min_front < 0.35:
            # 很近，后退 + 大转弯
            twist.linear.x = -0.1
            # 哪边空间大就往哪边转
            if self.min_left > self.min_right:
                twist.angular.z = 1.0
            else:
                twist.angular.z = -1.0

        elif self.min_front < 0.7:
            # 有点近，减速转
            twist.linear.x = 0.05
            if self.min_left > self.min_right:
                twist.angular.z = 0.6
            else:
                twist.angular.z = -0.6

        else:
            # 安全，前进 + 轻微随机转向
            twist.linear.x = 0.2
            twist.angular.z = random.uniform(-0.2, 0.2)

        self.cmd_pub.publish(twist)


def main():
    rclpy.init()
    node = AutoExplorer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        twist = Twist()
        node.cmd_pub.publish(twist)
        node.get_logger().info('已停止')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
