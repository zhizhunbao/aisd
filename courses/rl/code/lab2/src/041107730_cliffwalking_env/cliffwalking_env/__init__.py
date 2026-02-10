from gymnasium.envs.registration import register

register(
    id="cliffwalking_env/GridWorld-v0",
    entry_point="cliffwalking_env.envs:GridWorldEnv",
    max_episode_steps=300,
)

register(
    id="cliffwalking_env/CliffWalking-v0",
    entry_point="cliffwalking_env.envs:CliffWalkingEnv",
    max_episode_steps=200,
)
