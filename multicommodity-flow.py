#! /usr/bin/python
# An offline solver for the multicommodity max-flow problem
# Formulation taken from:
# http://support.sas.com/documentation/cdl/en/ormpug/65554/HTML/default/viewer.htm#ormpug_decomp_examples01.htm

import sys

class FlowNetwork:

  def __init__(self, graph_file, traffic_matrix_file, cost_file):
    self.links = dict()     # (u, v) --> link-speed of edge(u, v)
    self.tm = dict()        # (a, b) --> (demand from a to b, commodity_id)
    self.vertices = []
    self.incoming = dict()  # (vertex) --> [list of incoming (x, vertex) edges]
    self.outgoing = dict()  # (vertex) --> [list of outgoing (vertext, x) edges]
    self.balance = dict()   # (vertex, commodity_id) --> (balance)
    self.costs   = dict()   # (link, commodity_id) --> (cost)

    # Read in graph
    graph_fh = open(graph_file, "r")
    for line in graph_fh.readlines():
      records = line.split()
      assert(len(records) == 3)
      src = int(records[0])
      dst = int(records[1])
      link_speed = float(records[2])
      assert(link_speed > 0)
      self.links[(src, dst)] = link_speed

    # Set up vertices
    for link in self.links:
      src = link[0]
      dst = link[1]
      for node in link:
        if node not in self.vertices:
          self.vertices.append(node)
          self.outgoing[node] = []
          self.incoming[node] = []

    # Set up incoming and outgoing
    for link in self.links:
       src = link[0]
       dst = link[1]
       self.outgoing[src].append(link)
       self.incoming[dst].append(link)

    # Read in costs
    cost_fh = open(cost_file, "r")
    for line in cost_fh.readlines():
      records = line.split()
      assert(len(records) == 4)
      commodity_id = int(records[0])
      link = (int(records[1]), int(records[2]))
      cost = int(records[3])
      assert(cost > 0)
      self.costs[(link, commodity_id)] = cost  

    # Read in traffic matrix
    tm_fh = open(traffic_matrix_file, "r")
    commodity_id = 0
    for line in tm_fh.readlines():
      records = line.split()
      assert(len(records) == 3)
      src = int(records[0])
      dst = int(records[1])
      demand = float(records[2])
      assert(demand > 0)
      self.tm[(src, dst)] = (demand, commodity_id)
      commodity_id += 1

    # Set up data structure for balance constraints
    for vertex in self.vertices:
      for commodity_id in range(len(self.tm)):
        self.balance[(vertex, commodity_id)] = 0

    # Populate it
    for commodity in self.tm:
      src = commodity[0]
      dst = commodity[1]
      demand = self.tm[commodity][0]
      commodity_id = self.tm[commodity][1]
      self.balance[(src, commodity_id)] = demand
      self.balance[(dst, commodity_id)] = -demand

  def flow_on_link_var(self, link_src, link_dst, commodity_id):
    return "x_" + str(link_src) + "_" + str(link_dst) + "_" + str(commodity_id)

  def get_lp(self):
    num_commodities = len(self.tm)
    # Objective function
    print "min: ",
    for link in self.links:
      for k in range(num_commodities):
        print self.costs[(link, k)], "x" + str(link[0]) + str(link[1]) + str(k) + " +",
    print " 0 ;"
    print

    # Capacity constraints
    for link in self.links:
      for k in range(num_commodities):
        print self.flow_on_link_var(link[0], link[1], k) + " +",
      print "0 <= " + str(self.links[link]) + ";"
    print

    # Balance constraints
    for vertex in self.vertices:
      for k in range(num_commodities):
        for link in self.outgoing[vertex]:
          assert(link[0] == vertex)
          print self.flow_on_link_var(link[0], link[1], k) + " +",
        print "0 - ",

        for link in self.incoming[vertex]:
          assert(link[1] == vertex)
          print self.flow_on_link_var(link[0], link[1], k) + " -",
        print "0 = " + str(self.balance[(vertex, k)]) + ";"
    print

flow_network = FlowNetwork("./graph.sample", "./tm.sample", "./cost.sample")
flow_network.get_lp()
