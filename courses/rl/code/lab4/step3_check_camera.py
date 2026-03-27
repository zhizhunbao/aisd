"""
Step 3: 检查摄像头是否已配置（Lab 3 Step 10）
Usage: python3 step3_check_camera.py
"""
import os

URDF_DIR = "/home/peng/create3_ws/src/create3_sim/irobot_create_common/irobot_create_description/urdf"
CAMERA_FILE = os.path.join(URDF_DIR, "camera.urdf.xacro")
CREATE3_FILE = os.path.join(URDF_DIR, "create3.urdf.xacro")

print("=" * 50)
print("Step 3: Camera Check")
print("=" * 50)

# Check camera.urdf.xacro exists
if os.path.exists(CAMERA_FILE):
    print("✅ camera.urdf.xacro exists")
else:
    print("❌ camera.urdf.xacro NOT FOUND")
    print("   Run Lab 3 Step 10 first:")
    print(f"   Copy camera.urdf.xacro to {URDF_DIR}/")

# Check create3.urdf.xacro includes camera
if os.path.exists(CREATE3_FILE):
    with open(CREATE3_FILE, "r") as f:
        content = f.read()
    if "camera.urdf.xacro" in content:
        print("✅ create3.urdf.xacro includes camera")
    else:
        print("❌ create3.urdf.xacro does NOT include camera")
        print("   Add this line after wheel_with_wheeldrop include:")
        print('   <xacro:include filename="$(find irobot_create_description)/urdf/camera.urdf.xacro" />')
else:
    print("❌ create3.urdf.xacro NOT FOUND")

print()
print("If both ✅, camera is ready. Proceed to step4.")
print("If any ❌, fix the issue first (see Lab 3 installation guide Step 10).")
