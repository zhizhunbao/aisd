"""
CST8509 Lab 2: Null Agent for Cliff Walking
Author: Peng Wang
Student Number: 041107730

Description:
A simple agent that performs random actions to test the Gymnasium environment setup.
It demonstrates the basic interaction loop: reset -> step -> render.
"""

# 导入操作系统和环境变量加载工具
# Import os and environment variable loading tools
import os
from dotenv import load_dotenv

# 导入 Gymnasium 强化学习框架
# Import Gymnasium Reinforcement Learning framework
import gymnasium as gym

# 导入自定义的悬崖行走环境包
# Import custom cliffwalking environment package
import cliffwalking_env

# 加载个人信息环境变量
# Load personal information environment variables
load_dotenv('.env.local')


def main():
    """主程序：执行随机动作测试环境
    Main program: perform random actions to test the environment"""

    # 打印程序标题和个人信息
    # Print program header and personal information
    print("=" * 80)
    print(f"CST8509 Lab 2: Null Agent Test")
    print(f"Author: {os.getenv('NAME', 'Peng Wang')}")
    print(f"Student Number: {os.getenv('NUMBER', '041107730')}")
    print("=" * 80)

    # 创建悬崖行走环境并开启人类可视化模式
    # Create Cliff Walking environment and enable human visualization mode
    # 原因：render_mode="human" 允许我们通过 GUI 窗口观察代理的行为
    # Reason: render_mode="human" allows us to observe agent behavior via GUI window
    print("Available environments (cliff):", [k for k in gym.envs.registration.registry.keys() if 'cliff' in k])
    env = gym.make("cliffwalking_env/CliffWalking-v0", render_mode="human")

    # 重置环境获取初始观测
    # Reset environment to get initial observation
    observation, info = env.reset()

    # 执行 100 步随机动作测试
    # Perform 100 steps of random action testing
    print("Starting random testing...")
    for step in range(100):
        # 从动作空间中随机采样一个动作
        # Sample a random action from the action space
        action = env.action_space.sample()
        
        # 执行动作，获取下一步状态和奖励等信息
        # Execute action, get next state, reward, and other information
        observation, reward, terminated, truncated, info = env.step(action)
        
        # 打印当前步骤信息
        # Print current step information
        print(f"Step {step + 1}: Action={action}, Reward={reward}")
        
        # 如果到达终端状态或被截断，则重置环境
        # If terminal state or truncated, reset the environment
        if terminated or truncated:
            print("Episode finished, resetting...")
            observation, info = env.reset()

    # 打印测试完成提示并关闭环境
    # Print test completion message and close the environment
    print("\nTest completed successfully.")
    env.close()


# 程序入口点，运行主函数
# Program entry point, run main function
if __name__ == "__main__":
    main()
