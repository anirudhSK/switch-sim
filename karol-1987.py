#! /usr/bin/python

# Simulator for Karol's 1987 paper:
# Input vs Output queuing on a space-division switch

# Setup
import random
import sys
import numpy.random
random.seed(1)
num_ports = int(sys.argv[1])
current_tick = 0
arrival_rate = float(sys.argv[2])
input_queues = []
output_queues = []
output_pkt_count = []
output_del_acc = []
total_ticks = 1000000
OUTPUT_QUEUE_MAX = int(sys.argv[3]);
for i in range(0, num_ports):
  input_queues.append([])
  output_queues.append([])
  output_pkt_count.append([])
  output_del_acc.append([])
  for j in range(0, num_ports):
    output_pkt_count[i].append(0)
    output_del_acc[i].append(0)

while (current_tick < total_ticks):
  inputs_for_each_output = []

  # Input side
  for i in range(0, num_ports):
    rnd = numpy.random.random();
    if (rnd < arrival_rate):
      input_queues[i].append((current_tick, random.randint(0, num_ports - 1), i));
    inputs_for_each_output.append([])

  # Look at the input heads
  for i in range(0, num_ports):
    if (len(input_queues[i]) == 0) :
      continue
    output_at_head = input_queues[i][0][1]; # 0 for head of queue, 1 for output port
    inputs_for_each_output[output_at_head].append(i);

  # Switch packets to outputs
  for i in range(0, num_ports):
    inputs = inputs_for_each_output[i];
    if (len(inputs) == 0):
      continue
    else :
      current_queue_size = len(output_queues[i]);
      assert(OUTPUT_QUEUE_MAX > current_queue_size);
      sample_size = min(OUTPUT_QUEUE_MAX - current_queue_size, len(inputs));
      chosen_inputs = random.sample(inputs, sample_size);
      for input_port in chosen_inputs:
        input_packet = input_queues[input_port].pop(0);
        output_queues[i].append(input_packet);

  # Now deque packets
  for i in range(0, num_ports):
    if (len(output_queues[i]) > 0):
      tx_pkt = output_queues[i].pop(0);
      assert(current_tick >= tx_pkt[0]);
      input_port = tx_pkt[2];
      output_pkt_count[input_port][i] = output_pkt_count[input_port][i] + 1;
      output_del_acc[input_port][i] = output_del_acc[input_port][i] + (current_tick - tx_pkt[0]);

  current_tick = current_tick + 1;

for dst in range (0, num_ports):
  total = 0
  for src in range (0, num_ports):
   print "src", src, "dst", dst, "pkts", output_pkt_count[src][dst] * 1.0 * num_ports , "del", output_del_acc[src][dst] * 1.0 / (1.0 * num_ports * output_pkt_count[src][dst])
   total += output_pkt_count[src][dst]
  print "total", num_ports * total

