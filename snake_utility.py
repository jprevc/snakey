import pygame
import random

class Snake:

    def __init__(self,
                 start_pos,
                 move_keys,
                 color,
                 block_size,
                 num_of_start_blocks):

        self.block_size = block_size
        self.start_pos = start_pos
        self.move_keys = move_keys
        self.color = color
        self.num_of_start_blocks = num_of_start_blocks
        self.curr_dir = [1, 0]
        self.key_stack = []
        self.collision = False

        # set first start blocks
        self.block_pos_lst = []
        for i in range(num_of_start_blocks):
            self.block_pos_lst.append((self.start_pos[0] - i * self.block_size, self.start_pos[1]))

    def get_dir_from_keystack(self):
        if self.key_stack:
            key_pressed = self.key_stack[0]
            if key_pressed == self.move_keys['up']:
                new_dir = [0, -1]
            elif key_pressed == self.move_keys['right']:
                new_dir = [1, 0]
            elif key_pressed == self.move_keys['down']:
                new_dir = [0, 1]
            elif key_pressed == self.move_keys['left']:
                new_dir = [-1, 0]
            else:
                new_dir = self.curr_dir

            # if snake just reverts direction, don't allow it
            if new_dir == [-self.curr_dir[0], -self.curr_dir[1]]:
                new_dir = self.curr_dir

            self.curr_dir = new_dir

            self.key_stack.pop(0)

    def set_new_state(self, game_dims, snakes_lst):
        # add new block to front of snake according to direction
        new_block = [(self.block_pos_lst[0][0] + self.curr_dir[0]*self.block_size,
                      self.block_pos_lst[0][1] + self.curr_dir[1]*self.block_size)]
        self.block_pos_lst = new_block + self.block_pos_lst

        # remove last block from snake
        self.block_pos_lst.pop()

        # check for collision with screen frame or with other snakes
        # get list of snakes with self removed from it
        othr_snake_lst = [snake for snake in snakes_lst if snake is not self]
        if self.is_frame_collision(game_dims) or self.is_snake_collision(othr_snake_lst):
            self.collision = True
        else:
            self.collision = False

    def is_snake_collision(self, other_snakes):
        """ Returns True if snake is in collision with itself or other snakes. """
        # check for collision with itself
        if self.block_pos_lst[0] in self.block_pos_lst[1:]:
            return True

        # check for collision with other snakes
        for snake in other_snakes:
            if self.block_pos_lst[0] in snake.block_pos_lst:
                return True

        return False

    def is_frame_collision(self, game_dims):
        """ Returns True if snake is in collision with game frame. """
        return not ((0 <= self.block_pos_lst[0][0] < game_dims[0]) and
                    (0 <= self.block_pos_lst[0][1] < game_dims[1]))


class Cherry:

    def __init__(self, block_size):
        self.block_size = block_size
        self.position = None

    def _is_cherry_position_valid(self, snake_lst):
        """ Checks that cherry position is not placed onto some snake. """
        for snake in snake_lst:
            if self.position in snake.block_pos_lst:
                return False

        return True

    def set_new_random_position(self, snake_lst, frame_size):
        """ Sets new random position for cherry. """

        self.position = (random.randrange(0, frame_size[0], self.block_size),
                         random.randrange(0, frame_size[1], self.block_size))

        # recursively call function until new cherry position is valid
        if not self._is_cherry_position_valid(snake_lst):
            self.set_new_random_position(snake_lst, frame_size)

