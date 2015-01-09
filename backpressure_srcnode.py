import numpy.random
from simulator import SrcNode

class BackPressureSrcNode(SrcNode):

  def __init__(self, t_line_rate, t_num_dsts, backpressure_M):
    SrcNode.__init__(self, t_line_rate, t_num_dsts)
    self.pkt_queue = []
    self.backpressure_M = backpressure_M
    for i in range(0, t_num_dsts):
      self.pkt_queue.append([])

  def tick(self, targets, current_tick):
    for target in numpy.random.permutation(targets):
      # Find destination with maximum backpressure
      max_backpressure = -sys.maxint - 1
      argmax_list = []
      for dst_id in range(len(self.pkt_queue)):
        backpressure = len(self.pkt_queue[dst_id]) - len(target.pkt_queue[dst_id])
        if (backpressure > max_backpressure) :
          max_backpressure = backpressure
          argmax_list = [dst_id]
        elif (backpressure == max_backpressure):
          argmax_list += [dst_id]

      # Break ties randomly
      argmax = numpy.random.choice(argmax_list)

      if (max_backpressure >= self.backpressure_M):
        assert(backpressure_M <= 0 or len(target.pkt_queue[argmax]) < len(self.pkt_queue[argmax]))
        for i in range(min(len(self.pkt_queue[argmax]), self.line_rate)):
          target.recv(self.pkt_queue[argmax].pop(0))

  def recv(self, pkt):
    pkt.last_hop = str(self)
    self.pkt_queue[pkt.dst].append(pkt)
