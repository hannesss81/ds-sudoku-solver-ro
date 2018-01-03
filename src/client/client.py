import Pyro4

uri = "PYRO:obj_4452f056e2064f1b916c65f155da26a2@localhost:54003"
game = Pyro4.Proxy(uri)

print(game.update_game())