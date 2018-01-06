import game, Pyro4, socket, struct, threading, time

## Using multicast, will send it's URI out every 1.0 seconds.
def cast_uri(uri):
    while True:
        multicast_group = ('224.0.0.1', 6666)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ttl = struct.pack('b', 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        sock.sendto(str(uri), multicast_group)
        time.sleep(1)

daemon = Pyro4.Daemon()
game = game.Games()

uri = daemon.register(game) ## Registers the Games() object to the Pyro daemon.
print("Uri: " + str(uri))

thread = threading.Thread(target=cast_uri, args=[uri])
thread.start()

daemon.requestLoop()