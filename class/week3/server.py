# Standard library
import socket

# Project library
from lib.game_server import RockPaperScissor
from lib.my_thread import Thread

def create_game_room(room):
  global require_new_room
  require_new_room = False
  
  while len(room.connection_pool) < 2:
    c, conn = s.accept()
    room.join([c, conn])

  require_new_room = True
  Thread(room.start, None).start()
  # delete game room
  del room

PORT = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", PORT))

s.listen(5)

require_new_room = True

if __name__ == "__main__":
  while True:
    if require_new_room:
      Thread(create_game_room, RockPaperScissor()).start()
      require_new_room = False
