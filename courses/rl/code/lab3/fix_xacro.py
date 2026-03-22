#!/usr/bin/env python3
import os

path = os.path.expanduser('~/create3_ws/src/create3_sim/irobot_create_common/irobot_create_description/urdf/create3.urdf.xacro')
with open(path, 'r') as f:
    content = f.read()

target = 'wheel_with_wheeldrop.urdf.xacro" />'
camera_line = '  <xacro:include filename="$(find irobot_create_description)/urdf/camera.urdf.xacro" />'

if 'camera.urdf.xacro' not in content:
    content = content.replace(target, target + '\n' + camera_line)
    with open(path, 'w') as f:
        f.write(content)
    print('Added camera include to create3.urdf.xacro')
else:
    print('Camera include already exists')
