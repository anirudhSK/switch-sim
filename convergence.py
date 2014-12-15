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
  def tick(self, targets):
    # Generate packets
    for j in range(0, numpy.random.binomial(self.line_rate, self.arrival_rate)):
      self.pkt_queue.append((current_tick, 0))

    # Transfer based on backpressure
    backpressures = [(target, len(self.pkt_queue) - target.get_queue_size()) for target in targets if (len(self.pkt_queue) - target.get_queue_size() > 0)]
    if (len(backpressures) > 0) :
      picked_queue = max(backpressures)[0]
      print "Picking ", picked_queue
      assert(picked_queue.get_queue_size() < len(self.pkt_queue))
      picked_queue.recv(self.pkt_queue.pop(0))

class WayPointNode:
  def __init__(self):
    self.pkt_queue = []
  def tick(self, targets):
    print "WayPointNode ticking"
  def get_queue_size(self):
    return len(self.pkt_queue)
  def recv(self, pkt):
    self.pkt_queue.append(pkt)

class DstNode:
  def tick(self, targets):
    print "DstNode ticking"

LINE_RATE = 2
ARRIVAL_RATE = 0.8
srcnode = SrcNode(LINE_RATE, ARRIVAL_RATE)
waypoint1 = WayPointNode()
waypoint2 = WayPointNode()
dstnode = DstNode()
TICKS = 1000000

for current_tick in range(0, TICKS):
  srcnode.tick([waypoint1, waypoint2])
  waypoint1.tick([dstnode])
  waypoint2.tick([dstnode])
  dstnode.tick([])
