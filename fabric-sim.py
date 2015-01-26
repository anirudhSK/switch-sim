#!  /usr/bin/python

# A simulator to study fabric load balancing
from pkt_gen import PktGen
from dst_node import DstNode
from spine_node import SpineNode
from detail_spinenode import DeTailSpineNode
from vlb_srcnode import VlbSrcNode
from backpressure_srcnode import BackPressureSrcNode
from detail_srcnode import DeTailSrcNode
import numpy.random
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
# Destinations
dsts = [DstNode(t_line_rate = 2 * LINE_RATE, t_id = i) for i in range(NODES)]

# Spines
spines = []
if (scheme == "vlb" or scheme == "backpressure"):
  spines = [SpineNode(t_line_rate = 2, t_num_dsts = NODES, t_neighbors = dsts) for i in range(NODES)]
elif (scheme == "detail"):
  spines = [DeTailSpineNode(t_line_rate = 2, t_num_dsts = NODES, t_neighbors = dsts) for i in range(NODES)]
else:
  assert(False)

# Sources
srcs = []
if (scheme == "vlb"):
  srcs = [VlbSrcNode(t_line_rate = 2, t_num_dsts = NODES, t_neighbors = spines) for i in range(NODES)]
elif (scheme == "backpressure"):
  srcs = [BackPressureSrcNode(t_line_rate = 2, t_num_dsts = NODES, t_neighbors = spines, backpressure_M = M) for i in range(NODES)]
elif (scheme == "detail"):
  srcs = [DeTailSrcNode(t_line_rate = 2, t_num_dsts = NODES, t_neighbors = spines, pause_threshold = int(sys.argv[7]), resume_threshold = int(sys.argv[8]), load_balance_threshold = int(sys.argv[9])) for i in range(NODES)]
else:
  assert(False)

# Packet generators
pktgens = [PktGen(t_line_rate = 2 * LINE_RATE, t_load = LOAD, t_num_dsts = NODES, t_source = i, t_neighbors = [srcs[i]]) for i in range(NODES)]

# Simulate asymmetry to one destination alone
spines[NODES - 1].modify_line_rate(new_line_rate = 1, neighbor = dsts[-1])

# Visualize topology
dot_script = "digraph topology {node [shape = box ];\n"
node_types = [pktgens, srcs, spines, dsts]
for i in range(len(node_types)):
  node_list = node_types[i]
  for j in range(len(node_list)):
    dot_script += str(node_list[j]) + \
                  " [pos = \"" + str(i * 100) + "," + str(j * 100) + "!\"]" + \
                  " [label = " + str(node_list[j]) + "];\n"

# Edges
for node in pktgens + srcs + spines:
  for neighbor in node.neighbors:
    edge_label = str(node.line_rate[neighbor]) if (node not in pktgens) else str(node.line_rate[neighbor] * node.load)
    dot_script += str(node) + "->" + str(neighbor) + \
                  " [label = " + edge_label + "];\n"
dot_script += "}"
print dot_script

# Simulate
for current_tick in range(1, TICKS + 1):
  for i in range(NODES):
    pktgens[i].tick(current_tick)
  for x in numpy.random.permutation(srcs):
    x.tick(current_tick)
  for x in numpy.random.permutation(spines):
    x.tick(current_tick)
  for i in range(NODES):
    dsts[i].tick(current_tick)

# Output stats
for i in range(NODES):
  dsts[i].dump_stats()
print >> sys.stderr, "Expected delay according to Karol's 1987 paper", (((NODES - 1) * 1.0) / NODES) * 0.5 * (1.0 / LINE_RATE) * (LOAD / (1 - LOAD))
