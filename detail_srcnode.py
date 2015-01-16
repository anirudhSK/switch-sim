import numpy.random
from src_node import SrcNode

class DeTailSrcNode(SrcNode):
  PAUSE_THRESHOLD = 5
  RESUME_THRESHOLD = 2
  def __init__(self, t_line_rate, t_num_dsts, t_neighbors):
    SrcNode.__init__(self, t_line_rate, t_num_dsts, t_neighbors)
    self.neighbor_queue = dict()
    for neighbor in self.neighbors:
      self.neighbor_queue[neighbor] = []

  def tick(self, current_tick):
    for neighbor in numpy.random.permutation(self.neighbors):
      for i in range(self.line_rate):
        if ((len(self.neighbor_queue[neighbor]) > 0) and \
            (neighbor.input_counters[self.id] < DeTailSrcNode.RESUME_THRESHOLD)):
          # send packets to neighbor only if:
          # -- have packets for that neighbor
          # -- that neighbor isn't overloaded with your packets
          #    (i.e. your link to the neighbor is not blocked)
          #    (i.e. the neighbor's count of self's packets has fallen
          #     below the resume threshold)
          neighbor.recv(self.neighbor_queue[neighbor].pop(0))

  def recv(self, pkt):
    pkt.last_hop = str(self)
    preferred_neighbors  = []
    for neighbor in self.neighbors:
      if (neighbor.input_counters[self.id] < DeTailSrcNode.PAUSE_THRESHOLD):
        # Adaptive load balancing
        # In practice, this is the sequence of events
        # 1. The neighbor has too many packets from self.
        # 2. The neighbor issues a pause.
        # 3. This causes self to pause its link to neighbor.
        # 4. This causes the self-neighbor link queue to build up.
        # 5. This causes self to move its traffic to other neighbors
        # We hypersimplify by moving traffic to other neighbors
        # as soon as step 1 occurs.
        preferred_neighbors.append(neighbor)

    if (len(preferred_neighbors) > 0):
      chosen = numpy.random.choice(preferred_neighbors) 
      self.neighbor_queue[chosen].append(pkt)
    else:
      chosen = numpy.random.choice(self.neighbors)
      self.neighbor_queue[chosen].append(pkt)
