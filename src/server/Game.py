from lib import sudoku
import Pyro4

latest_game = 0  # Static counter for games (for uniqueness)


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
class Game:
    state = 0

    def __init__(self):
        # self.state = generate_solved_sudoku()
        self.players = {}
        self.id = "GAME" + str(latest_game)

    @Pyro4.expose
    def update_game(self):
        self.state += 1
        return self.state
