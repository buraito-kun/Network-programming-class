# Project library
from lib.my_thread import Thread

class RockPaperScissor:
  """A Rock Paper Scissor online game."""
  
  def __init__(self):
    self.is_started = False
    self.connection_pool = []
    self.player1_action = ""
    self.player2_action = ""
  
  def join(self, connection):
    """join player connection"""
    self.connection_pool.append(connection)
    
    # send state to client
    if len(self.connection_pool) == 1:
      self.connection_pool[0][0].send("waiting".encode())
    elif len(self.connection_pool) == 2:
      self.connection_pool[0][0].send("ready".encode())
      self.connection_pool[1][0].send("ready".encode())
    
    # validation
    if len(self.connection_pool) > 2:
      raise Exception("Error: connection pool limit.")
  
  def player_action(self):
    """player action handler"""
    player1 = Thread(self.action, 1)
    player2 = Thread(self.action, 2)
    player1.start()
    player2.start()
    while True:
      if player1.is_alive() or player2.is_alive():
        continue
      break
    self.connection_pool[0][0].send("finish".encode())
    self.connection_pool[1][0].send("finish".encode())

  def action(self, player_index):
    """get player action"""
    __action = ""
    while True:
      __action = self.connection_pool[player_index-1][0].recv(4096).decode()
      if __action not in ["rock", "paper", "scissor"]:
        continue
      break
  
    # set player action to global variable
    if player_index == 1:
      self.player1_action = __action
    elif player_index == 2:
      self.player2_action = __action

  def check_win_condition(self, p1_action, p2_action):
    """return is player 1 won, lose or draw"""
    # clear player action
    self.player1_action = ""
    self.player2_action = ""
    if p1_action == p2_action:
      # draw
      return "draw"
    elif p1_action == "rock" and p2_action == "scissor":
      # player1 won
      return "won"
    elif p1_action == "rock" and p2_action == "paper":
      # player1 lose
      return "lose"
    elif p1_action == "paper" and p2_action == "scissor":
      # player1 lose
      return "lose"
    elif p1_action == "paper" and p2_action == "rock":
      # player1 won
      return "won"
    elif p1_action == "scissor" and p2_action == "rock":
      # player1 lose
      return "lose"
    elif p1_action == "scissor" and p2_action == "paper":
      # player1 won
      return "won"

  def start(self):
    self.is_started = True
    self.player_action()
    compare_result = self.check_win_condition(self.player1_action, self.player2_action)
    if compare_result == "won":
      self.connection_pool[0][0].send("won".encode())
      self.connection_pool[1][0].send("lose".encode())
    elif compare_result == "lose":
      self.connection_pool[0][0].send("lose".encode())
      self.connection_pool[1][0].send("won".encode())
    elif compare_result == "draw":
      self.connection_pool[0][0].send("draw".encode())
      self.connection_pool[1][0].send("draw".encode())

    self.connection_pool[0][0].close()
    self.connection_pool[1][0].close()
    self.is_started = False
