
from sys import stderr, stdin, stdout

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


    def choose_action(self, args):
        return 'left,right,right,left,drop'


if __name__ == '__main__':
    Bot().run()
