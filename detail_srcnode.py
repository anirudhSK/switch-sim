import numpy.random
from src_node import SrcNode

class DeTailSrcNode(SrcNode):
  PAUSE_THRESHOLD = 5
  def __init__(self, t_line_rate, t_num_dsts, t_neighbors):
    SrcNode.__init__(self, t_line_rate, t_num_dsts, t_neighbors)
    self.neighbor_queue = dict()
    for neighbor in self.neighbors:
      self.neighbor_queue[neighbor] = []

  def tick(self, current_tick):
    for neighbor in numpy.random.permutation(self.neighbors):
      if ((len(self.neighbor_queue[neighbor]) > 0) and (neighbor.input_counters[self.id] < DeTailSrcNode.PAUSE_THRESHOLD)):
        neighbor.recv(self.neighbor_queue[neighbor].pop(0))

  def recv(self, pkt):
    pkt.last_hop = str(self)
    preferred_neighbors  = []
    for neighbor in self.neighbors:
      if (neighbor.input_counters[self.id] < DeTailSrcNode.PAUSE_THRESHOLD):
        # Cheat (no pause messages)
        preferred_neighbors.append(neighbor)

    if (len(preferred_neighbors) > 0):
      chosen = numpy.random.choice(preferred_neighbors) 
      self.neighbor_queue[chosen].append(pkt)
    else:
      chosen = numpy.random.choice(self.neighbors)
      self.neighbor_queue[chosen].append(pkt)
