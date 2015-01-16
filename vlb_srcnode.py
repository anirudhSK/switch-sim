import numpy.random
from src_node import SrcNode

class VlbSrcNode(SrcNode):

  def __init__(self, t_line_rate, t_num_dsts, t_neighbors):
    SrcNode.__init__(self, t_line_rate, t_num_dsts, t_neighbors)
    self.agg_pkt_queue = []

  def tick(self, current_tick):
    assert(len(self.agg_pkt_queue) <= self.line_rate * len(self.neighbors));
    for neighbor in numpy.random.permutation(self.neighbors):
      for i in range(self.line_rate):
        if (len(self.agg_pkt_queue) > 0) :
          neighbor.recv(self.agg_pkt_queue.pop(0))
    assert(len(self.agg_pkt_queue) == 0)

  def recv(self, pkt):
    pkt.last_hop = str(self)
    self.agg_pkt_queue.append(pkt)
