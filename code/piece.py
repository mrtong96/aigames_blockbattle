
PIECES = {
    'I_PIECE': [[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]],
    'J_PIECE': [[1,0,0],[1,1,1],[0,0,0]],
    'L_PIECE': [[0,0,1],[1,1,1],[0,0,0]],
    'O_PIECE': [[1,1],[1,1]],
    'S_PIECE': [[0,1,1],[1,1,0],[0,0,0]],
    'T_PIECE': [[0,1,0],[1,1,1],[0,0,0]],
    'Z_PIECE': [[1,1,0],[0,1,1],[0,0,0]]
}

class Piece(object):

    def __init__(self, _type):
        if _type.islower():
            _type = _type.upper()
        self.data = PIECES['{}_PIECE'.format(_type)]
        self.size = len(self.data)

    def rotate_right(self):
        row = [0] * self.size
        result = [row[:] for i in range(self.size)]
        for y in range(self.size):
            for x in range(self.size):
                result[x][self.size - y - 1] = self.data[y][x]
        self.data = result

    def rotate_left(self):
        row = [0] * self.size
        result = [row[:] for i in range(self.size)]
        for y in range(self.size):
            for x in range(self.size):
                result[self.size - x - 1][y] = self.data[y][x]
        self.data = result

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
