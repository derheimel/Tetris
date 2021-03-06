__author__ = 'Aaron'
import random
import pygame
from pygame import Color
from block  import Block

init = pygame.init()

volume = 0.4

pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
pygame.mixer.music.load('sound/typea.mp3')
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)

board_width = 10
board_height = 20

block_size = 32
block_tuple = (block_size, block_size)

default_location = [3, -2]

smallfont = pygame.font.SysFont('comicsansms', 18)
bigfont = pygame.font.SysFont('comicsansms', 36)

status_surface_width = 150

screen_width = board_width * block_size + status_surface_width
screen_height = board_height * block_size
screen = pygame.display.set_mode((screen_width, screen_height))

next_block_surface = (
    screen_width - status_surface_width + (status_surface_width / 10),
    screen_height / 10,
    status_surface_width - (status_surface_width / 5),
    status_surface_width - (status_surface_width / 5)
)



next_block_pos = None

border_size = 5

blue = pygame.image.load('gfx/blue.png')
green = pygame.image.load('gfx/green.png')
orange = pygame.image.load('gfx/orange.png')
red = pygame.image.load('gfx/red.png')
turquoise = pygame.image.load('gfx/turquoise.png')
violet = pygame.image.load('gfx/violet.png')
yellow = pygame.image.load('gfx/yellow.png')
ghost = pygame.image.load('gfx/ghost.png')

blue = pygame.transform.scale(blue, block_tuple)
green = pygame.transform.scale(green, block_tuple)
orange = pygame.transform.scale(orange, block_tuple)
red = pygame.transform.scale(red, block_tuple)
turquoise = pygame.transform.scale(turquoise, block_tuple)
violet = pygame.transform.scale(violet,  block_tuple)
yellow = pygame.transform.scale(yellow, block_tuple)
ghost = pygame.transform.scale(ghost, block_tuple)

clock = pygame.time.Clock()
elapsed = 0
default_speed = 2.
speed = default_speed

score = 0
full_rows = 0
level = 0
lines_levelup = 5
line_counter = 0
game_over = False

block_types = [(turquoise, 'I'), (blue, 'J'), (orange, 'L'), (yellow, 'O'), (green, 'S'), (violet, 'T'), (red, 'Z')]
blocks = []
cur_block = None
ghost_block = None
next_block = None

def controller_tick():
    global game_over
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                return 0
            elif event.key == pygame.K_m:
                if pygame.mixer.music.get_volume() != 0:
                    pygame.mixer.music.set_volume(0)
                else:
                    pygame.mixer.music.set_volume(volume)
            elif event.key == pygame.K_r:
                restart()
                return 1
            if game_over:
                return 1
            elif event.key == pygame.K_UP:
                rotate()
            elif event.key == pygame.K_DOWN:
                if not down():
                    new_block()
            elif event.key == pygame.K_RIGHT:
                left_right('right')
            elif event.key == pygame.K_LEFT:
                left_right('left')
            elif event.key == pygame.K_SPACE:
                all_the_way_down(cur_block)
                new_block()

    global elapsed
    elapsed += clock.get_time()
    if elapsed >= (1000 / speed):
        if not down():
            if cur_block.pos[1] == default_location[1]:
                game_over = True
                return 1
            new_block()
        elapsed -= (1000 / speed)

    return 1

"""Restarts the game"""
def restart():
    global cur_block
    global next_block
    global blocks
    global score
    global level
    global game_over
    global elapsed
    global speed
    cur_block = None
    next_block = None
    blocks = []
    score = 0
    level = 0
    game_over = False
    elapsed = 0
    speed = default_speed
    new_block()


"""Places the current block as part of the scenery and generates a new block"""
def new_block():
    global cur_block
    global next_block
    if cur_block is not None:
        for x in cur_block.get_pieces_as_blocks():
            blocks.append(x)

        check_rows()
        cur_block = Block(next_block.sprite, next_block.type, default_location, board_width, board_height)

    else:
        new_type = random.choice(block_types)
        cur_block = Block(new_type[0], new_type[1], default_location, board_width, board_height)

    new_ghost_block()
    new_next_block()

def new_ghost_block():
    global ghost_block
    ghost_block = Block(ghost, cur_block.type, cur_block.pos, board_width, board_height)
    for x in range(cur_block.rotation_counter):
        ghost_block.rotate_90()
    all_the_way_down(ghost_block)

"""Generates a new block. Is called by new_block()"""
def new_next_block():
    global next_block
    global next_block_pos
    new_type = random.choice(block_types)
    next_block = Block(new_type[0], new_type[1], [0, 0], board_width, board_height)
    width, height = next_block.get_size()
    width *= block_size
    height *= block_size
    x = next_block_surface[0] + next_block_surface[2] / 2 - width / 2
    y = next_block_surface[1] + next_block_surface[3] / 2 - height / 2
    next_block_pos = [x, y]

"""Checks if there are full rows and deletes them."""
def check_rows():
    full_rows = []
    for y in range(board_height):
        full_row = True
        for x in range(board_width):
            found = False
            for block in blocks:
                if block.pos == [x, y]:
                    found = True
                    break

            if not found:
                full_row = False
                break

        if full_row:
            delete_row(y)
            full_rows.append(y)

    for row in full_rows:
        pull_everything_above(row)

    calc_score(full_rows)

def calc_score(full_rows):
    global score
    global line_counter
    global level
    global lines_levelup
    global speed
    plus = 0
    lines = len(full_rows)
    line_counter += lines
    if lines == 1:
        plus = 40
    elif lines == 2:
        plus = 100
    elif lines == 3:
        plus = 300
    elif lines == 4:
        plus = 1200

    plus *= level + 1
    score += plus

    if line_counter >= lines_levelup * (level + 1):
        line_counter = 0
        level += 1
        speed *= 1.15

"""Moves every row above <row> down until they touch"""
def pull_everything_above(row):
    for block in blocks:
        if block.pos[1] < row:
            block.move('down')

def delete_row(y):
    global blocks
    new_blocks = []
    for x in range(len(blocks)):
        block = blocks[x]
        if block.pos[1] != y:
            new_blocks.append(block)

    blocks = new_blocks

"""Moves the current block down to the bottom"""
def all_the_way_down(block):
    while block.is_in_bounds('down'):
        if len(blocks) == 0:
            block.move('down')
        else:
            found_collision = False
            for x in blocks:
                if block.detect_collision(x.pos, 'down'):
                    found_collision = True

            if not found_collision:
                block.move('down')
            else:
                return

"""Rotates the block with a horizontal tolerance of 1,
meaning that the rotation is still successful if a
collision would occur. In case of a collision the block
is moved 1 field left or right if that solves the collision."""
def rotate():
    if cur_block.is_in_bounds('rotate'):
        if not detect_collision('rotate'):
            cur_block.rotate_90()
    else:
        cur_block.move('left')
        if cur_block.is_in_bounds('rotate'):
            cur_block.rotate_90()
        else:
            cur_block.move('right', 2)
            if cur_block.is_in_bounds('rotate'):
                cur_block.rotate_90()
            else:
                 cur_block.move('left')

    new_ghost_block()

"""Checks if the current block would collide with something
when moved in <direction>"""
def detect_collision(direction):
    for x in blocks:
        if cur_block.detect_collision(x.pos, direction):
            return True

    return False

"""Checks if the current block can move down without touching something"""
def down():
    if cur_block.is_in_bounds('down'):
        for x in blocks:
            if cur_block.detect_collision(x.pos, 'down'):
                return False
    else:
        return False

    cur_block.move('down')
    return True

"""Moves the current block to <direction>"""
def left_right(direction):
    if cur_block.is_in_bounds(direction):
        for x in blocks:
            if cur_block.detect_collision(x.pos, direction):
                return

        cur_block.move(direction)
        new_ghost_block()

def view_tick():
    screen.fill(Color('white'))

    render_borders()
    render_text()

    if not game_over:
        ghost_block.render(screen)
        cur_block.render(screen)
        for block in blocks:
            block.render(screen)

    next_block.render(screen, pos = next_block_pos)

    pygame.display.update()

def render_text():
    global speed

    if game_over:
        text = 'GAME OVER'
        line_height = bigfont.size(text)[1]
        x = (screen_width - status_surface_width) / 2 - bigfont.size(text)[0] / 2
        y = screen_height / 4
        text = bigfont.render(text, True, Color('black'))
        screen.blit(text, [x, y])

        text = 'press r to start over'
        x = (screen_width - status_surface_width) / 2 - smallfont.size(text)[0] / 2
        y += line_height + 5
        text = smallfont.render(text, True, Color('black'))
        screen.blit(text, [x, y])

    text = smallfont.render('Score: ' + str(score), True, Color('black'))
    x = next_block_surface[0]
    y = next_block_surface[1] + next_block_surface[3] + 30
    screen.blit(text, [x, y])

    text = smallfont.render('Level: ' + str(level), True, Color('black'))
    y += 30
    screen.blit(text, [x, y])

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
    new_block()

    while 1:
        if not controller_tick():
            return

        view_tick()

        clock.tick(60)

main()
pygame.quit()
quit()
