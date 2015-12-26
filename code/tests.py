
import unittest
import piece
import board
import random
import search
import time
import genetic_alg

class TestPiece(unittest.TestCase):
    def test_rotation_count(self):
        for _type in piece.PIECES:
            p1 = piece.Piece(_type)
            p2 = p1.copy()

            for i in range(4):
                p1.rotate_right()

            self.assertTrue(p1.equals(p2))

            for i in range(4):
                p1.rotate_left()

            self.assertTrue(p1.equals(p2))

    # even size
    def test_one_rotation(self):
        p = piece.Piece('I')
        p.rotate_right()
        rotated_data = [[0,0,1,0],[0,0,1,0],[0,0,1,0],[0,0,1,0]]
        self.assertEquals(p.data, rotated_data)
        p.rotate_left()
        rotated_data = [[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]]
        self.assertEquals(p.data, rotated_data)

    # odd size
    def test_one_rotation2(self):
        p = piece.Piece('L')
        p.rotate_right()
        rotated_data = [[0,1,0],[0,1,0],[0,1,1]]
        self.assertEquals(p.data, rotated_data)
        p.rotate_left()
        rotated_data = [[0,0,1],[1,1,1],[0,0,0]]
        self.assertEquals(p.data, rotated_data)

    def test_get_locations(self):
        answers = {
            'I': [(0,1),(1,1),(2,1),(3,1)],
            'J': [(0,0),(0,1),(1,1),(2,1)],
            'L': [(2,0),(0,1),(1,1),(2,1)],
            'O': [(0,0),(0,1),(1,0),(1,1)],
            'S': [(1,0),(2,0),(0,1),(1,1)],
            'T': [(1,0),(0,1),(1,1),(2,1)],
            'Z': [(0,0),(1,0),(1,1),(2,1)]
        }

        for _type in answers:
            p = piece.Piece(_type)
            data = p.get_locations()
            self.assertEquals(set(data), set(answers[_type]))

    def test_copy(self):
        for _type in piece.PIECES:
            for num_rotations in range(4):
                p1 = piece.Piece(_type, num_rotations)
                p2 = p1.copy()
                self.assertEquals(p1._type, p2._type)
                self.assertEquals(p1.data, p2.data)
                self.assertEquals(p1.size, p2.size)
                self.assertEquals(p1.right_rotations, p2.right_rotations)
                self.assertTrue(p1.equals(p2))

class TestBoard(unittest.TestCase):
    def test_default_init(self):
        for width in range(1,4):
            for height in range(1,4):
                b = board.Board(width=width, height=height)
                self.assertEquals(width, b.width)
                self.assertEquals(height, b.height)
                for row in b.data:
                    for el in row:
                        self.assertEquals(0, el)

    def test_default_data(self):
        data = '0,1,2,3;1,2,3,0;2,3,0,1;3,0,1,2'
        b = board.Board(data=data)
        self.assertEquals(4, b.width)
        self.assertEquals(4, b.height)
        data = [[0,1,2,3],[1,2,3,0],[2,3,0,1],[3,0,1,2]]
        self.assertEquals(b.data, data)

    def test_valid_positions_blank(self):
        b = board.Board(width=5, height=5)
        positions = b.get_valid_positions('I')
        self.assertEquals(len(positions), 7)
        positions = map(lambda x: (x[0].right_rotations, x[1], x[2]), positions)
        correct_positions = [(0,0,3),(0,1,3),(1,-2,1),(1,-1,1),(1,0,1),(1,1,1),(1,2,1)]
        self.assertEquals(set(correct_positions), set(positions))

    def test_valid_positions_floor(self):
        b = board.Board(width=5, height=6)
        for i in range(len(b.data[5])):
            b.data[5][i] = 3
        positions = b.get_valid_positions('I')
        self.assertEquals(len(positions), 7)
        positions = map(lambda x: (x[0].right_rotations, x[1], x[2]), positions)
        correct_positions = [(0,0,3),(0,1,3),(1,-2,1),(1,-1,1),(1,0,1),(1,1,1),(1,2,1)]
        self.assertEquals(set(correct_positions), set(positions))

class testBoard(unittest.TestCase):
    def test_feature_vector(self):
        b = board.Board(5,5)
        result = b.get_feature_vector()
        self.assertEquals(result, {'points_scored': 0, 'sum_highest': 0, 'sum_height_diffs': 0, 'hole_num': 0})

        b = board.Board(data='0,0,0,0,0;0,0,0,0,0;0,0,0,0,0;0,0,0,0,0;2,2,2,2,2')
        result = b.get_feature_vector()
        self.assertEquals(result, {'points_scored': 1, 'sum_highest': 5, 'sum_height_diffs': 0, 'hole_num': 0})

        b = board.Board(data='2,0,0,0,0;0,2,0,0,0;0,0,2,0,0;0,0,0,2,0;0,0,0,0,2')
        result = b.get_feature_vector()
        self.assertEquals(result, {'points_scored': 0, 'sum_highest': 15, 'sum_height_diffs': 4, 'hole_num': 10})

        b = board.Board(data='0,0,0,0,0;0,0,0,0,0;2,2,2,2,2;2,0,2,0,2;2,2,2,2,2')
        result = b.get_feature_vector()
        self.assertEquals(result, {'points_scored': 2, 'sum_highest': 15, 'sum_height_diffs': 0, 'hole_num': 2})

        b = board.Board(data='2,0,0,2,0;0,0,0,0,0;0,0,0,0,0;0,0,0,0,0;0,0,0,0,0')
        result = b.get_feature_vector()
        self.assertEquals(result, {'points_scored': 0, 'sum_highest': 10, 'sum_height_diffs': 15, 'hole_num': 0})

        b = board.Board(data='0,0,0,0,0;0,0,0,0,0;0,0,0,0,0;2,2,2,2,2;2,2,0,2,2')
        result = b.get_feature_vector()
        self.assertEquals(result, {'points_scored': 1, 'sum_highest': 10, 'sum_height_diffs': 0, 'hole_num': 1})

        b = board.Board(data='0,0,0,0,0;0,0,0,0,0;0,0,0,0,0;2,2,2,2,2;2,2,0,2,2')
        result = b.get_feature_vector(combo_counter=10)
        self.assertEquals(result, {'points_scored': 11, 'sum_highest': 10, 'sum_height_diffs': 0, 'hole_num': 1})

        b = board.Board(data='0,0,0,0,0;2,2,2,2,2;2,2,2,2,2;2,2,2,2,2;2,2,2,2,2')
        result = b.get_feature_vector()
        self.assertEquals(result, {'points_scored': 8, 'sum_highest': 20, 'sum_height_diffs': 0, 'hole_num': 0})


def almostEquals(num1, num2, tolerance):
    return abs(num1 - num2) < tolerance

class test_genetic_alg(unittest.TestCase):
    def test_magnitude(self):
        feature_vector = {1:0.0, 2:0.0}
        self.assertTrue(almostEquals(genetic_alg.magnitude(feature_vector), 0.0, .000001))

        feature_vector = {1:3.0, 2:4.0}
        self.assertTrue(almostEquals(genetic_alg.magnitude(feature_vector), 5.0, .000001))

        feature_vector = {1:3.0, 2:4.0, 3:5.0}
        self.assertTrue(almostEquals(genetic_alg.magnitude(feature_vector), 7.0710678118654755, .000001))

    def test_normalize(self):
        feature_vector = {1:3.0, 2:4.0}
        normalized = genetic_alg.normalize(feature_vector)
        self.assertTrue(almostEquals(normalized[1], .6, .000001))
        self.assertTrue(almostEquals(normalized[2], .8, .000001))

        feature_vector = {1:3.0, 2:6.0, 3:9.0, 4:12.0}
        normalized = genetic_alg.normalize(feature_vector)
        self.assertTrue(almostEquals(normalized[1], 0.18257418583505536, .000001))
        self.assertTrue(almostEquals(normalized[2], 0.3651483716701107, .000001))
        self.assertTrue(almostEquals(normalized[3], 0.5477225575051661, .000001))
        self.assertTrue(almostEquals(normalized[4], 0.7302967433402214, .000001))

    def test_combine(self):
        mem1 = (4.0, {1:7.0, 2:3.0})
        mem2 = (1.0, {1:2.0, 2:28.0})

        combined = genetic_alg.combine(mem1, mem2)
        self.assertTrue(almostEquals(combined[1], .6, .000001))
        self.assertTrue(almostEquals(combined[2], .8, .000001))

    def test_ga_feature_vectors(self):
        b = genetic_alg.StackerBoard(data='0,0,0,0,0,0;0,0,0,0,0,0;0,0,0,0,0,0;0,0,0,0,0,0;0,0,0,0,0,0;0,0,0,0,0,0')
        result = b.get_feature_vector()
        ans = {'sum_tower_height_diffs': 0, 'sum_tower': 0, 'sum_valley': 0, 'tower_lines': 0, 'hole_tower': 0}
        self.assertEquals(result, ans)

        b = genetic_alg.StackerBoard(data='1,1,1,1,1,1;1,1,1,1,1,1;1,1,1,1,1,1;1,1,1,1,1,1;1,1,1,1,1,1;1,1,1,1,1,1')
        result = b.get_feature_vector()
        self.assertEquals(result, ans)

        b = genetic_alg.StackerBoard(data='0,0,0,0,0,0;0,0,0,0,0,0;0,0,0,0,0,0;2,2,2,2,2,2;2,2,2,2,2,2;2,2,2,2,2,2')
        result = b.get_feature_vector()
        ans = {'sum_tower_height_diffs': 0, 'sum_tower': 9, 'sum_valley': 9, 'tower_lines': 3, 'hole_tower': 0}
        self.assertEquals(result, ans)

        b = genetic_alg.StackerBoard(data='0,0,0,0,0,0;0,0,0,0,0,0;0,0,0,0,0,0;0,0,0,2,2,2;0,0,0,2,0,2;0,0,0,2,2,2')
        result = b.get_feature_vector()
        ans = {'sum_tower_height_diffs': 0, 'sum_tower': 0, 'sum_valley': 9, 'tower_lines': 0, 'hole_tower': 0}
        self.assertEquals(result, ans)

        b = genetic_alg.StackerBoard(data='0,0,0,0,0,0;0,0,0,0,0,0;0,0,0,0,0,0;2,2,2,0,0,0;2,0,2,0,0,0;2,2,2,0,0,0')
        result = b.get_feature_vector()
        ans = {'sum_tower_height_diffs': 0, 'sum_tower': 9, 'sum_valley': 0, 'tower_lines': 2, 'hole_tower': 1}
        self.assertEquals(result, ans)

        b = genetic_alg.StackerBoard(data='0,2,0,2,0,2;2,0,2,0,2,0;0,2,0,2,0,2;2,0,2,0,2,0;0,2,0,2,0,2;2,0,2,0,2,0')
        result = b.get_feature_vector()
        ans = {'sum_tower_height_diffs': 2, 'sum_tower': 16, 'sum_valley': 17, 'tower_lines': 0, 'hole_tower': 7}
        self.assertEquals(result, ans)

if __name__ == '__main__':
    unittest.main()











