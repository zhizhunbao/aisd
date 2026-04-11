#!/usr/bin/env python3
"""Test if all required imports are available in the WSL environment."""
import sys
print(f"Python: {sys.version}")
print(f"Path: {sys.executable}")

errors = []

try:
    import gymnasium
    print(f"  gymnasium: {gymnasium.__version__}")
except ImportError as e:
    errors.append(f"  gymnasium: MISSING ({e})")

try:
    import numpy
    print(f"  numpy: {numpy.__version__}")
except ImportError as e:
    errors.append(f"  numpy: MISSING ({e})")

try:
    import cv2
    print(f"  opencv: {cv2.__version__}")
except ImportError as e:
    errors.append(f"  opencv: MISSING ({e})")

try:
    import rclpy
    print(f"  rclpy: OK")
except ImportError as e:
    errors.append(f"  rclpy: MISSING ({e})")

try:
    from cv_bridge import CvBridge
    print(f"  cv_bridge: OK")
except ImportError as e:
    errors.append(f"  cv_bridge: MISSING ({e})")

try:
    import matplotlib
    print(f"  matplotlib: {matplotlib.__version__}")
except ImportError as e:
    errors.append(f"  matplotlib: MISSING ({e})")

try:
    from stable_baselines3 import DQN, PPO
    import stable_baselines3
    print(f"  stable_baselines3: {stable_baselines3.__version__}")
except ImportError as e:
    errors.append(f"  stable_baselines3: MISSING ({e})")

try:
    from irobot_create_msgs.msg import StopStatus
    print(f"  irobot_create_msgs: OK")
except ImportError as e:
    errors.append(f"  irobot_create_msgs: MISSING ({e})")

if errors:
    print("\n--- MISSING PACKAGES ---")
    for e in errors:
        print(e)
else:
    print("\nAll imports OK!")
