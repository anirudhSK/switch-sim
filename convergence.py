#!  /usr/bin/python

# A simulator to study backpressure on leaf-spine topologies
from simulator import *
import sys

# Constants
scheme = sys.argv[1]
numpy.random.seed(int(sys.argv[2]))
NODES = int(sys.argv[3])
LOAD = float(sys.argv[4])
TICKS = int(sys.argv[5])
M = int(sys.argv[6])
LINE_RATE = NODES

# Nodes
# Packet generators
pktgens = [PktGen(t_max_rate = LINE_RATE, t_load = LOAD, t_num_dsts = NODES, t_source = i) for i in range(NODES)]

# Sources
srcs = [SrcNode(t_line_rate = 1, t_num_dsts = NODES, t_scheme = scheme) for i in range(NODES)]

# Spines
spines = [SpineNode(t_line_rate = 1, t_num_dsts = NODES) for i in range(NODES)]

# Destinations
dsts = [DstNode(t_line_rate = LINE_RATE, t_id = i) for i in range(NODES)]

# Simulate
for current_tick in range(1, TICKS + 1):
  for i in range(NODES):
    pktgens[i].tick(srcs[i], current_tick)
  for x in numpy.random.permutation(srcs):
    x.tick(spines, current_tick, backpressure_M = M)
  for x in numpy.random.permutation(spines):
    x.tick(dsts, current_tick)
  for i in range(NODES):
    dsts[i].tick(current_tick)

# Output stats
for i in range(NODES):
  dsts[i].dump_stats()
print "Expected delay according to Karol's 1987 paper", (((NODES - 1) * 1.0) / NODES) * 0.5 * (1.0 / LINE_RATE) * (LOAD / (1 - LOAD))
