import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 12345))
your_player = s.recv(4096).decode()
print(your_player)
your_player = your_player.replace("You are player", "").replace(".", "")

while True:
  data = s.recv(4096).decode()
  if data == "your turn":
    input("Press enter to roll dice.")
    s.send("req".encode())
    dice_value = s.recv(4096).decode()
    print("You rolled", dice_value)
    all_player_score = s.recv(4096).decode().split(",")
    print("Current player score")
    for index, score in enumerate(all_player_score):
      print(f"Player{index+1}: {score}")
  if data.startswith("winner:"):
    if your_player in data.split(":")[1].split(","):
      print("You won!")
    else:
      print("You lose!")
    break
  if data == "started":
    print("Game started.")
s.close()
