import numpy.random
from simulator import SrcNode

class VlbSrcNode(SrcNode):

  def __init__(self, t_line_rate, t_num_dsts):
    SrcNode.__init__(self, t_line_rate, t_num_dsts)
    self.agg_pkt_queue = []

  def tick(self, targets, current_tick):
    assert(len(self.agg_pkt_queue) <= self.line_rate * len(targets));
    for target in numpy.random.permutation(targets):
      if (len(self.agg_pkt_queue) > 0) :
        target.recv(self.agg_pkt_queue.pop(0))
    assert(len(self.agg_pkt_queue) == 0)

  def recv(self, pkt):
    pkt.last_hop = str(self)
    self.agg_pkt_queue.append(pkt)
