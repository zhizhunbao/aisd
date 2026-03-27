"""
Step 1: 添加人类 actor 到 small_house.world（验证后注释掉）
Usage: python3 step1_add_human_actor.py
"""
WORLD_FILE = "/home/peng/create3_ws/src/aws-robomaker-small-house-world/worlds/small_house.world"

HUMAN_ACTOR = """
    <!-- Lab 4 Step 1: Human walking actor (comment out after verification) -->
    <actor name="human_actor">
      <skin>
        <filename>walk.dae</filename>
      </skin>
      <animation name="walking">
        <filename>walk.dae</filename>
        <interpolate_x>true</interpolate_x>
      </animation>
      <script>
        <loop>true</loop>
        <delay_start>0.000000</delay_start>
        <auto_start>true</auto_start>
        <trajectory id="0" type="walking">
          <waypoint>
            <time>0</time>
            <pose>0 2 0 0 0 -1.57</pose>
          </waypoint>
          <waypoint>
            <time>2</time>
            <pose>0 -2 0 0 0 -1.57</pose>
          </waypoint>
          <waypoint>
            <time>2.5</time>
            <pose>0 -2 0 0 0 1.57</pose>
          </waypoint>
          <waypoint>
            <time>7</time>
            <pose>0 2 0 0 0 1.57</pose>
          </waypoint>
          <waypoint>
            <time>7.5</time>
            <pose>0 2 0 0 0 -1.57</pose>
          </waypoint>
        </trajectory>
      </script>
    </actor>
"""

with open(WORLD_FILE, "r") as f:
    content = f.read()

if "human_actor" in content:
    print("Human actor already exists, skipping")
else:
    content = content.replace("  </world>", HUMAN_ACTOR + "  </world>")
    with open(WORLD_FILE, "w") as f:
        f.write(content)
    print("✅ Human actor added")
    print("   Next: rebuild + launch Gazebo, verify human walks in house")
    print("   Then: run step2 to comment it out and add red ball")
