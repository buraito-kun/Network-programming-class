# Standard library
import threading

class Thread(threading.Thread):
  def __init__(self, func, args):
    super().__init__()
    self.func = func
    self.args = args

  def run(self):
    try:
      self.func(self.args)
    except:
      self.func()
