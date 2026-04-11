# Lab 5 Prompt Template — Filled Out

Author: Peng Wang (041107730)

## Prompt Used

```
I need you to generate a complete Dockerfile and docker-compose.yml for my
ROS 2 Humble project.

## PROJECT CONTEXT
I am completing an assignment that uses:
- ROS 2 Humble on Ubuntu 22.04
- Gazebo Classic (Gazebo 11)
- RViz2
- A camera added to the robot URDF (camera.urdf.xacro)
- Create3 simulator modified to include:
  - A moving red ball actor in the AWS small house world
  - A patched AWS small house world (with red_ball_actor XML injected)
- A custom Gymnasium-based RL node (aisd_examples/CreateRedBall-v0)
- A Python virtual environment with common ML dependencies
  (gymnasium, stable-baselines3, matplotlib, numpy<2)
- My own ROS 2 workspace containing:
  - 041107730_aisd_examples (Gymnasium environment package)
  - aisd_examples/envs/create3_red_ball.py (environment + ROS 2 RedBallNode)
  - Agent scripts: null.py, qlearning.py, dqn.py, ppo.py, non-rl.py

## WHAT I NEED FROM YOU

### Dockerfile requirements:
- Uses ROS 2 Humble (FROM osrf/ros:humble-desktop)
- Multi-stage build (clone → build)
- Supports building a full ROS 2 workspace using colcon
- Installs Python 3 venv and ML packages (gymnasium, stable-baselines3, etc.)
- Installs Gazebo Classic and required Mesa/OpenGL libs
- Copies my ROS 2 workspace into /ros2_ws/src
- Applies my patches (URDF camera, world modifications, actors)
- Creates a Python virtual environment in /opt/ros_venv and activates it
- Builds all my packages with colcon build
- Sources /opt/ros/humble/setup.bash, /ros2_ws/install/setup.bash, and the venv
- Supports launching Gazebo + RViz2 from inside the container

### docker-compose.yml requirements:
- Builds the container with ARG ROS_DISTRO=humble
- Uses host networking (required for ROS 2 DDS discovery)
- Exposes GUI applications by mapping: /tmp/.X11-unix:/tmp/.X11-unix
- Passes through environment variables: DISPLAY, RMW_IMPLEMENTATION, IGNITION_VERSION=fortress
- Enables optional GPU acceleration using NVIDIA_VISIBLE_DEVICES=all and NVIDIA_DRIVER_CAPABILITIES=all
- Runs the container in privileged mode for device access
- Provides a command override that launches a bash shell

## EXTRA REQUIREMENTS
- The Dockerfile is multi-stage (clone → build)
- My workspace lives in /ros2_ws
- The final image drops into bash by default
- The Compose file is fully valid YAML (spaces, not tabs)

## PATCH LOCATIONS
- patches/camera.urdf.xacro → Inject into create3_sim URDF (add camera to Create3)
- patches/red_ball_actor.xml → Inject into AWS small_house.world (add red ball actor)

## REPOSITORIES TO CLONE
- https://github.com/iRobotEducation/create3_sim.git (branch: humble)
- https://github.com/aws-robotics/aws-robomaker-small-house-world.git (branch: ros2)

## WHAT TO OUTPUT
Please output:
1. The complete Dockerfile
2. The complete docker-compose.yml
3. Any additional instructions I need to run:
   docker compose build
   docker compose run <service>
   ros2 launch <my package> <my launch file>

Make sure the output is clean, accurate, and ready to use. Be explicit with paths and commands.
```
