import gymnasium
import cliffwalking_env

# Configuration constants
ENV_ID = "cliffwalking_env/CliffWalking-v0"
RENDER_MODE = "human"
TEST_STEPS = 1000

env = gymnasium.make(ENV_ID, render_mode=RENDER_MODE)
observation, info = env.reset()

# Perform random actions for TEST_STEPS steps
for _ in range(TEST_STEPS):
    action = env.action_space.sample()  # Get a random action
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()

env.close()
