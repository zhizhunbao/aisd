"""
Step 4: 创建 aisd_vision ROS 2 包 + 复制 redball.py
Usage: python3 step4_setup_package.py
"""
import os
import shutil

WS_SRC = "/home/peng/create3_ws/src"
PKG_DIR = os.path.join(WS_SRC, "aisd_vision")
PKG_INNER = os.path.join(PKG_DIR, "aisd_vision")

if os.path.exists(os.path.join(PKG_INNER, "redball.py")):
    print("aisd_vision package already exists, skipping")
    print("   Delete and re-run if you want to recreate:")
    print(f"   rm -rf {PKG_DIR}")
    exit(0)

os.makedirs(PKG_INNER, exist_ok=True)

# __init__.py
with open(os.path.join(PKG_INNER, "__init__.py"), "w") as f:
    f.write("")

# Copy redball.py
src = "/mnt/c/Users/40270/Desktop/workspace/aisd/courses/rl/code/lab4/redball.py"
shutil.copy2(src, os.path.join(PKG_INNER, "redball.py"))

# setup.py
with open(os.path.join(PKG_DIR, "setup.py"), "w") as f:
    f.write("""from setuptools import setup

package_name = 'aisd_vision'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='peng',
    maintainer_email='peng@todo.todo',
    description='AISD Vision package - red ball detection',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'redball = aisd_vision.redball:main',
        ],
    },
)
""")

# setup.cfg
with open(os.path.join(PKG_DIR, "setup.cfg"), "w") as f:
    f.write("""[develop]
script_dir=$base/lib/aisd_vision
[install]
install_scripts=$base/lib/aisd_vision
""")

# package.xml
with open(os.path.join(PKG_DIR, "package.xml"), "w") as f:
    f.write("""<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>aisd_vision</name>
  <version>0.0.1</version>
  <description>AISD Vision package - red ball detection</description>
  <maintainer email="peng@todo.todo">peng</maintainer>
  <license>Apache License 2.0</license>
  <depend>rclpy</depend>
  <depend>sensor_msgs</depend>
  <depend>geometry_msgs</depend>
  <depend>cv_bridge</depend>
  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
""")

# resource marker
res_dir = os.path.join(PKG_DIR, "resource")
os.makedirs(res_dir, exist_ok=True)
with open(os.path.join(res_dir, "aisd_vision"), "w") as f:
    f.write("")

print("✅ aisd_vision package created")
print("   Next: run step5 to build")
