"""Use the minerl-compatible env"""

import argparse
import pprint
import time
from collections import defaultdict
from typing import cast

import gymnasium as gym

import mcio_remote as mcio
from mcio_remote.envs import minerl_env


def tutorial(instance_name: str | None, world_name: str | None) -> None:
    if instance_name is not None:
        if world_name is None:
            raise ValueError("World name must be provided if instance name is provided")
        opts = mcio.types.RunOptions.for_launch(instance_name, world_name)
    else:
        opts = mcio.types.RunOptions.for_connect()

    # gym.make() works, but I prefer just creating the env instance directly.
    # env = minerl_env.MinerlEnv(opts, render_mode="human")
    env = gym.make("MCio/MinerlEnv-v0", render_mode="human", run_options=opts)
    env = cast(minerl_env.MinerlEnv, env.unwrapped)

    setup_commands = [
        "time set 0t",  # Just after sunrise
        "teleport @s ~ ~ ~ -90 0",  # face East
        # "summon minecraft:sheep ~2 ~2 ~2",
        # "summon minecraft:cow ~-2 ~2 ~-2",
    ]
    observation, info = env.reset(options={"commands": setup_commands})
    env.skip_ticks(25)
    env.render()
    input("Setup complete")

    # This will return 0 for any unspecified key
    action: minerl_env.MinerlAction = defaultdict(int)
    # action["ESC"] = 0
    action["camera"] = [0, 90]

    for i in range(int(360 / 90)):
        print(action)
        observation, reward, terminated, truncated, info = env.step(action)
        print(i)
        env.render()
        # time.sleep(0.2)
        # input()
    # print_step(action, observation)
    env.skip_ticks(1)
    env.render()

    input("Done")

    env.close()


def print_step(
    action: minerl_env.MinerlAction | None = None,
    observation: minerl_env.MinerlObservation | None = None,
) -> None:
    if action is not None:
        print(f"Action:\n{pprint.pformat(action)}")
    if observation is not None:
        print(f"Obs:\n{obs_to_string(observation)}")
    print("-" * 10)


def obs_to_string(obs: minerl_env.MinerlObservation) -> str:
    """Return a pretty version of the observation as a string.
    Prints the shape of the frame rather than the frame itself"""
    frame = obs["frame"]
    obs["frame"] = frame.shape
    formatted = pprint.pformat(obs)
    obs["frame"] = frame
    return formatted


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Demo of using Minerl-compatible actions and observations.\n"
        "Connect to a running instance (default mode) or launch a specified instance and world.\n"
        "This will only work properly if Minecraft is in SYNC mode.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    mcio.util.logging_add_arg(parser)

    parser.add_argument(
        "--instance-name",
        "-i",
        type=str,
        help="Name of the Minecraft instance to launch",
    )
    parser.add_argument("--world", "-w", type=str, help="World name")

    args = parser.parse_args()
    mcio.util.logging_init(args=args)
    return args


if __name__ == "__main__":
    args = parse_args()

    tutorial(args.instance_name, args.world)
