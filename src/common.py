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
    # solution = sudoku.generate_grid()
    # game = sudoku.generate_game(solution)
    # state = ''
    # for row in game:
    #     for elem in row:
    #         state += str(elem)
    # solution_str = ""
    # for row in solution:
    #     for elem in row:
    #         solution_str += str(elem)
    # return state, solution_str
    return "state", "solution_str"


@Pyro4.expose
class Games:
    latest_game = 0
    running_games = {}

    def get_games(self):
        return self.running_games

    def get_game_ids(self):
        return ", ".join(str(id) for id in self.running_games.iterkeys())

    def add_game(self):
        state, solution_str = generate_solved_sudoku()
        self.latest_game += 1
        self.running_games[self.latest_game] = {"state": state, "solution": solution_str, "players": []}
        print("Added a new game.")
