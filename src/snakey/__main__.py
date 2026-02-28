import argparse
import json
import sys
from typing import Any

import pygame

from snakey import utils


def init_game(config_data: dict[str, Any]) -> tuple[list[utils.Snake], list[utils.Cherry]]:
    """
    Initializes the game with the provided configuration.

    :param config_data: Dictionary containing game configuration (window size, number of
                        snakes, keyboard keys, etc.)
    :return: Tuple of initialized snake and cherry lists.
    """
    snake_colors: list[tuple[int, int, int]] = [
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 50),
        (205, 0, 205),
    ]

    snake_lst: list[utils.Snake] = []
    for i in range(config_data["num_snakes"]):
        keys = config_data["keys"][i]
        snake = utils.Snake(
            start_pos=config_data["start_pos"][i],
            move_keys={
                "up": pygame.__getattribute__(keys[0]),
                "right": pygame.__getattribute__(keys[1]),
                "down": pygame.__getattribute__(keys[2]),
                "left": pygame.__getattribute__(keys[3]),
            },
            color=snake_colors[i],
            block_size=config_data["block_size"],
            num_of_start_blocks=config_data["initial_snake_length"],
        )
        snake_lst.append(snake)

    cherry_lst: list[utils.Cherry] = []
    for _ in range(config_data["num_cherries"]):
        cherry = utils.Cherry(config_data["block_size"])
        cherry.set_new_random_position(snake_lst, config_data["main_window_size"])
        cherry_lst.append(cherry)

    return snake_lst, cherry_lst


def redraw_screen(
    snake_lst: list[utils.Snake],
    cherry_lst: list[utils.Cherry],
    block_size: int,
    screen: pygame.Surface,
) -> None:
    """Redraws the screen with updated snake and cherry positions."""
    screen.fill((0, 0, 0))

    for snake in snake_lst:
        for block_pos in snake.block_pos_lst:
            pygame.draw.rect(screen, snake.color, (block_pos[0], block_pos[1], block_size, block_size))

    for cherry in cherry_lst:
        if cherry.position is not None:
            pygame.draw.rect(screen, (255, 0, 0), (cherry.position[0], cherry.position[1], block_size, block_size))

    pygame.display.update()


def main_loop(
    snake_list: list[utils.Snake],
    cherry_list: list[utils.Cherry],
    screen: pygame.Surface,
    configuration_data: dict[str, Any],
) -> int:
    """
    Main game loop. Returns when a snake collision occurs.

    :return: A status flag from SnakeGameStatusFlags.
    """
    size: tuple[int, int] = configuration_data["main_window_size"]
    block_size: int = configuration_data["block_size"]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for snake in snake_list:
                    if event.key in snake.move_keys.values():
                        snake.key_stack.append(event.key)
            elif event.type == pygame.USEREVENT:
                for snake in snake_list:
                    snake.get_dir_from_keystack()
                    snake.set_new_state(size, snake_list)

                    if snake.collision:
                        return utils.SnakeGameStatusFlags.COLLISION_OCCURENCE

                    for cherry in cherry_list:
                        if snake.block_pos_lst[0] == cherry.position:
                            snake.block_pos_lst.append(snake.block_pos_lst[-1])
                            cherry.set_new_random_position(snake_list, size)

                redraw_screen(snake_list, cherry_list, block_size, screen)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="snakey",
        description="A simple snake game written in Python.",
    )
    parser.add_argument("-c", "--config", required=False, help="Path to a custom game configuration file.")

    args = parser.parse_args()

    config_path = args.config if args.config is not None else utils.get_default_config_path()

    with open(config_path, encoding="utf-8") as config_file:
        configuration_data = json.load(config_file)

    pygame.init()

    screen = pygame.display.set_mode(configuration_data["main_window_size"])
    pygame.display.set_caption("Snakey")
    pygame.time.set_timer(pygame.USEREVENT, configuration_data["refresh_rate"])

    while True:
        snake_lst, cherry_lst = init_game(configuration_data)
        main_loop(snake_lst, cherry_lst, screen, configuration_data)


if __name__ == "__main__":
    main()
