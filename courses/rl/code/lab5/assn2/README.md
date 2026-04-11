# Assignment 2: Create3 RedBall Tracking

Author: Peng Wang (041107730)

## Overview

A Gymnasium environment (`aisd_examples/CreateRedBall-v0`) that integrates with a ROS 2 Node to train a Create 3 robot to rotate and keep a moving red ball centered in its camera view.

## Directory Structure

```
Assn2/
  null.py                 - Null agent (random actions)
  non-rl.py               - Non-RL agent (direct computation)
  qlearning.py            - Q-Learning agent
  dqn.py                  - DQN agent (Stable-Baselines3)
  ppo.py                  - PPO agent (Stable-Baselines3)
  screenshots/            - Training plots and graphs
  041107730_aisd_examples/
    pyproject.toml
    aisd_examples/
      __init__.py
      envs/
        __init__.py
        create3_red_ball.py   - Gymnasium environment + ROS 2 Node
```

## Setup

```bash
# Install the environment package
cd 041107730_aisd_examples
pip install -e .
cd ..
```

## Running

**Prerequisites**: Gazebo simulation with the red ball in the AWS small house must be running, and the Create 3 must be undocked.

```bash
# 1. Test with null agent
python null.py

# 2. Q-Learning training
python qlearning.py

# 3. DQN training
python dqn.py

# 4. PPO training
python ppo.py

# 5. Non-RL comparison
python non-rl.py
```

## Environment Details

- **Observation**: `Discrete(641)` — x-pixel of red ball center (0-640)
- **Action**: `Discrete(641)` — maps to angular Twist: `(A-320)/320 * π/2`
- **Episode**: 100 steps (counter-based termination)
- **Reward**: `-(|position - 320| / 320)` → range [-1, 0], 0 = perfectly centered
