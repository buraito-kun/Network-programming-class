# Standard library
import socket

# Project library
from lib.game_server import RockPaperScissor

PORT = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", PORT))

s.listen(5)

choices_pool = ["rock", "paper", "scissor"]

while True:
  c, conn = s.accept()
  game_room = RockPaperScissor()
  player_action = c.recv(4096).decode()
  while True:
    try:
      server_action = input("""\n    Type 1, 2 or 3\n      1: (rock)\n      2: (paper)\n      3: (scissor)\n\n> """)
      int(server_action)
      if int(server_action) <= 0 and int(server_action) >= 4:
        raise Exception("Error: specify value not in range 1-3.")
      break
    except:
      pass
  game_room.player1_action = choices_pool[int(server_action)-1]
  game_room.player2_action = player_action
  compare_result = game_room.check_win_condition(game_room.player1_action, game_room.player2_action)
  if compare_result == "won":
    c.send("lose".encode())
  elif compare_result == "lose":
    c.send("won".encode())
  elif compare_result == "draw":
    c.send("draw".encode())

  print("something", compare_result)
  if compare_result == "draw":
    print("Draw.")
    print("Game ended.")
  elif compare_result == "won":
    print("You won!")
    print("Game ended.")
  elif compare_result == "lose":
    print("You lose!")
    print("Game ended.")