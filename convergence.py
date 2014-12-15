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

class SrcNode:  
  def tick(self, targets):
    print "SrcNode ticking"

class WayPointNode:
  def tick(self, targets):
    print "WayPointNode ticking"

class DstNode:
  def tick(self, targets):
    print "DstNode ticking"

srcnode = SrcNode()
waypoint1 = WayPointNode()
waypoint2 = WayPointNode()
dstnode = DstNode()
TICKS = 1000000

for current_tick in range(0, TICKS):
  srcnode.tick([waypoint1, waypoint2])
  waypoint1.tick([dstnode])
  waypoint2.tick([dstnode])
  dstnode.tick([])
