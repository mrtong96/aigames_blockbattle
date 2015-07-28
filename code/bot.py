
from sys import stderr, stdin, stdout
import board
import piece
import json
import util

class Bot(object):


    def __init__(self):
        self.settings = {}
        self.game_settings = {}
        self.game_settings['game'] = {}
        self.game_settings['player1'] = {}
        self.game_settings['player2'] = {}


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

    def choose_action(self, args=None):
        bot_name = self.settings['your_bot']
        b = board.Board(data=self.game_settings[bot_name]['field'])

        piece1 = self.game_settings['game']['this_piece_type']
        piece2 = self.game_settings['game']['next_piece_type']

        feature_vectors = []
        for pos in b.get_valid_positions(piece1):
            b.place_piece(*pos)
            feature_vectors.append((pos, b.get_feature_vector()))
            b.remove_piece(*pos)

        feature_vectors.sort(key=lambda x: - util.multiply_feature_vectors(x[1], WEIGHT_VECTOR))

        path = []

        for pos in feature_vectors:
            best_valid_pos = pos[0]

            end_piece = best_valid_pos[0]
            end_loc = (best_valid_pos[1], best_valid_pos[2])

            start_piece = piece.Piece(piece1)
            start_loc = self.game_settings['game']['this_piece_position']
            start_loc = eval('(' + start_loc + ')')

            path = b.get_path(start_piece, start_loc, end_piece, end_loc)

            if not path:
                continue

            b.place_piece(*best_valid_pos)

            return ','.join(path)


WEIGHT_VECTOR = {'solid_lines': .760666, 'sum_highest': -.510066,\
    'sum_height_diffs': -.184483, 'hole_num': -.35663}


if __name__ == '__main__':
    Bot().run()
