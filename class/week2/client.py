# Standard library
import socket

PORT = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("localhost", PORT))

choices_pool = ["rock", "paper", "scissor"]

while True:
  try:
    player_action = input("""
    Type 1, 2 or 3
      1: (rock)
      2: (paper)
      3: (scissor)

> """)
    int(player_action)
    if int(player_action) <= 0 and int(player_action) >= 4:
      raise Exception("Error: specify value not in range 1-3.")
    break
  except:
    pass

s.send(str(choices_pool[int(player_action)-1]).encode())
print("Opponent is thinking...")
data = s.recv(4096).decode()
if data == "draw":
  print("Draw.")
  print("Game ended.")
elif data == "won":
  print("You won!")
  print("Game ended.")
elif data == "lose":
  print("You lose!")
  print("Game ended.")

s.close()