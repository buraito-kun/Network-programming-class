import socket
import threading
from lib.game_server import Game

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 12345))
s.listen(5)

while True:
  game_room = Game()
  while game_room.get_current_connection_count() < 4:
    c, conn = s.accept()
    game_room.join(c, conn)
  threading.Thread(target=game_room.start).start()
