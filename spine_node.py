import numpy.random
class SpineNode:

  object_count = 0

  def __str__(self):
    return "spine"+str(self.id) if self.name == "" else self.name

  def __init__(self, t_line_rate, t_num_dsts, t_neighbors, t_name = ""):
    assert(isinstance(t_line_rate, int))
    self.line_rate = t_line_rate
    self.pkt_queue = []
    self.id = SpineNode.object_count
    self.name = t_name
    SpineNode.object_count += 1
    for i in range(t_num_dsts):
      self.pkt_queue.append([])
    self.neighbors = t_neighbors

  def tick(self, current_tick):
    for neighbor in numpy.random.permutation(self.neighbors):
      # No choice, only one path to neighbor
      for i in range(min(self.line_rate, len(self.pkt_queue[neighbor.get_id()]))):
        neighbor.recv(self.pkt_queue[neighbor.get_id()].pop(0))

  def recv(self, pkt):
    pkt.last_hop = str(self)
    self.pkt_queue[pkt.dst].append(pkt)

  def modify_line_rate(self, new_line_rate):
    self.line_rate = new_line_rate
