
# The tetris Board
class Board(object):

    def __init__(self, width=None, height=None, data=None):
        
        assert data or (width and height), 'Invalid arguments'

        if data:
            data = data.split(';')
            data = [line.split(',') for line in data]
            self.data = [[int(el) for el in line] for line in data]
            self.width = len(self.data[0])
            self.height = len(self.data)
        else:
            self.width = width
            self.height = height
            row = [0] * width
            self.data = [row[:] for i in range(height)]

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
                elif char == 2:
                    out += '+'
                elif char == 3:
                    out += '='
                else:
                    out += 'E'
            out += '|\n'
        out += '-' * (len(self.data[0]) + 2) + '\n'
        return out