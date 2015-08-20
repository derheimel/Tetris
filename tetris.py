__author__ = 'Aaron'
import pygame
from pygame import Color
from block  import Block

init = pygame.init()

board_width = 10
board_height = 20

block_size = 32
block_tuple = (block_size, block_size)

screen_width = board_width * block_size
screen_height = board_height * block_size
screen = pygame.display.set_mode((screen_width, screen_height))

border_size = 5

blue = pygame.image.load('gfx/blue.png')
green = pygame.image.load('gfx/green.png')
orange = pygame.image.load('gfx/orange.png')
red = pygame.image.load('gfx/red.png')
turquoise = pygame.image.load('gfx/turquoise.png')
violet = pygame.image.load('gfx/violet.png')
yellow = pygame.image.load('gfx/yellow.png')

blue = pygame.transform.scale(blue, block_tuple)
green = pygame.transform.scale(green, block_tuple)
orange = pygame.transform.scale(orange, block_tuple)
red = pygame.transform.scale(red, block_tuple)
turquoise = pygame.transform.scale(turquoise, block_tuple)
violet = pygame.transform.scale(violet,  block_tuple)
yellow = pygame.transform.scale(yellow, block_tuple)

clock = pygame.time.Clock()

blocks = []
cur_block = None
next_block = None

def controller_tick():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                return 0
            elif event.key == pygame.K_UP:
                cur_block.rotate_90()
            elif event.key == pygame.K_DOWN:
                down()
            elif event.key == pygame.K_RIGHT:
                left_right('right')
            elif event.key == pygame.K_LEFT:
                left_right('left')
            elif event.key == pygame.K_SPACE:
                cur_block.move('down', board_height + 2)

    return 1

def down():
    if cur_block.is_in_bounds(board_width, board_height, 'down'):
        for x in blocks:
            if cur_block.detect_collision(x.pos, 'down'):
                return False
    else:
        return False

    cur_block.move('down')
    return True

def left_right(direction):
    if cur_block.is_in_bounds(board_width, board_height, direction):
        print 'is in bounds'
        for x in blocks:
            if cur_block.detect_collision(x.pos, direction):
                return

        cur_block.move(direction)

def view_tick():
    screen.fill(Color('white'))

    render_borders()

    for block in blocks:
        block.render(screen)

    cur_block.render(screen)

    pygame.display.update()

def render_borders():
    pygame.draw.line(
        screen,
        Color('black'),
        (0, 0),
        (0, block_size * board_height),
        border_size
    )
    pygame.draw.line(
        screen,
        Color('black'),
        (0, 0),
        (block_size * board_width, 0),
        border_size
    )
    pygame.draw.line(
        screen,
        Color('black'),
        (block_size * board_width, 0),
        (block_size * board_width, block_size * board_height),
        border_size
    )
    pygame.draw.line(
        screen,
        Color('black'),
        (0, block_size * board_height),
        (block_size * board_width, block_size * board_height),
        border_size
    )

def main():
    global cur_block
    cur_block = Block(green, 'Z', [0, 0])

    while 1:
        if not controller_tick():
            return

        view_tick()

        clock.tick(60)

main()
pygame.quit()
quit()
