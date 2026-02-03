# CliffWalking Environment

Custom Gymnasium environment for CST8509 Lab 2.

## Installation

```bash
pip install -e .
```

## Usage

```python
import gymnasium
import cliffwalking_env

env = gymnasium.make("cliffwalking_env/CliffWalking-v0", render_mode="human")
observation, info = env.reset()

for _ in range(1000):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    
    if terminated or truncated:
        observation, info = env.reset()

env.close()
```
