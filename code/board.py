
from piece import Piece, PIECES, NUM_ROTATIONS
from search import BoardSearchProblem, aStarSearch, boardHeuristic, depthFirstSearch
from copy import copy, deepcopy
import time

def matrix_to_list(matrix, filter_func=lambda x: x):
    result = []
    for y, row in enumerate(matrix):
        for x, el in enumerate(row):
            if filter_func(el):
                result.append((x, y))
    return result

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

    def copy(self):
        b = Board(width=self.width, height=self.height)
        b.data = deepcopy(self.data)
        return b

    # returns tuples of piece_type, num rotations right, position
    # returns list of valid final positions of the piece
    def get_valid_positions(self, piece_type):
        valid_positions = []
        piece = Piece(piece_type)

        for i in range(NUM_ROTATIONS[piece_type]):

            blocks = piece.get_locations()

            p_minx = min(map(lambda x: x[0], blocks))
            p_maxx = max(map(lambda x: x[0], blocks))
            p_miny = min(map(lambda x: x[1], blocks))
            p_maxy = max(map(lambda x: x[1], blocks))

            lowest_blocks = filter(lambda x: x[1] == p_miny, blocks)

            # refers to the top left corner of the block (0,0)
            for y in range(-p_miny, self.height - p_maxy):
                for x in range(-p_minx, self.width - p_maxx):
                    shift_blocks = map(lambda b: (x + b[0], y + b[1]), blocks)

                    conflict_space = map(lambda x: self.data[x[1]][x[0]] > 1, shift_blocks)
                    conflict_space = reduce(lambda x, y: x or y, conflict_space)

                    if conflict_space:
                        continue

                    floor_exists = False
                    for x_block, y_block in shift_blocks:
                        if y_block == self.height - 1 or self.data[y_block + 1][x_block] > 1:
                            floor_exists = True

                    if not floor_exists:
                        continue

                    valid_positions.append((Piece(piece_type, right_rotations=i), x, y))

            piece.rotate_right()

        return valid_positions
    
    def place_piece(self, piece, x, y):

        blocks = matrix_to_list(piece.data)

        shift_blocks = map(lambda b: (x + b[0], y + b[1]), blocks)

        for x_pos, y_pos in shift_blocks:
            if self.data[y_pos][x_pos] > 1:
                print 'Error'
                return
            self.data[y_pos][x_pos] = 2

    def remove_piece(self, piece, x, y):
        blocks = matrix_to_list(piece.data)

        shift_blocks = map(lambda b: (x + b[0], y + b[1]), blocks)

        for x_pos, y_pos in shift_blocks:
            if self.data[y_pos][x_pos] < 2:
                print 'Error'
                return
            self.data[y_pos][x_pos] = 0

    # gets the path for piece going from start_loc to end_loc
    def get_path(self, start_piece, start_loc, end_piece, end_loc):
        piece_type = start_piece._type
        start_rot = start_piece.right_rotations
        end_rot = end_piece.right_rotations
        problem = BoardSearchProblem(self, piece_type, end_rot, end_loc, start_rot, start_loc)
        backwards_path = aStarSearch(problem, boardHeuristic)

        if backwards_path == 'Error':
            return []

        path_map = {'up': 'down', 'left': 'right', 'right':'left',\
            'turnleft': 'turnright', 'turnright': 'turnleft'}

        path = []
        for action in backwards_path[::-1]:
            path.append(path_map[action])

        while path and path[-1] == 'down':
            path.pop()

        path.append('drop')

        return path

    def get_feature_vector(self):
        feature_vector = {}
        row_data = map(lambda row: map(lambda x: 1 if x > 1 else 0, row), self.data)
        col_data = zip(*row_data)

        def highest(col):
            ht = self.height
            for el in col:
                if el:
                    break
                ht -= 1
            return ht

        highest_cols = map(lambda col: highest(col), col_data)
        feature_vector['sum_highest'] = sum(highest_cols)

        solid_rows = map(lambda row: reduce(lambda x, y: x and y, row), row_data)
        feature_vector['solid_lines'] = sum(solid_rows)

        height_diffs = []
        for i in range(len(highest_cols) - 1):
            height_diffs.append(abs(highest_cols[i] - highest_cols[i + 1]))
        feature_vector['sum_height_diffs'] = sum(height_diffs)

        spaces = map(lambda row: map(lambda x: 1 if not x else 0, row), row_data)
        spaces = matrix_to_list(spaces)

        not_holes = set(filter(lambda x: x[1] == 0, spaces))

        fringe = not_holes.copy()
        while len(fringe):
            x, y = fringe.pop()
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            for neighbor in neighbors:
                if neighbor in spaces and neighbor not in not_holes:
                    not_holes.add(neighbor)
                    fringe.add(neighbor)

        feature_vector['hole_num'] = len(set(spaces) - not_holes)

        return feature_vector

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

def test0():
    t0 = time.time()
    b = Board(data='0,0,0,0,0;0,0,0,0,0;2,2,2,2,2;2,0,2,0,2;2,2,2,2,2')
    b = Board(10, 20)
    piece1 = 'T'
    piece2 = 'T'
    valid_positions1 = b.get_valid_positions(piece1)
    
    feature_vectors = {}

    counter = 0

    for pos1 in valid_positions1:
        b.place_piece(*pos1)

        feature_vectors[pos1] = b.get_feature_vector()
        b.remove_piece(*pos1)

    print counter
    print time.time() - t0

def test1():
    b = Board(10,10)
    base=Board(data='0,0,0,1,1,1,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,2,2,0,0,0,0,0;0,0,0,0,2,2,0,0,0,0;0,0,0,2,2,0,0,0,0,0;0,0,0,0,2,2,0,0,0,0;0,0,0,0,2,2,0,0,0,0;0,0,0,2,2,2,0,0,0,0;0,0,0,2,2,2,0,0,0,0')
    p1 = Piece('I')
    p2 = Piece('I')
    p2.rotate_right()
    loc1 = (0,0)
    loc2 = (2,2)

    path = b.get_path(p1, loc1, p2, loc2)

    result = b.get_feature_vector()
    print result

def test2():
    import time
    t0 = time.time()
    total = 0
    for piece in PIECES:
        b = Board(data='0,0,0,1,1,1,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,2,2,0,0,0,0,0;0,0,0,0,2,2,0,0,0,0;0,0,0,2,2,0,0,0,0,0;0,0,0,0,2,2,0,0,0,0;0,0,0,0,2,2,0,0,0,0;0,0,0,2,2,2,0,0,0,0;0,0,0,2,2,2,0,0,0,0')
        base_piece = Piece(piece, right_rotations=0)
        res = b.get_valid_positions(piece)
        total += len(res)
        for el in res:
            b = Board(data='0,0,0,1,1,1,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,2,2,0,0,0,0,0;0,0,0,0,2,2,0,0,0,0;0,0,0,2,2,0,0,0,0,0;0,0,0,0,2,2,0,0,0,0;0,0,0,0,2,2,0,0,0,0;0,0,0,2,2,2,0,0,0,0;0,0,0,2,2,2,0,0,0,0')
            b.place_piece(el[0], el[1], el[2])
            start_loc = (3, -1)
            problem = BoardSearchProblem(b, el[0]._type, el[0].right_rotations, (el[1], el[2]), base_piece.right_rotations, start_loc)
            path = aStarSearch(problem, boardHeuristic)
            
            print b
            print path
            
    print time.time() - t0
    print total

def test3():
    base=Board(data='0,0,0,1,1,1,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,2,2,0,0,0,0,0;0,0,0,0,2,2,0,0,0,0;0,0,0,2,2,0,0,0,0,0;0,0,0,0,2,2,0,0,0,0;0,0,0,0,2,2,0,0,0,0;0,0,0,2,2,2,0,0,0,0;0,0,0,2,2,2,0,0,0,0')
    first_type = 'S'
    second_type = 'L'
    positions = base.get_valid_positions(first_type)
    boards = []
    for position in positions:
        b=Board(data='0,0,0,1,1,1,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,2,2,0,0,0,0,0;0,0,0,0,2,2,0,0,0,0;0,0,0,2,2,0,0,0,0,0;0,0,0,0,2,2,0,0,0,0;0,0,0,0,2,2,0,0,0,0;0,0,0,2,2,2,0,0,0,0;0,0,0,2,2,2,0,0,0,0')
        b.place_piece(el[0], el[1], el[2])

def test4():
    import time
    t0 = time.time()
    base=Board(data='0,0,0,1,1,1,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0;0,0,0,2,2,0,0,0,0,0;0,0,0,0,2,2,0,0,0,0;0,0,0,2,2,0,0,0,0,0;0,0,0,0,2,2,0,0,0,0;0,0,0,0,2,2,0,0,0,0;0,0,0,2,2,2,0,0,0,0;0,0,0,2,2,2,0,0,0,0')
    for i in range(10):
        base.get_feature_vector()
    print time.time() - t0

def test5():
    b = Board(data='0,0,0,0,0;0,0,0,0,0;2,2,2,2,2;2,0,2,0,2;2,2,2,2,2')
    print b
    result = b.get_feature_vector()
    print result
    #self.assertEquals(result, {'solid_lines': 0, 'sum_highest': 10, 'sum_height_diffs': 15, 'hole_num': 0})

#test0()



