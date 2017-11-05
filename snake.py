import sys
import pygame
import random

pygame.init()

size = width, height = 640, 480
black = 0, 0, 0

screen = pygame.display.set_mode(size)

rect_size = 20, 20
start_pos = 300, 200

def get_dir_from_key(old_dir, key_pressed_stack):

    new_dir = old_dir
    if key_pressed_stack:
        key_pressed = key_pressed_stack[0]
        if key_pressed == pygame.K_UP:
            new_dir = [0, -1]
        elif key_pressed == pygame.K_RIGHT:
            new_dir = [1, 0]
        elif key_pressed == pygame.K_DOWN:
            new_dir = [0, 1]
        elif key_pressed == pygame.K_LEFT:
            new_dir = [-1, 0]

        # if snake just reverts direction, don't allow it
        if new_dir == [-old_dir[0], -old_dir[1]]:
            new_dir = old_dir

        key_pressed_stack.pop(0)

    return key_pressed_stack, new_dir

def set_new_snake_state(rect_pos_lst, direction):
    rect_pos_lst = [(rect_pos_lst[0][0] + direction[0]*rect_size[0], rect_pos_lst[0][1] + direction[1]*rect_size[1])] + rect_pos_lst
    rect_pos_lst.pop()

    if rect_pos_lst[0] in rect_pos_lst[1:]:
        collision = True
    elif rect_pos_lst[0][0] > width or rect_pos_lst[0][1] > height or rect_pos_lst[0][0] < 0 or rect_pos_lst[0][1] < 0:
        collision = True
    else:
        collision = False

    return rect_pos_lst, collision

def set_new_cherry_pos(snake_rect_pos_lst):
    new_cherry_pos = random.randrange(0, width, rect_size[0]), random.randrange(0, height, rect_size[0])
    while new_cherry_pos in snake_rect_pos_lst:
        new_cherry_pos = random.randrange(0, width, rect_size[0]), random.randrange(0, height, rect_size[0])

    return new_cherry_pos

def init_game():
    cherry_pos = set_new_cherry_pos([])

    rect_pos_lst = []
    # set first three rectangles
    for i in range(3):
        rect_pos_lst.append((start_pos[0] - i * rect_size[0], start_pos[1]))

    direction = [1, 0]

    return rect_pos_lst, cherry_pos, direction


refresh_rate = 100
pygame.time.set_timer( pygame.USEREVENT , refresh_rate )

timer = pygame.time.get_ticks()

rect_pos_lst, cherry_pos, direction = init_game()
key_stack = [pygame.key.get_pressed()]
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            key_stack.append(event.key)
        elif event.type == pygame.USEREVENT:

            key_stack, direction = get_dir_from_key(direction, key_stack)
            screen.fill(black)

            rect_pos_lst, collision = set_new_snake_state(rect_pos_lst, direction)
            if collision:
                rect_pos_lst, cherry_pos, direction = init_game()

            if rect_pos_lst[0] == cherry_pos:
                cherry_pos = set_new_cherry_pos(rect_pos_lst)
                rect_pos_lst.append((rect_pos_lst[-1][0], rect_pos_lst[-1][1]))

            # draw snake
            for rect_pos in rect_pos_lst:
                pygame.draw.rect(screen, (0, 255, 0), (rect_pos[0], rect_pos[1], rect_size[0], rect_size[1]))

            # draw cherry
            pygame.draw.rect(screen, (255, 0, 0), (cherry_pos[0], cherry_pos[1], rect_size[0], rect_size[1]))

            pygame.display.update()

