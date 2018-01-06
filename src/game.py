from lib import sudoku
import Pyro4

latest_game = 0  # Static counter for games (for uniqueness)

BUFFER_SIZE = 1024

## List of common keywords that are used for communicating.

JOIN_GAME = 'join'
LIST_GAMES = 'list'
CREATE_GAME = 'create'
DONE = 'done'
JOIN_OK = 'join_ok'
GAME_STATE = 'game_state'
NEW_GUESS = 'new_guess'
WIN = 'msg'


def generate_solved_sudoku():
    solution = sudoku.generate_grid()
    game = sudoku.generate_game(solution)
    state = ''
    for row in game:
        for elem in row:
            state += str(elem)
    solution_str = ""
    for row in solution:
        for elem in row:
            solution_str += str(elem)
    return state, solution_str


@Pyro4.expose
class Games:  ## Allows Pyro to manage this object over all hosts.
    latest_game = 0
    running_games = {}

    def get_games(self):
        return self.running_games

    def get_game_ids(self):
        return ", ".join(str(id) for id in self.running_games.iterkeys())

    def add_game(self):
        state, solution_str = generate_solved_sudoku()
        self.latest_game += 1
        self.running_games["GAME" + str(self.latest_game)] = {"state": (state, solution_str), "players": {}}
        print("Added a new game.")

    def join(self, nickname, game_id):
        print(self.running_games)
        print(nickname, game_id)
        self.running_games[game_id]["players"][nickname] = 0
        return JOIN_OK

    def request_game_data(self, game_id):
        is_over = False
        return is_over, self.running_games[game_id]

    def new_guess(self, guess, game_id, nickname):
        print("New guess: " + str(guess), game_id, nickname)

        game = self.running_games[game_id]

        x, y, guess = list(guess)
        print(x, y, guess)
        if self.check_match(x, y, guess, game):
            game["players"][nickname] = game["players"][nickname] + 1
            index = 9 * int(x) + int(y)
            modified_game_state = (game["state"][0][:index] + guess + game["state"][0][index + 1:], game["state"][1])
            game["state"] = modified_game_state
        else:
            game["players"][nickname] = game["players"][nickname] - 1
        if game["state"][0] == game["state"][1]:
            current_winner = ""
            name = ""
            current_max = -999999
            for name, score in game["players"].iteritems():
                if current_max < score:
                    current_winner = name
                    current_max = score
            print("Winner: " + str(name) + ", score: " + str(score))
        self.running_games[game_id] = game

    def check_match(self, x, y, guess, game):
        correct = game["state"][1]
        print(correct)
        print(guess)
        if correct[9 * int(x) + int(y)] == guess:
            return True
        return False
