import mcio_remote as mcio

mcio.util.logging_init()

ro = mcio.types.RunOptions()
args = mcio.envs.minerl_env.MinerlEnvArgs(ro, render_mode="human")
env = mcio.envs.minerl_env.MinerlEnv(args)

obs, info = env.reset()
act = env.action_space.sample()
print(act)


def n() -> None:
    print(act["inventory"])
    obs, reward, terminated, truncated, info = env.step(act)


breakpoint()
print("HERE")
env.close()
