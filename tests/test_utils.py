import pathlib

from snakey import utils


def test_get_default_config_path_returns_path() -> None:
    path = utils.get_default_config_path()
    assert isinstance(path, pathlib.Path)


def test_get_default_config_path_exists() -> None:
    path = utils.get_default_config_path()
    assert path.exists(), f"Default config not found at {path}"


def make_snake(start_pos: tuple[int, int] = (100, 100), block_size: int = 10) -> utils.Snake:
    return utils.Snake(
        start_pos=start_pos,
        move_keys={"up": 0, "right": 1, "down": 2, "left": 3},
        color=(0, 255, 0),
        block_size=block_size,
        num_of_start_blocks=5,
    )


class TestSnake:
    def test_initial_block_count(self) -> None:
        snake = make_snake(block_size=10)
        assert len(snake.block_pos_lst) == 5

    def test_initial_position(self) -> None:
        snake = make_snake(start_pos=(100, 100), block_size=10)
        assert snake.block_pos_lst[0] == (100, 100)

    def test_blocks_extend_leftward_by_default(self) -> None:
        snake = make_snake(start_pos=(100, 100), block_size=10)
        for i, block in enumerate(snake.block_pos_lst):
            assert block == (100 - i * 10, 100)

    def test_no_collision_inside_frame(self) -> None:
        snake = make_snake(start_pos=(100, 100))
        assert not snake.is_frame_collision((640, 480))

    def test_frame_collision_left(self) -> None:
        snake = make_snake(start_pos=(0, 100), block_size=10)
        snake.block_pos_lst[0] = (-10, 100)
        assert snake.is_frame_collision((640, 480))

    def test_frame_collision_right(self) -> None:
        snake = make_snake(start_pos=(100, 100), block_size=10)
        snake.block_pos_lst[0] = (640, 100)
        assert snake.is_frame_collision((640, 480))

    def test_frame_collision_top(self) -> None:
        snake = make_snake(start_pos=(100, 100), block_size=10)
        snake.block_pos_lst[0] = (100, -10)
        assert snake.is_frame_collision((640, 480))

    def test_no_snake_collision_empty(self) -> None:
        snake = make_snake()
        assert not snake.is_snake_collision([])

    def test_self_collision(self) -> None:
        snake = make_snake(start_pos=(50, 100), block_size=10)
        snake.block_pos_lst[0] = snake.block_pos_lst[2]
        assert snake.is_snake_collision([])

    def test_collision_with_other_snake(self) -> None:
        snake1 = make_snake(start_pos=(100, 100))
        snake2 = make_snake(start_pos=(100, 100))
        snake1.block_pos_lst[0] = snake2.block_pos_lst[1]
        assert snake1.is_snake_collision([snake2])

    def test_direction_does_not_reverse(self) -> None:
        snake = make_snake()
        snake.curr_dir = [1, 0]
        snake.key_stack = [3]  # "left" key = opposite of current direction
        snake.get_dir_from_keystack()
        assert snake.curr_dir == [1, 0]

    def test_direction_changes_up(self) -> None:
        snake = make_snake()
        snake.curr_dir = [1, 0]
        snake.key_stack = [0]  # "up"
        snake.get_dir_from_keystack()
        assert snake.curr_dir == [0, -1]

    def test_set_new_state_moves_head(self) -> None:
        snake = make_snake(start_pos=(100, 100), block_size=10)
        original_head = snake.block_pos_lst[0]
        snake.curr_dir = [1, 0]
        snake.set_new_state((640, 480), [])
        new_head = snake.block_pos_lst[0]
        assert new_head == (original_head[0] + 10, original_head[1])

    def test_set_new_state_length_unchanged(self) -> None:
        snake = make_snake()
        original_len = len(snake.block_pos_lst)
        snake.set_new_state((640, 480), [])
        assert len(snake.block_pos_lst) == original_len


class TestCherry:
    def test_initial_position_is_none(self) -> None:
        cherry = utils.Cherry(block_size=10)
        assert cherry.position is None

    def test_set_new_random_position(self) -> None:
        cherry = utils.Cherry(block_size=10)
        cherry.set_new_random_position([], (640, 480))
        assert cherry.position is not None

    def test_position_within_bounds(self) -> None:
        cherry = utils.Cherry(block_size=10)
        for _ in range(50):
            cherry.set_new_random_position([], (640, 480))
            assert cherry.position is not None
            x, y = cherry.position
            assert 0 <= x < 640
            assert 0 <= y < 480

    def test_position_not_on_snake(self) -> None:
        snake = make_snake(start_pos=(100, 100), block_size=10)
        cherry = utils.Cherry(block_size=10)
        for _ in range(20):
            cherry.set_new_random_position([snake], (640, 480))
            assert cherry.position not in snake.block_pos_lst

    def test_position_aligned_to_block_size(self) -> None:
        block_size = 10
        cherry = utils.Cherry(block_size=block_size)
        for _ in range(50):
            cherry.set_new_random_position([], (640, 480))
            assert cherry.position is not None
            x, y = cherry.position
            assert x % block_size == 0
            assert y % block_size == 0
