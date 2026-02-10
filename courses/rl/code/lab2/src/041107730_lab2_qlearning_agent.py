import os
import random

import numpy as np
import matplotlib.pyplot as plt

import gymnasium
import cliffwalking_env

IMAGE_DIR = os.path.join(os.path.dirname(__file__), "lab2_images")
os.makedirs(IMAGE_DIR, exist_ok=True)

# Hyperparameters
EPISODES = 50
MAX_STEPS = 1000
GAMMA = 0.9
EPSILON_INIT = 0.1
DECAY = 0.5
ALPHA = 1.0

env = gymnasium.make("cliffwalking_env/CliffWalking-v0", render_mode="human")

# Calculate state and action space sizes
numstates = (env.observation_space['agent'].high[0] + 1) * (env.observation_space['agent'].high[1] + 1)
numactions = env.action_space.n
xsize = env.observation_space['agent'].high[0] + 1

# Initialize Q-table with random values
q_table = [[random.random() for _ in range(numactions)] for _ in range(numstates)]

returns_history = []
steps_history = []
epsilon = EPSILON_INIT

for episode in range(EPISODES):
    state_dict, _ = env.reset()
    state = state_dict['agent'][1] * xsize + state_dict['agent'][0]

    total_reward = 0
    steps = 0
    done = False

    while not done:
        steps += 1

        # Epsilon-greedy action selection
        if random.random() < epsilon:
            action = random.choice(range(numactions))
        else:
            action = q_table[state].index(max(q_table[state]))

        # Step the environment
        next_state_dict, reward, terminated, truncated, info = env.step(action)
        next_state = next_state_dict['agent'][1] * xsize + next_state_dict['agent'][0]
        total_reward += reward

        # Q-Learning update: Q(s,a) = r + gamma * max Q(s',a')
        best_next = max(q_table[next_state])
        q_table[state][action] = reward + GAMMA * best_next

        state = next_state
        done = terminated or truncated

        if steps > MAX_STEPS:
            break

    epsilon -= DECAY * epsilon
    returns_history.append(total_reward)
    steps_history.append(steps)
    print(f"Episode {episode + 1}/{EPISODES}: {steps} steps, reward: {total_reward:.1f}")

# Plot episode returns
plt.figure()
plt.plot(returns_history)
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.title('Q-Learning Episode Returns')
plt.savefig(os.path.join(IMAGE_DIR, "qlearning_returns.png"))
plt.close()

# Plot steps per episode
plt.figure()
plt.plot(steps_history)
plt.xlabel('Episode')
plt.ylabel('Steps')
plt.title('Q-Learning Steps per Episode')
plt.savefig(os.path.join(IMAGE_DIR, "qlearning_steps.png"))
plt.close()

env.close()
