import numpy.random
from spine_node import SpineNode

class DeTailSpineNode(SpineNode):
  def __init__(self, t_line_rate, t_num_dsts, t_neighbors, t_name = ""):
    SpineNode.__init__(self, t_line_rate, t_num_dsts, t_neighbors, t_name)
    # occupancy of each input counter across all queues
    # used to signal pause
    self.input_counters = []
    assert (len(t_neighbors) == t_num_dsts)
    num_srcs = t_num_dsts
    # XXX: Fix above, works on leaf-spine for now
    for i in range(num_srcs):
      self.input_counters.append(0)

  def tick(self, current_tick):
    for neighbor in numpy.random.permutation(self.neighbors):
      # No choice, only one path to neighbor
      for i in range(min(self.line_rate, len(self.pkt_queue[neighbor.get_id()]))):
        next_pkt = self.pkt_queue[neighbor.get_id()].pop(0)
        neighbor.recv(next_pkt)
        self.input_counters[next_pkt.src] -= 1

  def recv(self, pkt):
    pkt.last_hop = str(self)
    self.pkt_queue[pkt.dst].append(pkt)
    self.input_counters[pkt.src] += 1
