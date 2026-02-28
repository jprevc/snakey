import pathlib
import random


def get_default_config_path() -> pathlib.Path:
    return pathlib.Path(__file__).parent / "res" / "config.json"


class Snake:
    """
    Snake class. Defines one snake for one player.

    :param start_pos: Starting position for the snake. This is position of the head block
                      in pixels, as tuple of x and y position.
    :param move_keys: Dictionary that binds directions to keyboard keys. Dictionary should
                      have four keys: 'up', 'right', 'down', and 'left'. Corresponding values
                      should be pygame keyboard codes.
    :param color: Color of the snake as rgb code in tuple.
    :param block_size: Size of one block of the snake in pixels.
    :param num_of_start_blocks: Number of starting blocks for the snake.
    """

    def __init__(
        self,
        start_pos: tuple[int, int],
        move_keys: dict[str, int],
        color: tuple[int, int, int],
        block_size: int,
        num_of_start_blocks: int,
    ) -> None:
        self.block_size = block_size
        self.start_pos = start_pos
        self.move_keys = move_keys
        self.color = color
        self.num_of_start_blocks = num_of_start_blocks
        self.curr_dir = [1, 0]
        self.key_stack: list[int] = []
        self.collision = False

        self.block_pos_lst: list[tuple[int, int]] = []
        for i in range(num_of_start_blocks):
            self.block_pos_lst.append((self.start_pos[0] - i * self.block_size, self.start_pos[1]))

    def get_dir_from_keystack(self) -> None:
        """Updates snake's direction by checking which key was pressed."""
        if self.key_stack:
            key_pressed = self.key_stack[0]
            if key_pressed == self.move_keys["up"]:
                new_dir = [0, -1]
            elif key_pressed == self.move_keys["right"]:
                new_dir = [1, 0]
            elif key_pressed == self.move_keys["down"]:
                new_dir = [0, 1]
            elif key_pressed == self.move_keys["left"]:
                new_dir = [-1, 0]
            else:
                new_dir = self.curr_dir

            # prevent reversing direction
            if new_dir == [-self.curr_dir[0], -self.curr_dir[1]]:
                new_dir = self.curr_dir

            self.curr_dir = new_dir
            self.key_stack.pop(0)

    def set_new_state(self, game_dims: tuple[int, int], snakes_lst: list["Snake"]) -> None:
        """
        Sets new snake position and checks for collision with game frame or other snakes.

        :param game_dims: Game frame dimensions as tuple of width and height.
        :param snakes_lst: List containing all snakes in the game.
        """
        new_block: list[tuple[int, int]] = [
            (
                self.block_pos_lst[0][0] + self.curr_dir[0] * self.block_size,
                self.block_pos_lst[0][1] + self.curr_dir[1] * self.block_size,
            )
        ]
        self.block_pos_lst = new_block + self.block_pos_lst
        self.block_pos_lst.pop()

        other_snakes = [snake for snake in snakes_lst if snake is not self]
        self.collision = self.is_frame_collision(game_dims) or self.is_snake_collision(other_snakes)

    def is_snake_collision(self, other_snakes: list["Snake"]) -> bool:
        """
        Returns True if snake is in collision with itself or other snakes.

        :param other_snakes: List of other snakes in the game.
        """
        if self.block_pos_lst[0] in self.block_pos_lst[1:]:
            return True

        return any(self.block_pos_lst[0] in snake.block_pos_lst for snake in other_snakes)

    def is_frame_collision(self, game_dims: tuple[int, int]) -> bool:
        """
        Returns True if the snake's head is outside the game frame.

        :param game_dims: Game frame dimensions as tuple of width and height.
        """
        head_x, head_y = self.block_pos_lst[0]
        return not (0 <= head_x < game_dims[0] and 0 <= head_y < game_dims[1])


class Cherry:
    """
    Cherry class, defines one cherry in the game.

    :param block_size: Dimension of the block which represents a cherry.
    """

    def __init__(self, block_size: int) -> None:
        self.block_size = block_size
        self.position: tuple[int, int] | None = None

    def _is_cherry_position_valid(self, snake_lst: list[Snake]) -> bool:
        """Returns True if cherry is not placed on any snake."""
        return not any(self.position in snake.block_pos_lst for snake in snake_lst)

    def set_new_random_position(self, snake_lst: list[Snake], game_dims: tuple[int, int]) -> None:
        """
        Sets a new random position for the cherry, ensuring it does not overlap a snake.

        :param snake_lst: List of snakes in the game.
        :param game_dims: Game frame dimensions as tuple of width and height.
        """
        self.position = (
            random.randrange(0, game_dims[0], self.block_size),
            random.randrange(0, game_dims[1], self.block_size),
        )

        if not self._is_cherry_position_valid(snake_lst):
            self.set_new_random_position(snake_lst, game_dims)


class SnakeGameStatusFlags:
    COLLISION_OCCURENCE = 1
