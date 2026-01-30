from gymnasium.envs.registration import register

register(
    id="cliffwalking_env/GridWorld-v0",
    entry_point="cliffwalking_env.envs:CliffWalkingEnv",
)

register(
    id="cliffwalking_env/CliffWalking-v0",
    entry_point="cliffwalking_env.envs:CliffWalkingEnv",
)
