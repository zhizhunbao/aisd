#!/bin/bash
# Fix AWS Small House: replace catkin with ament_cmake
PKG_DIR=~/create3_ws/src/aws-robomaker-small-house-world

cat > "$PKG_DIR/package.xml" << 'EOF'
<?xml version="1.0"?>
<package format="3">
  <name>aws_robomaker_small_house_world</name>
  <version>1.0.0</version>
  <description>AWS RoboMaker small house world for Gazebo (ament port)</description>
  <license>Apache-2.0</license>
  <maintainer email="ros-contributions@amazon.com">AWS RoboMaker</maintainer>
  <buildtool_depend>ament_cmake</buildtool_depend>
  <exec_depend>gazebo_ros</exec_depend>
  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
EOF
echo "✅ package.xml replaced with ament_cmake"

# Build AWS package
echo "Building aws_robomaker_small_house_world..."
source /opt/ros/humble/setup.bash
cd ~/create3_ws
colcon build --symlink-install --packages-select aws_robomaker_small_house_world

echo "🎉 Done! Now launching simulation..."
source ~/create3_ws/install/setup.bash
source /usr/share/gazebo-11/setup.sh
export IGNITION_VERSION=fortress
ros2 launch irobot_create_gazebo_bringup create3_gazebo_aws_small.launch.py
