# Lab 5 AI Response — Dockerfile & docker-compose.yml

Author: Peng Wang (041107730)

## AI Tool Used

ChatGPT (OpenAI)

## Response Summary

The AI generated the following deliverables based on the filled-out prompt template:

### 1. Dockerfile

A multi-stage Dockerfile with three stages:

**Stage 1 — CLONE:**
- Base image: `osrf/ros:humble-desktop`
- Clones `create3_sim` (humble branch) and `aws-robomaker-small-house-world` (ros2 branch)
- Copies local Assignment 2 workspace
- Applies camera URDF patch via `sed` injection into `create3.urdf.xacro`
- Applies red ball actor patch via `sed` injection into `small_house.world`

**Stage 2 — BUILD:**
- Installs system dependencies: Gazebo Classic, Mesa/OpenGL, Python dev tools, cv_bridge
- Runs `rosdep install` and `colcon build --symlink-install`
- Creates Python venv at `/opt/ros_venv` with gymnasium, stable-baselines3, matplotlib, numpy<2
- Installs `aisd_examples` Gymnasium environment package

**Stage 3 — RUNTIME:**
- Creates entrypoint script that sources all setup files and activates the venv
- Default command: `bash`

### 2. docker-compose.yml

- Service: `ros2-create3`
- Build args: `ROS_DISTRO=humble`
- Host networking for ROS 2 DDS
- X11 socket volume mount for GUI
- Environment: DISPLAY, RMW_IMPLEMENTATION, IGNITION_VERSION, NVIDIA vars
- Privileged mode enabled
- Interactive bash shell

### 3. Run Instructions

```bash
# Build the image
docker compose build

# Run the container (enter bash)
docker compose run ros2-create3

# Inside the container — Launch Gazebo simulation
ros2 launch irobot_create_gazebo_bringup create3_gazebo_aws_small.launch.py

# In another terminal — Open a second shell into the running container
docker compose exec ros2-create3 bash

# Navigate to assignment directory and run agents
cd /ros2_ws/assn2
python3 null.py        # Test null agent
python3 qlearning.py   # Q-Learning training
python3 dqn.py         # DQN training
python3 ppo.py         # PPO training
python3 non-rl.py      # Non-RL comparison
```

## Notes

- The `xhost +local:docker` command must be run on the host before starting the container to allow X11 forwarding
- On WSL2 with Docker Desktop, ensure WSL2 integration is enabled in Docker Desktop settings
- The `--system-site-packages` flag in venv creation allows the venv to access system-installed ROS 2 Python packages (rclpy, cv_bridge, etc.)
