
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
        # copies data
        self.data = map(lambda row: row[:], PIECES[_type])
        self.size = len(self.data)

        self.right_rotations = 0
        num_rotations = (right_rotations - left_rotations) % 4
        if num_rotations < 3:
            for i in range(num_rotations):
                self.rotate_right()
        else:
            for i in range(4 - num_rotations):
                self.rotate_left()

    # does an in-place rotation
    def rotate_right(self):
        self.right_rotations = (self.right_rotations + 1) % 4
        for y1 in range(self.size / 2):
            for x1 in range((self.size + 1) / 2):
                y2 = self.size - y1 - 1
                x2 = self.size - x1 - 1

                tmp = self.data[y1][x1]
                self.data[y1][x1] = self.data[x2][y1]
                self.data[x2][y1] = self.data[y2][x2]
                self.data[y2][x2] = self.data[x1][y2]
                self.data[x1][y2] = tmp

    # does an in-place rotation
    def rotate_left(self):
        self.right_rotations = (self.right_rotations - 1) % 4
        for y1 in range(self.size / 2):
            for x1 in range((self.size + 1) / 2):
                y2 = self.size - y1 - 1
                x2 = self.size - x1 - 1

                tmp = self.data[y1][x1]
                self.data[y1][x1] = self.data[x1][y2]
                self.data[x1][y2] = self.data[y2][x2]
                self.data[y2][x2] = self.data[x2][y1]
                self.data[x2][y1] = tmp

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
