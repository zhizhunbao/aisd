# ============================================================
# Dockerfile — CST8509 Lab 5: Docker Containerization
# Author: Peng Wang (041107730)
#
# Multi-stage Dockerfile for ROS 2 Humble + Gazebo Classic
# with Create3 simulator, camera URDF, red ball actor,
# and Assignment 2 Gymnasium RL environment.
# ============================================================

# ==========================
# ARG: ROS distribution
# ==========================
ARG ROS_DISTRO=humble

# ============================================================
# Stage 1: CLONE — pull repos & copy source into build context
# ============================================================
FROM osrf/ros:${ROS_DISTRO}-desktop AS clone

ENV DEBIAN_FRONTEND=noninteractive

# --------------------------------------------------------
# System tools needed for cloning & patching
# --------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        python3-pip \
        python3-vcstool \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------
# Create ROS 2 workspace
# --------------------------------------------------------
RUN mkdir -p /ros2_ws/src

# --------------------------------------------------------
# Clone create3_sim (humble branch)
# --------------------------------------------------------
RUN cd /ros2_ws/src && \
    git clone --depth 1 --branch humble \
        https://github.com/iRobotEducation/create3_sim.git

# --------------------------------------------------------
# Clone AWS Small House world (ros2 branch)
# --------------------------------------------------------
RUN cd /ros2_ws/src && \
    git clone --depth 1 --branch ros2 \
        https://github.com/aws-robotics/aws-robomaker-small-house-world.git

# --------------------------------------------------------
# Copy local Assignment 2 ROS 2 workspace
# (Gymnasium environment package + agents)
# --------------------------------------------------------
COPY assn2/ /ros2_ws/assn2/

# --------------------------------------------------------
# Apply PATCH 1: Add camera to Create3 URDF
# Copy the camera URDF xacro into create3_sim
# --------------------------------------------------------
COPY patches/camera.urdf.xacro \
     /ros2_ws/src/create3_sim/irobot_create_common/irobot_create_description/urdf/camera.urdf.xacro

# Inject camera xacro include into create3.urdf.xacro
# (add <xacro:include> right before the closing </robot> tag)
RUN sed -i '/<\/robot>/i \  <xacro:include filename="$(find irobot_create_description)/urdf/camera.urdf.xacro" />' \
    /ros2_ws/src/create3_sim/irobot_create_common/irobot_create_description/urdf/create3.urdf.xacro

# --------------------------------------------------------
# Apply PATCH 2: Add red ball actor to AWS small house world
# --------------------------------------------------------
COPY patches/red_ball_actor.xml /tmp/red_ball_actor.xml
RUN sed -i '/<\/world>/r /tmp/red_ball_actor.xml' \
    /ros2_ws/src/aws-robomaker-small-house-world/worlds/small_house.world && \
    rm /tmp/red_ball_actor.xml


# ============================================================
# Stage 2: BUILD — install deps, build workspace, set up venv
# ============================================================
FROM osrf/ros:${ROS_DISTRO}-desktop AS build

ENV DEBIAN_FRONTEND=noninteractive
ENV IGNITION_VERSION=fortress

# --------------------------------------------------------
# System dependencies: Gazebo Classic + Mesa/OpenGL + dev
# --------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
        gazebo \
        ros-humble-gazebo-ros-pkgs \
        ros-humble-gazebo-ros2-control \
        ros-humble-irobot-create-msgs \
        ros-humble-irobot-create-gazebo-sim \
        python3-colcon-common-extensions \
        python3-rosdep \
        python3-vcstool \
        python3-pip \
        python3-venv \
        python3-opencv \
        ros-humble-cv-bridge \
        ros-humble-xacro \
        libgl1-mesa-glx \
        libgl1-mesa-dri \
        mesa-utils \
        x11-apps \
        git \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------
# Copy workspace from clone stage
# --------------------------------------------------------
COPY --from=clone /ros2_ws /ros2_ws

# --------------------------------------------------------
# Install ROS dependencies via rosdep
# --------------------------------------------------------
RUN cd /ros2_ws && \
    . /opt/ros/humble/setup.sh && \
    rosdep update && \
    rosdep install --from-paths src -yi --skip-keys="irobot_create_msgs" || true

# --------------------------------------------------------
# Build all ROS 2 packages with colcon
# --------------------------------------------------------
RUN cd /ros2_ws && \
    . /opt/ros/humble/setup.sh && \
    colcon build --symlink-install

# --------------------------------------------------------
# Create Python virtual environment in /opt/ros_venv
# with ML packages (gymnasium, stable-baselines3, etc.)
# --------------------------------------------------------
RUN python3 -m venv /opt/ros_venv --system-site-packages && \
    /opt/ros_venv/bin/pip install --upgrade pip "setuptools>=61,<80" && \
    /opt/ros_venv/bin/pip install \
        "numpy<2" \
        gymnasium \
        matplotlib \
        stable-baselines3

# --------------------------------------------------------
# Install Gymnasium environment package (aisd_examples)
# --------------------------------------------------------
RUN /opt/ros_venv/bin/pip install -e /ros2_ws/assn2/041107730_aisd_examples


# ============================================================
# Stage 3: RUNTIME — final slim image
# ============================================================
FROM build AS runtime

# --------------------------------------------------------
# Entrypoint script: source everything and drop into bash
# --------------------------------------------------------
RUN echo '#!/bin/bash\n\
set -e\n\
source /opt/ros/humble/setup.bash\n\
source /usr/share/gazebo-11/setup.sh 2>/dev/null || true\n\
source /ros2_ws/install/setup.bash 2>/dev/null || true\n\
source /opt/ros_venv/bin/activate\n\
export IGNITION_VERSION=fortress\n\
exec "$@"\n' > /ros_entrypoint.sh && \
    chmod +x /ros_entrypoint.sh

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
