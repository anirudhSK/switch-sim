#!  /usr/bin/python

# A simulator to contrast the convergence of backpressure and CONGA

# Here's the setup:
#           spine1
#    src1            dst1
#           spine2
import numpy.random
import numpy

class SrcNode:

  def __init__(self, t_line_rate, t_arrival_rate):
    self.line_rate = t_line_rate
    self.arrival_rate = t_arrival_rate
    self.pkt_queue = []

  def tick(self, targets, current_tick, dsts):
    # Generate packets
    for j in range(0, numpy.random.binomial(self.line_rate, self.arrival_rate)):
      self.pkt_queue.append((current_tick, numpy.random.choice(dsts).get_id()))

    # Transfer based on backpressure to destination on each of the links
    # Since there is only one destination, this is trivial
    for target in numpy.random.permutation(targets):
      backpressure = len(self.pkt_queue) - target.get_queue_size()
      if (backpressure > 0) :
        print "Picking ", target
        assert(target.get_queue_size() < len(self.pkt_queue))
        target.recv(self.pkt_queue.pop(0), current_tick)

class SpineNode:

  def __init__(self, t_line_rate, t_id):
    self.id = t_id
    self.line_rate = t_line_rate
    self.pkt_queue = []

  def tick(self, targets, current_tick):
    assert(len(targets) == 1)
    for i in range(self.line_rate):
      if (len(self.pkt_queue) > 0):
        targets[0].recv(self.pkt_queue.pop(0), current_tick)

  def get_queue_size(self):
    return len(self.pkt_queue)

  def recv(self, pkt, current_tick):
    self.pkt_queue.append(pkt)

  def modify_line_rate(self, new_line_rate):
    self.line_rate = new_line_rate

  def get_id(self):
    return self.id

class DstNode:

  def __init__(self, t_line_rate, t_id):
    self.line_rate = t_line_rate
    self.pkt_queue = []
    self.id = t_id

  def recv(self, pkt, current_tick):
    assert(pkt[1] == self.id)
    self.pkt_queue.append(pkt)

  def tick(self, targets, current_tick):
    for i in range(min(self.line_rate, len(self.pkt_queue))):
      self.pkt_queue.pop(0)

  def get_id(self):
    return self.id

LINE_RATE = 2
ARRIVAL_RATE = 0.5
src1 = SrcNode(LINE_RATE, ARRIVAL_RATE)
spine1 = SpineNode(1, 1)
spine2 = SpineNode(1, 2)
dst1 = DstNode(LINE_RATE, 1)
TICKS = 1000000

for current_tick in range(0, TICKS):
  src1.tick([spine1, spine2], current_tick, [dst1])
  spine1.tick([dst1], current_tick)
  spine2.tick([dst1], current_tick)
  dst1.tick([], current_tick)
  if (current_tick == TICKS / 2):
    print "Modified line rate for spine1"
    spine1.modify_line_rate(0)
