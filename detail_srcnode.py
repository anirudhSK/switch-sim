import numpy.random
from src_node import SrcNode

class DeTailSrcNode(SrcNode):
  def __init__(self, t_line_rate, t_num_dsts, t_neighbors, \
               pause_threshold = 5, resume_threshold = 2, load_balance_threshold = 10):
    SrcNode.__init__(self, t_line_rate, t_num_dsts, t_neighbors)
    self.neighbor_queue = dict()
    self.pause_threshold = pause_threshold
    self.resume_threshold = resume_threshold
    self.load_balance_threshold = load_balance_threshold
    self.paused = dict()
    assert(self.resume_threshold <= self.pause_threshold)
    for neighbor in self.neighbors:
      self.neighbor_queue[neighbor] = []
      self.paused[neighbor] = False

  def tick(self, current_tick):
    # Pause logic
    for neighbor in (self.neighbors):
      # If link was paused and it now hit the resume threshold
      if ((neighbor.input_counters[self.id] <= self.resume_threshold) and \
          self.paused[neighbor]):
        self.paused[neighbor] = False
      # If link was not paused and it now hit pause threshold
      elif ((neighbor.input_counters[self.id] >= self.pause_threshold) and \
          (not self.paused[neighbor])):
        self.paused[neighbor] = True

    # Transmit packets on unpaused links
    for neighbor in numpy.random.permutation(self.neighbors):
      for i in range(self.line_rate):
        if ((len(self.neighbor_queue[neighbor]) > 0) and (not self.paused[neighbor])):
          neighbor.recv(self.neighbor_queue[neighbor].pop(0))

  def recv(self, pkt):
    pkt.last_hop = str(self)
    preferred_neighbors  = []
    for neighbor in self.neighbors:
      if (len(self.neighbor_queue[neighbor]) < self.load_balance_threshold):
        preferred_neighbors.append(neighbor)

    if (len(preferred_neighbors) > 0):
      chosen = numpy.random.choice(preferred_neighbors) 
      self.neighbor_queue[chosen].append(pkt)
    else:
      chosen = numpy.random.choice(self.neighbors)
      self.neighbor_queue[chosen].append(pkt)
