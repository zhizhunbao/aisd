"""
Step 2: 注释掉人类 actor，添加红球 actor
Usage: python3 step2_add_red_ball.py
"""
WORLD_FILE = "/home/peng/create3_ws/src/aws-robomaker-small-house-world/worlds/small_house.world"

RED_BALL_ACTOR = """
    <!-- Lab 4 Step 2: Travelling red ball actor -->
    <actor name="red_ball_actor">
      <link name="link">
        <visual name="visual">
          <geometry>
            <sphere>
              <radius>.2</radius>
            </sphere>
          </geometry>
          <material name="red">
            <ambient>1 0 0 1</ambient>
            <diffuse>1 0 0 1</diffuse>
            <specular>0 0 0 0</specular>
            <emissive>0 0 0 1</emissive>
          </material>
        </visual>
      </link>
      <script>
        <loop>true</loop>
        <delay_start>0.000000</delay_start>
        <auto_start>true</auto_start>
        <trajectory id="0" type="line">
          <waypoint>
            <time>0.0</time>
            <pose>-1 0 1 0 0 0</pose>
          </waypoint>
          <waypoint>
            <time>2.0</time>
            <pose>1 0 1 0 0 0</pose>
          </waypoint>
          <waypoint>
            <time>4.0</time>
            <pose>-1 0 1 0 0 0</pose>
          </waypoint>
        </trajectory>
      </script>
    </actor>
"""

import re

with open(WORLD_FILE, "r") as f:
    content = f.read()

# Comment out human actor if present
if "<actor name=\"human_actor\">" in content and "<!--" not in content.split("human_actor")[0][-10:]:
    content = re.sub(
        r'(\s*<!-- Lab 4 Step 1[^>]*-->)?\s*<actor name="human_actor">.*?</actor>',
        '\n    <!-- Lab 4 Step 1: Human actor commented out after verification -->\n    <!-- <actor name="human_actor">...</actor> -->',
        content,
        flags=re.DOTALL
    )
    print("✅ Human actor commented out")

# Add red ball actor
if "red_ball_actor" in content:
    print("Red ball actor already exists, skipping")
else:
    content = content.replace("  </world>", RED_BALL_ACTOR + "  </world>")
    with open(WORLD_FILE, "w") as f:
        f.write(content)
    print("✅ Red ball actor added")
    print("   Next: rebuild + launch Gazebo, verify red ball bounces back and forth")
