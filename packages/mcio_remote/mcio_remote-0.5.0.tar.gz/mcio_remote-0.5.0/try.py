import mcio_remote as mcio


def run() -> None:
    ro = mcio.types.RunOptions()
    env = mcio.envs.minerl_env.MinerlEnv(ro, render_mode="human")

    cmds = [
        "time set night",
        "teleport @s ~ ~ ~ -180 45",  # Look north and down
        # "summon minecraft:sheep ~2 ~2 ~2",
        # "summon minecraft:cow ~-2 ~2 ~-2",
    ]
    env.reset(options={"commands": cmds})
    env.skip_ticks(25)

    env.close()


mcio.util.logging_init()
run()
