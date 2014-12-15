#!  /usr/bin/python

# A simulator to contrast the convergence of backpressure and CONGA

# Here's the setup:
#        waypoint1
#        /        \
#       /          \
#      /            \
#  srcnode        dstnode
#      \            /
#       \          /
#        \        /
#        waypoint2
#
import numpy.random
import numpy

class SrcNode:

  def __init__(self, t_line_rate, t_arrival_rate):
    self.line_rate = t_line_rate
    self.arrival_rate = t_arrival_rate
    self.pkt_queue = []

  def tick(self, targets, current_tick):
    # Generate packets
    for j in range(0, numpy.random.binomial(self.line_rate, self.arrival_rate)):
      self.pkt_queue.append((current_tick, 0))

    # Transfer based on backpressure to destination on each of the links
    # Since there is only one destination, this is trivial
    for target in numpy.random.permutation(targets):
      backpressure = len(self.pkt_queue) - target.get_queue_size()
      if (backpressure > 0) :
        print "Picking ", target
        assert(target.get_queue_size() < len(self.pkt_queue))
        target.recv(self.pkt_queue.pop(0))

class WayPointNode:

  def __init__(self, t_line_rate, t_id):
    self.id = t_id
    self.line_rate = t_line_rate
    self.pkt_queue = []

  def tick(self, targets):
    assert(len(targets) == 1)
    for i in range(self.line_rate):
      if (len(self.pkt_queue) > 0):
        targets[0].recv(self.pkt_queue.pop(0))

  def get_queue_size(self):
    return len(self.pkt_queue)

  def recv(self, pkt):
    self.pkt_queue.append(pkt)

  def modify_line_rate(self, new_line_rate):
    self.line_rate = new_line_rate

  def get_id(self):
    return self.id

class DstNode:

  def __init__(self, t_line_rate):
    self.line_rate = t_line_rate
    self.pkt_queue = []

  def recv(self, pkt):
    self.pkt_queue.append(pkt)

  def tick(self, targets):
    for i in range(min(self.line_rate, len(self.pkt_queue))):
      self.pkt_queue.pop(0)

LINE_RATE = 2
ARRIVAL_RATE = 0.5
srcnode = SrcNode(LINE_RATE, ARRIVAL_RATE)
waypoint1 = WayPointNode(1, 1)
waypoint2 = WayPointNode(1, 2)
dstnode = DstNode(LINE_RATE)
TICKS = 1000000

for current_tick in range(0, TICKS):
  srcnode.tick([waypoint1, waypoint2], current_tick)
  waypoint1.tick([dstnode])
  waypoint2.tick([dstnode])
  dstnode.tick([])
