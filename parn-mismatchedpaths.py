from simulator import *
import sys
import numpy.random

# Show that M-backpressure is worse than backpressure unless
# there is a mismatch in hop counts across the two paths
# Based on http://dl.acm.org/citation.cfm?id=2502369

# Usage
if (len(sys.argv) < 4):
  print sys.argv[0], "TICKS M num_interim_nodes"
  exit(0)

# Constants
scheme = "backpressure"
TICKS = int(sys.argv[1])
M = int(sys.argv[2])
num_interim_nodes = int(sys.argv[3])

# Nodes
# Packet generators
pkt = PktGen(t_max_rate = 1, t_load = 1.0, t_num_dsts = 1, t_source = 0)

# Nodes
src = SrcNode(t_line_rate = 1, t_num_dsts = 1, t_scheme = scheme)

# interim nodes
interims = [SrcNode(t_line_rate = 1, t_num_dsts = 1, t_scheme = scheme) for i in range(num_interim_nodes)]

# Spines
# for route through interim nodes
alt_spine = SpineNode(t_line_rate = 1, t_num_dsts = 1, t_name = "alt_spine")
main_spine = SpineNode(t_line_rate = 1, t_num_dsts = 1, t_name = "main_spine")

# Destinations
dst = DstNode(t_line_rate = 1, t_id = 0)

# Simulate
for current_tick in range(1, TICKS + 1):
  pkt.tick(src, current_tick)
  src.tick([interims[0] if num_interim_nodes > 0 else alt_spine, main_spine], current_tick, backpressure_M = M)
  # Permute all parallel entities
  for x in numpy.random.permutation([main_spine, alt_spine] + range(num_interim_nodes)):
    if (num_interim_nodes > 0 and x == (num_interim_nodes - 1)) :
      assert(x >= 0)
      interims[x].tick([alt_spine], current_tick, backpressure_M = M)
    elif x == main_spine :
      main_spine.tick([dst], current_tick)
    elif x == alt_spine:
      alt_spine.tick([dst], current_tick)
    else :
      assert(x >= 0)
      assert(x < len(interims))
      assert(x + 1 < len(interims))
      interims[x].tick([interims[x+1]], current_tick, backpressure_M = M)
  dst.tick(current_tick)

# Output stats
dst.dump_stats()
