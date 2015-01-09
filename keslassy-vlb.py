#! /usr/bin/python
# Simulate Keslassy et al's paper on Optimal Load Balancing
import numpy.random
import sys
PORTS = int(sys.argv[1])
LEAFS = PORTS
SPINES = PORTS
LINE_RATE = PORTS
# i.e. rate relative to interconnect links
# Keslassy's paper sets the line rates to R
# and the interconnect rates to R/N (Fig. 1).
# We set R=N, so that R/N = 1
# (so that we don't use fractional rates)

ARRIVAL_RATE = float(sys.argv[2])
numpy.random.seed(int(sys.argv[3]))
TICKS = int(sys.argv[4])

leaf_nodes = range(LEAFS)
spine_nodes = range(SPINES)

# Queue data structures
leaf_inputs  = [] 
leaf_outputs = []
spine_voqs = []

# Stat counters
pkt_stats = dict()
del_stats = dict()

for leaf in leaf_nodes:
  leaf_inputs.append([])
  leaf_outputs.append([])
  for leaf_peer in leaf_nodes:
    pkt_stats[(leaf, leaf_peer)] = 0
    del_stats[(leaf, leaf_peer)] = 0

for spine in spine_nodes:
  spine_voqs.append([])
  for leaf in leaf_nodes:
    spine_voqs[spine].append([])

# Simulate
for current_tick in range(1, TICKS + 1):
  # Generate packets at leaf_inputs
  for i in range(0, LEAFS):
    for j in range(0, numpy.random.binomial(LINE_RATE, ARRIVAL_RATE)):
      leaf_inputs[i].append((current_tick, numpy.random.random_integers(0, LEAFS - 1), i));

  # Move all packets from leaf_inputs to spine_voqs
  # Use round-robin to load balance across all spines
  # We have a full mesh from leafs to spines
  # and each leaf-spine link can transmit 1 pkt/slot
  for i in numpy.random.permutation(range(0, LEAFS)):
    permute_spines = numpy.random.permutation(range(SPINES))
    spine_cursor=0
    while (len(leaf_inputs[i]) > 0):
      pkt_to_bounce = leaf_inputs[i].pop(0);
      assert (spine_cursor < SPINES)
      spine_voqs[permute_spines[spine_cursor]][pkt_to_bounce[1]].append(pkt_to_bounce);
      spine_cursor = (spine_cursor + 1)

  # All packets should have been moved by now
  for i in range(0, LEAFS):
    assert(len(leaf_inputs[i]) == 0)

  # Move as many pkts as possible from spine_voqs to leaf_outputs
  # Use round-robin to go through all VOQs
  # We have a full mesh from spines to leafs
  # and each spine-leaf link can transmit 1 pkt/slot
  for i in numpy.random.permutation(range(0, SPINES)):
    for j in numpy.random.permutation(range(0, LEAFS)):
      if (len(spine_voqs[i][j]) > 0):
        pkt_to_send = spine_voqs[i][j].pop(0)
        assert(pkt_to_send[1] == j);
        leaf_outputs[pkt_to_send[1]].append(pkt_to_send);

  # Transmit packets out
  for i in range(0, LEAFS):
    # pop out up to LINE RATE number of packets
    for j in range(0, min(LINE_RATE, len(leaf_outputs[i]))):
      tx_pkt = leaf_outputs[i].pop(0);
      src = tx_pkt[2];
      pkt_stats[(src, i)] = pkt_stats[(src, i)]  + 1;
      assert(current_tick >= tx_pkt[0]);
      del_stats[(src, i)] = del_stats[(src, i)] + (current_tick - tx_pkt[0]);

# Output stats
for dst in range(0, LEAFS):
  total = 0
  for src in range (0, LEAFS):
    print "src", src, "dst", dst, "pkts", pkt_stats[(src, dst)], "del",\
          del_stats[(src, dst)] * 1.0 / pkt_stats[(src, dst)]
    total += pkt_stats[(src, dst)]
  print "total", total
print "Expected delay according to Karol's 1987 paper", (((LEAFS - 1) * 1.0) / LEAFS) * 0.5 * (1.0 / LINE_RATE) * (ARRIVAL_RATE / (1 - ARRIVAL_RATE))
