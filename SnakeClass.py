import pygame


class Snake:

    block_size = 10

    def __init__(self,
                 start_pos,
                 move_keys,
                 color,
                 num_of_start_blocks=3):

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
            self.block_pos_lst.append((self.start_pos[0] - i * Snake.block_size, self.start_pos[1]))

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
        new_block = [(self.block_pos_lst[0][0] + self.curr_dir[0]*Snake.block_size,
                      self.block_pos_lst[0][1] + self.curr_dir[1]*Snake.block_size)]
        self.block_pos_lst = new_block + self.block_pos_lst

        # remove last block from snake
        self.block_pos_lst.pop()

        # check for collision with screen frame
        self.collision = (self.block_pos_lst[0][0] > game_dims[0] or self.block_pos_lst[0][1] > game_dims[1]) or \
                         (self.block_pos_lst[0][0] < 0 or self.block_pos_lst[0][1] < 0)
        if self.collision:
            return

        # check for collision with snakes
        for snake in snakes_lst:
            if snake is self:  # check for collision with itself
                self.collision = self.block_pos_lst[0] in self.block_pos_lst[1:]
                if self.collision:
                    return
            else:  # check for collision with other snakes
                self.collision = self.block_pos_lst[0] in snake.block_pos_lst
                if self.collision:
                    return
