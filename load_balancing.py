#! /usr/bin/python
# Simulate Awerbuch and Leighton's 1993 FOCS paper
# on a bipartite graph, because that's what most datacenters
# care about
import random
import sys

TICKS = 1000000
LEAFS = 10
SPINES = 10
ARRIVAL_RATE = float(sys.argv[1])

leaf_nodes = range(LEAFS)
spine_nodes = range(SPINES)

# Queue data structures
leaf_inputs  = [] 
leaf_outputs = []
spine_outputs = []
output_pkt_count = []
output_del_acc = []
for leaf in leaf_nodes:
  leaf_inputs.append([])
  leaf_outputs.append([])
  output_pkt_count.append(0);
  output_del_acc.append(0);

for spine in spine_nodes:
  spine_outputs.append([])

# Simulate
for current_tick in range(0, TICKS):
  # Generate packets at leaf_inputs
  for i in range(0, LEAFS):
    rnd = random.random();
    if (rnd < ARRIVAL_RATE):
      leaf_inputs[i].append((current_tick, random.randint(0, LEAFS - 1)));

  # Move them from leaf_inputs to spine_outputs
  for i in range(0, LEAFS):
    if (len(leaf_inputs[i]) == 0):
      continue
    pkt_to_bounce = leaf_inputs[i].pop(0); 
    spine_outputs[random.randint(0, SPINES - 1)].append(pkt_to_bounce);

  # Move them from spine_outputs to leaf_outputs
  for i in range(0, SPINES):
    if (len(spine_outputs[i]) == 0):
      continue
    pkt_to_send = spine_outputs[i].pop(0);
    leaf_outputs[pkt_to_send[1]].append(pkt_to_send);

  # Transmit packets out
  for i in range(0, LEAFS):
    if (len(leaf_outputs[i])==0):
      continue
    tx_pkt = leaf_outputs[i].pop(0);
    output_pkt_count[i] = output_pkt_count[i] + 1;
    assert(current_tick >= tx_pkt[0]);
    output_del_acc[i] = output_del_acc[i] + (current_tick - tx_pkt[0]);

for i in range (0, LEAFS):
   print i, output_pkt_count[i] * 1.0 / TICKS, "pkt/tick", output_del_acc[i] * 1.0 /output_pkt_count[i], "ticks"
