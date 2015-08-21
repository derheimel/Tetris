__author__ = 'Aaron'
import numpy
class Block(object):

    def __init__(self, sprite, type, pos, board_width, board_heigth):
        self._sprite = sprite
        self._sprite_size = sprite.get_rect().height
        self._type = type
        self._pos = pos
        self.board_width = board_width
        self.board_height = board_heigth
        self._pieces_pos = []
        self._pieces = numpy.array(self._calculate_pieces())

        self._counter = 0
        self._rotation_counter = 0

    def get_size(self):
        return len(self._pieces), len(self._pieces[0])

    @property
    def sprite(self):
        return self._sprite

    @property
    def type(self):
        return self._type

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    @property
    def pieces_pos(self):
        self._pieces_pos = []
        for x in range(4):
            self._next_pos()

        self._counter = 0
        return self._pieces_pos

    @property
    def rotation_counter(self):
        return  self._rotation_counter

    def _calculate_pieces(self):
        if self._type == '.':
            pieces = [[1]]
        elif self._type == 'I':
            pieces = [[0 for x in range(4)] for x in range(4)]
            pieces[0][1] = 1
            pieces[1][1] = 1
            pieces[2][1] = 1
            pieces[3][1] = 1
        elif self._type == 'O':
            pieces = [[1 for x in range(2)] for x in range(2)]
        else:
            pieces = [[0 for x in range(3)] for x in range(3)]
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

    def _next_pos(self):

        pos = [0, 0]
        find = False
        counter = 0
        for x in range(len(self._pieces)):
            for y in range(len(self._pieces[x])):
                if self._pieces[x][y] == 1:
                    if counter >= self._counter:
                        self._counter += 1
                        find = True
                        pos = [x + self._pos[0], y + self._pos[1]]
                        self._pieces_pos.append(pos)
                        counter += 1
                        break

                    counter += 1

            if find:
                break

        return pos

    def rotate_90(self, inverse = False):
        self._pieces = numpy.rot90(self._pieces)
        self._rotation_counter += 1

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
        elif direction =='rotate':
            self.rotate_90()

        block._pos = new_pos

    def detect_collision(self, pos, direction):
        block = Block(self._sprite, self._type, self._pos, self.board_width, self.board_height)
        for x in range(self.rotation_counter):
            block.rotate_90()
        self.move(direction, block=block)

        for xy in block.pieces_pos:
            if xy == pos:
                return True

    def is_in_bounds(self, direction):
        min_x = 0
        max_x = self.board_width
        max_y = self.board_height

        block = Block(self._sprite,  self._type, self._pos, self.board_width, self.board_height)
        for x in range(self.rotation_counter):
            block.rotate_90()
        block.move(direction, block=block)

        positions = block.pieces_pos

        for xy in positions:
            if xy[0] < min_x or xy[0] >= max_x or xy[1] >= max_y:
                return False

        return True

    def get_pieces_as_blocks(self):
        blocks = []
        for x in self.pieces_pos:
            blocks.append(Block(self._sprite, '.', x, self.board_width, self.board_height))

        return blocks

    def render(self, screen, pos = None):
        iter = len(self.pieces_pos)
        self._pieces_pos = []

        if pos is not None:
            for x in range(iter):
                next_pos = self._next_pos()
                screen.blit(self.sprite, [pos[0] + (next_pos[0] * self._sprite_size), pos[1] + (next_pos[1] * self._sprite_size)])

        else:
            for x in range(iter):
                screen.blit(self.sprite, tuple(self._sprite_size * x for x in self._next_pos()))

        self._counter = 0