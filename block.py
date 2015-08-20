__author__ = 'Aaron'
import numpy
import pygame
class Block():

    def __init__(self, sprite, type, pos):
        self._sprite = sprite
        self._sprite_size = sprite.get_rect().height
        self._type = type
        self._pos = pos
        self._pieces_pos = []
        self._pieces = numpy.array(self._calculate_pieces())

        self._counter = 0
        self._rotation_counter = 0

    @property
    def pos(self):
        return self._pos

    @property
    def pieces_pos(self):
        self._pieces_pos = []
        for x in range(4):
            self._next_pos()

        self._counter = 0
        return self._pieces_pos

    def _calculate_pieces(self):
        if self._type == 'I':
            pieces = [[1 for x in range(1)] for x in range(4)]
        elif self._type == 'O':
            pieces = [[1 for x in range(2)] for x in range(2)]
        else:
            pieces = [[0 for x in range(2)] for x in range(3)]
            if self._type == 'J':
                pieces[0][0] = 1
                pieces[0][1] = 1
                pieces[1][1] = 1
                pieces[2][1] = 1
            elif self._type == 'L':
                pieces[2][0] = 1
                pieces[0][1] = 1
                pieces[1][1] = 1
                pieces[2][1] = 1
            elif self._type == 'S':
                pieces[1][0] = 1
                pieces[2][0] = 1
                pieces[0][1] = 1
                pieces[1][1] = 1
            elif self._type == 'T':
                pieces[1][0] = 1
                pieces[0][1] = 1
                pieces[1][1] = 1
                pieces[2][1] = 1
            elif self._type == 'Z':
                pieces[0][0] = 1
                pieces[1][0] = 1
                pieces[1][1] = 1
                pieces[2][1] = 1

        return pieces

    def _get_rotation_offset(self):
        x_offset = 0
        y_offset = 0
        if self._type == 'I':
            if self._rotation_counter % 4 == 1 or self._rotation_counter % 4  == 3:
                x_offset = 1
                y_offset = -2

        return x_offset, y_offset

    def _next_pos(self):
        x_offset, y_offset = self._get_rotation_offset()

        pos = (0, 0)
        find = False
        counter = 0
        for x in range(len(self._pieces)):
            for y in range(len(self._pieces[x])):
                if self._pieces[x][y] == 1:
                    if counter >= self._counter:
                        self._counter += 1
                        find = True
                        pos = (x + self._pos[0] + x_offset, y + self._pos[1] + y_offset)
                        self._pieces_pos.append(pos)
                        counter += 1
                        break

                    counter += 1

            if find:
                break

        return pos

    def get_rect(self):
        width = len(self._pieces) * self._sprite_size
        height = len(self._pieces) * self._sprite_size
        return self._pos, (width, height)

    def rotate_90(self, inverse = False):
        self._pieces = numpy.rot90(self._pieces)
        self._rotation_counter += 1
        print self.pieces_pos

    def move(self, direction, distance = None, block = None):
        if distance is None:
            distance = 1

        if block is None:
            block = self

        new_pos = list(block._pos)
        if direction == 'down':
            new_pos[1] = block._pos[1] + distance
        elif direction == 'right':
            new_pos[0] = block._pos[0] + distance
        elif direction == 'left':
            new_pos[0] = block._pos[0] - distance

        block._pos = new_pos

    def detect_collision(self, pos, direction):
        block = Block(self._sprite, self._type, self._pos)
        self.move(direction, block=block)

        for xy in block.pieces_pos:
            if xy == pos:
                return True

    def is_in_bounds(self, board_width, board_height, direction):
        min_x = 0
        max_x = board_width
        max_y = board_height

        block = Block(self._sprite,  self._type, self._pos)
        self.move(direction, block=block)
        positions = block.pieces_pos

        for xy in positions:
            if xy[0] < min_x or xy[0] >= max_x or xy[1] >= max_y:
                return False

        return True

    def get_pieces_as_blocks(self):
        blocks = []
        for x in self._pieces_pos:
            blocks.append(Block(self._sprite, '.', x))

        return blocks

    def render(self, screen):
        self._pieces_pos = []
        for x in range(4):
            screen.blit(self._sprite, tuple(self._sprite_size * x for x in self._next_pos()))

        self._counter = 0