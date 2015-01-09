class SrcNode:

  object_count = 0

  def __str__(self):
    return "leaf"+str(self.id)

  def __init__(self, t_line_rate, t_num_dsts, t_neighbors):
    assert(isinstance(t_line_rate, int))
    self.line_rate = t_line_rate
    self.id = SrcNode.object_count
    SrcNode.object_count += 1
    self.neighbors = t_neighbors
