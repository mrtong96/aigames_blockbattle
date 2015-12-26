
from sys import stderr, stdin, stdout
import board
import piece
import json
import util
import time

class Bot(object):

    def __init__(self):
        self.settings = {}
        self.game_settings = {}
        self.game_settings['game'] = {}
        self.game_settings['player1'] = {}
        self.game_settings['player2'] = {}

        # for the AI, may need to fool around with weights a bit...
        self.last_position = None
        self.WEIGHT_VECTOR = {'points_scored': .760666, 'sum_highest': -.510066,\
            'sum_height_diffs': -.184483, 'hole_num': -.35663}
        # commital to strategy in previous move. To get the bot to try to stick to one plan
        self.stubbornness = 1.5

    def run(self):
        while not stdin.closed:
            try:
                rawline = stdin.readline()

                if len(rawline) == 0:
                    break

                line = rawline.strip()

                if len(line) == 0:
                    continue

                parts = line.split()
                command = parts[0]

                if command == 'settings':
                    self.update_settings(parts[1:])
                elif command == 'update':
                    self.update_game_settings(parts[1:])
                elif command == 'action':
                    out = self.choose_action(parts[1:]) + '\n'
                    stdout.write(out)
                    stdout.flush()
                else:
                    stderr.write('Unknown command: %s\n' % (command))
                    stdout.flush()
            except Exception as e:
                stderr.write('Error reading lines: {}\n'.format(e))
                stdout.flush()
                return 


    def update_settings(self, args):
        if len(args) > 2:
            self.settings[args[0]] = args[1:]
        else:
            self.settings[args[0]] = args[1]


    def update_game_settings(self, args):
        if args[0] == 'game':
            if len(args) > 3:
                self.game_settings[args[0]][args[1]] = args[2:]
            else:
                self.game_settings[args[0]][args[1]] = args[2]
        else:
            if len(args) > 3:
                self.game_settings[args[0]][args[1]] = args[2:]
            else:
                self.game_settings[args[0]][args[1]] = args[2]

    # TODO: rebuild this
    def choose_action(self, args=None):
        t0 = time.time()
        # time given to the algorithm to find the best move. Can change later
        time_given = min(.001 * float(args[1]), 1.0)

        bot_name = self.settings['your_bot']
        b = board.Board(data=self.game_settings[bot_name]['field'])
        bot_combo = int(self.game_settings[bot_name]['combo'])

        piece1 = self.game_settings['game']['this_piece_type']
        piece2 = self.game_settings['game']['next_piece_type']

        feature_vectors = []
        for pos in b.get_valid_positions(piece1):
            b.place_piece(*pos)
            feature_vector = b.get_feature_vector(combo_counter=bot_combo)
            value = multiply_feature_vectors(feature_vector, self.WEIGHT_VECTOR)
            if pos == self.last_position:
                value += self.stubbornness
            feature_vectors.append((pos, value))
            b.remove_piece(*pos)

        feature_vectors.sort(key=lambda x: - x[1])

        # go through various possible positions to depth 2
        # if < 55 ms left, break

        # Check last intended move for depth 2, if new depth1 search returns different depth 2 pos, add
        # penalty to changing it.

        depth2_pos_list = []

        test_depth2 = 0

        for pos1 in b.get_valid_positions(piece1):
            # if piece unreachable, break
            if not self.get_path(b, pos1):
                break

            # given 55 ms to safely finish up
            if time.time() - t0 > time_given - .085:
                break

            depth2_values = []
            b.place_piece(*pos1)

            detph2_valid_positions = b.get_valid_positions(piece2)
            for pos2 in detph2_valid_positions:
                b.place_piece(*pos2)
                feature_vector = b.get_feature_vector(combo_counter=bot_combo)
                value = multiply_feature_vectors(feature_vector, self.WEIGHT_VECTOR)
                if pos1 == self.last_position:
                    value += self.stubbornness
                depth2_values.append(value)

                b.remove_piece(*pos2)

            depth2_data = zip(detph2_valid_positions, depth2_values)
            depth2_data.sort(key=lambda x: -x[1])

            for data in depth2_data:
                if not self.get_path(b, data[0]):
                    continue
                else:
                    depth2_pos_list.append((pos1, data[1], data[0]))
                    break

            b.remove_piece(*pos1)

            test_depth2 += 1
        
        #print 'nodes expanded: {}'.format(test_depth2)

        depth2_pos_list.sort(key=lambda x: -x[1])
        new_position_order, _, depth2_pos_list = zip(*depth2_pos_list)

        positions, _ = zip(*feature_vectors)
        positions = new_position_order + positions[len(new_position_order):]

        for pos in positions:
            path = self.get_path(b, pos)

            if not path:
                #print ':no path:'
                continue

            #print 'time taken: {}'.format(1000 * (time.time() - t0))
            self.last_position = pos
            return ','.join(path)

    # determines if it's possible for the piece to move to that location
    def get_path(self, board, pos):
        end_piece = pos[0]
        end_loc = (pos[1], pos[2])

        piece1 = self.game_settings['game']['this_piece_type']
        start_piece = piece.Piece(piece1)
        start_loc = self.game_settings['game']['this_piece_position']
        start_loc = eval('(' + start_loc + ')')

        return board.get_path(start_piece, start_loc, end_piece, end_loc)

def multiply_feature_vectors(vector1, vector2):
    return sum(map(lambda x: vector1[x] * vector2[x], vector1.keys()))

if __name__ == '__main__':
    Bot().run()
