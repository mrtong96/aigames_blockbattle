
PIECES = {
    'I': [[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]],
    'J': [[1,0,0],[1,1,1],[0,0,0]],
    'L': [[0,0,1],[1,1,1],[0,0,0]],
    'O': [[1,1],[1,1]],
    'S': [[0,1,1],[1,1,0],[0,0,0]],
    'T': [[0,1,0],[1,1,1],[0,0,0]],
    'Z': [[1,1,0],[0,1,1],[0,0,0]]
}

NUM_ROTATIONS = {
    'I': 2,
    'J': 4,
    'L': 4,
    'O': 1,
    'S': 2,
    'T': 4,
    'Z': 2
}

class Piece(object):

    def __init__(self, _type, right_rotations=0, left_rotations=0):
        self._type = _type
        self.data = PIECES[_type]
        self.size = len(self.data)

        self.right_rotations = 0
        for i in range(right_rotations):
            self.rotate_right()
        for i in range(left_rotations):
            self.rotate_left()

    def rotate_right(self):
        self.right_rotations = (self.right_rotations + 1) % 4
        row = [0] * self.size
        result = [row[:] for i in range(self.size)]
        for y in range(self.size):
            for x in range(self.size):
                result[x][self.size - y - 1] = self.data[y][x]
        self.data = result

    def rotate_left(self):
        self.right_rotations = (self.right_rotations - 1) % 4
        row = [0] * self.size
        result = [row[:] for i in range(self.size)]
        for y in range(self.size):
            for x in range(self.size):
                result[self.size - x - 1][y] = self.data[y][x]
        self.data = result

    def get_locations(self):
        blocks = []
        for y, row in enumerate(self.data):
            for x, el in enumerate(row):
                if el:
                    blocks.append((x, y))
        return blocks

    def copy(self):
        return Piece(_type=self._type, right_rotations=self.right_rotations)

    def equals(self, other):
        return self._type == other._type and self.right_rotations == other.right_rotations

    def __repr__(self):
        return str(self)

    def __str__(self):
        out = '-' * (len(self.data[0]) + 2) + '\n'
        for line in self.data:
            out += '|'
            for char in line:
                if char == 0:
                    out += ' '
                elif char == 1:
                    out += '*'
            out += '|\n'
        out += '-' * (len(self.data[0]) + 2) + '\n'
        return out
