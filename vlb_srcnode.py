import numpy.random
from src_node import SrcNode

class VlbSrcNode(SrcNode):

  def __init__(self, t_line_rate, t_num_dsts, t_neighbors):
    SrcNode.__init__(self, t_line_rate, t_num_dsts, t_neighbors)
    self.neighbor_queue = dict()
    for neighbor in self.neighbors:
      self.neighbor_queue[neighbor] = []

  def tick(self, current_tick):
    for neighbor in numpy.random.permutation(self.neighbors):
      for i in range(self.line_rate):
        if (len(self.neighbor_queue[neighbor]) > 0) :
          neighbor.recv(self.neighbor_queue[neighbor].pop(0))

  def recv(self, pkt):
    pkt.last_hop = str(self)
    chosen = numpy.random.choice(self.neighbors)
    self.neighbor_queue[chosen].append(pkt)
