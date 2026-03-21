#!/bin/bash
# Add camera.urdf.xacro include to create3.urdf.xacro
XACRO_FILE=~/create3_ws/src/create3_sim/irobot_create_common/irobot_create_description/urdf/create3.urdf.xacro

if grep -q "camera.urdf.xacro" "$XACRO_FILE"; then
    echo "ℹ️  camera.urdf.xacro already included"
else
    sed -i '/<\/robot>/i \    <xacro:include filename="$(find irobot_create_description)/urdf/camera.urdf.xacro" />' "$XACRO_FILE"
    echo "✅ camera include added to create3.urdf.xacro"
fi

# Rebuild
echo "Rebuilding irobot_create_description..."
source /opt/ros/humble/setup.bash
cd ~/create3_ws
colcon build --symlink-install --packages-select irobot_create_description

# Configure bashrc
LINES=(
    "source /opt/ros/humble/setup.bash"
    "source ~/create3_ws/install/setup.bash"
    "source /usr/share/gazebo-11/setup.sh"
    "export IGNITION_VERSION=fortress"
)
for line in "${LINES[@]}"; do
    grep -Fq "$line" ~/.bashrc 2>/dev/null || echo "$line" >> ~/.bashrc
done
echo "✅ bashrc configured"
echo "🎉 Done! Close and reopen WSL terminal."
