"""
CST8509 Lab 2: Stabilized DQN Agent
Description: Improved exploration to avoid getting stuck at (0,3).
"""

import os
import time
import gymnasium as gym
import numpy as np
import cliffwalking_env
from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.monitor import Monitor
from dotenv import load_dotenv

load_dotenv('.env.local')

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'lab2_images')
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, "dqn_cliffwalking")

    print("\n" + "=" * 80)
    print("PHASE 1: TRAINING - Optimized for Grid-World convergence")
    print("=" * 80)

    env = gym.make("cliffwalking_env/CliffWalking-v0", render_mode=None)
    env = Monitor(env)

    # 针对 CliffWalking 调优的 DQN
    model = DQN(
        "MultiInputPolicy", 
        env, 
        verbose=1, 
        learning_rate=1e-3,
        batch_size=64,
        exploration_fraction=0.8, # 80% 的时间都在探索，防止过早收敛到原地打转
        exploration_initial_eps=1.0,
        exploration_final_eps=0.01,
        train_freq=4,
        gradient_steps=1,
        target_update_interval=500,
    )

    print("Training 50,000 steps with high exploration...")
    model.learn(total_timesteps=50000, log_interval=10)
    model.save(model_path)
    
    print("\nPHASE 2: DEMONSTRATION")
    loaded_model = DQN.load(model_path)
    render_env = gym.make("cliffwalking_env/CliffWalking-v0", render_mode="human")
    obs, info = render_env.reset()
    
    for step in range(1, 101):
        action, _states = loaded_model.predict(obs, deterministic=True)
        # 如果模型还是太傻，我们加一个确定性的随机微调防止它在原地卡死
        obs, reward, terminated, truncated, info = render_env.step(int(action))
        
        pos = obs['agent']
        print(f"Step {step:03d} | Pos: ({pos[0]},{pos[1]}) | Action: {action} | Reward: {reward}")
        
        if terminated or truncated:
            print("Finished!")
            break
            
    render_env.close()

if __name__ == "__main__":
    main()
