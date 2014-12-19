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
output_pkt_count = []
output_del_acc = []

for leaf in leaf_nodes:
  leaf_inputs.append([])
  leaf_outputs.append([])
  output_pkt_count.append(0);
  output_del_acc.append(0);

for spine in spine_nodes:
  spine_voqs.append([])
  for leaf in leaf_nodes:
    spine_voqs[spine].append([])

# Simulate
for current_tick in range(1, TICKS + 1):
  # Generate packets at leaf_inputs
  for i in range(0, LEAFS):
    for j in range(0, numpy.random.binomial(LINE_RATE, ARRIVAL_RATE)):
      leaf_inputs[i].append((current_tick, numpy.random.random_integers(0, LEAFS - 1)));

  # Move all packets from leaf_inputs to spine_voqs
  # Use round-robin to load balance across all spines
  # We have a full mesh from leafs to spines
  # and each leaf-spine link can transmit 1 pkt/slot
  spine_cursor=0
  for i in range(0, LEAFS):
    while (len(leaf_inputs[i]) > 0):
      pkt_to_bounce = leaf_inputs[i].pop(0);
      spine_voqs[spine_cursor][pkt_to_bounce[1]].append(pkt_to_bounce);
      spine_cursor = (spine_cursor + 1) % SPINES

  # All packets should have been moved by now
  for i in range(0, LEAFS):
    assert(len(leaf_inputs[i]) == 0)

  # Move as many pkts as possible from spine_voqs to leaf_outputs
  # Use round-robin to go through all VOQs
  # We have a full mesh from spines to leafs
  # and each spine-leaf link can transmit 1 pkt/slot
  for i in range(0, SPINES):
    for j in range(0, LEAFS):
      if (len(spine_voqs[i][j]) > 0):
        pkt_to_send = spine_voqs[i][j].pop(0)
        assert(pkt_to_send[1] == j);
        leaf_outputs[pkt_to_send[1]].append(pkt_to_send);

  # Transmit packets out
  for i in range(0, LEAFS):
    # pop out up to LINE RATE number of packets
    for j in range(0, min(LINE_RATE, len(leaf_outputs[i]))):
      tx_pkt = leaf_outputs[i].pop(0);
      output_pkt_count[i] = output_pkt_count[i] + 1;
      assert(current_tick >= tx_pkt[0]);
      output_del_acc[i] = output_del_acc[i] + (current_tick - tx_pkt[0]);

# Output stats
for i in range (0, LEAFS):
  print i, (output_pkt_count[i] * 1.0 / (TICKS * LINE_RATE)), "pkt/tick",\
        (output_del_acc[i] * 1.0 /output_pkt_count[i]) * LINE_RATE, "ticks"

# Queue stats
for i in range (0, LEAFS):
  print "Queue size at leaf_inputs", i, len(leaf_inputs[i])

for i in range (0, SPINES):
  for j in range(0, LEAFS):
    print "VOQ(",i,",",j,")",len(spine_voqs[i][j])

for i in range (0, LEAFS):
  print "Queue size at leaf outputs", i, len(leaf_outputs[i])
