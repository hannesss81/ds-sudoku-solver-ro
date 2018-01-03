from Game import Game
import Pyro4

daemon = Pyro4.Daemon()

game = Game()

uri = daemon.register(game)
print(uri)
daemon.requestLoop()