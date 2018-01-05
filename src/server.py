import common
import Pyro4

daemon = Pyro4.Daemon()

game = common.Games()

uri = daemon.register(game)
print(uri)

daemon.requestLoop()