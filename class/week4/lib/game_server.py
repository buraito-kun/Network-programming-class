import socket
from threading import Thread
import random
import time

class Game:
  """A roll dice game turn base with 4 players who reach 20 score first win."""
  def __init__(self) -> None:
    self.room_size = 4
    self.connection_pool: list[tuple[socket.socket, tuple[str, int]]] = []
    self.player_score = [0 for i in range(self.room_size)]

  def get_current_connection_count(self) -> int:
    """get current connection count"""
    return len(self.connection_pool)
  
  def join(self, c: socket.socket, conn: tuple[str, int]) -> None:
    """let player join to the room"""
    if len(self.connection_pool) > self.room_size:
      raise Exception("Error room size limit.")
    self.connection_pool.append((c, conn))
    c.send(f"You are player{self.get_current_connection_count()}.".encode())

  def broadcast(self, message: str) -> None:
    """send a message to all clients"""
    for connection in self.connection_pool:
      connection[0].send(message.encode())
  
  def start(self) -> None:
    """start a game"""
    self.broadcast("started")
    while self.check_win_condition() == -1:
      self.get_player_req()
      self.broadcast(",".join([str(_) for _ in self.player_score]))
    time.sleep(1)
    if type(self.check_win_condition()) == int:
      self.broadcast(f"winner:{self.check_win_condition()+1}")
    else:
      self.broadcast(f"""winner:{",".join([str(player_index+1) for player_index in self.check_win_condition()])}""")
    self.close_connection()

  def close_connection(self) -> None:
    """close clients connection"""
    for connection in self.connection_pool:
      connection[0].close()

  def check_win_condition(self) -> int | list[int]:
    """check win condition for player who reach 20 score
    if two more player reach upper or equal to 20 that game will have one more winner"""
    p: list[int] = []
    for index, score in enumerate(self.player_score):
      if score >= 20:
        p.append(index)
    if len(p) == 0:
      return -1
    elif len(p) == 1:
      return p[0]
    else:
      if self.player_score.count(max(self.player_score)) > 1:
        temp: list[int] = []
        for index, score in enumerate(self.player_score):
          if max(self.player_score) == score:
            temp.append(index)
        return temp
      else:
        return p[self.player_score.index(max(self.player_score))]
  
  def get_player_req(self):
    """get player request signal for roll dice"""
    for index, player in enumerate(self.connection_pool):
      player[0].send("your turn".encode())
      if player[0].recv(4096).decode() == "req":
        roll_dice_value = random.randint(1, 6)
        self.player_score[index] += roll_dice_value
        player[0].send(f"{roll_dice_value}".encode())
