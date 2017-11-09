import sys
import pygame
import random
from SnakeClass import Snake

pygame.init()

size = width, height = 640, 480
black = 0, 0, 0

refresh_rate = 100

screen = pygame.display.set_mode(size)

start_pos = 300, 200


def set_new_cherry_pos(snake_lst):
    new_cherry_pos = random.randrange(0, width, Snake.block_size), random.randrange(0, height, Snake.block_size)

    # check if new cherry position is within any of the snakes and set new one
    for snk in snake_lst:
        while new_cherry_pos in snk.block_pos_lst:
            new_cherry_pos = random.randrange(0, width, Snake.block_size), random.randrange(0, height, Snake.block_size)

    return new_cherry_pos


def init_game():

    snake1 = Snake(start_pos=(300, 200),
                   move_keys={'up': pygame.K_UP,
                              'right': pygame.K_RIGHT,
                              'down': pygame.K_DOWN,
                              'left': pygame.K_LEFT},
                   color=(0, 255, 0),
                   num_of_start_blocks=10)

    snake2 = Snake(start_pos=(300, 300),
                   move_keys={'up': pygame.K_w,
                              'right': pygame.K_d,
                              'down': pygame.K_s,
                              'left': pygame.K_a},
                   color=(0, 0, 255),
                   num_of_start_blocks=10)
    init_snake_lst = [snake1, snake2]

    new_cherry_pos = set_new_cherry_pos(init_snake_lst)

    return init_snake_lst, new_cherry_pos


pygame.time.set_timer(pygame.USEREVENT, refresh_rate)

timer = pygame.time.get_ticks()

snake_lst, cherry_pos = init_game()
# key_stack = [pygame.key.get_pressed()]
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            for snake in snake_lst:
                if event.key in [val for _, val in snake.move_keys.items()]:
                    snake.key_stack.append(event.key)
        elif event.type == pygame.USEREVENT:

            for snake in snake_lst:
                snake.get_dir_from_keystack()
                snake.set_new_state(size, snake_lst)

                # check if there is collision
                if snake.collision:
                    snake_lst, cherry_pos = init_game()

                # check if cherry was eaten
                if snake.block_pos_lst[0] == cherry_pos:
                    snake.block_pos_lst.append(snake.block_pos_lst[-1])
                    cherry_pos = set_new_cherry_pos(snake_lst)

            screen.fill(black)

            # draw snake
            for snake in snake_lst:
                for block_pos in snake.block_pos_lst:
                    pygame.draw.rect(screen,
                                     snake.color,
                                     (block_pos[0], block_pos[1], Snake.block_size, Snake.block_size))

            # draw cherry
            pygame.draw.rect(screen, (255, 0, 0), (cherry_pos[0], cherry_pos[1], Snake.block_size, Snake.block_size))

            pygame.display.update()
