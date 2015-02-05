import sys
import numpy.random
import numpy

class Packet:

  def __init__(self, creation_tick, source, destination):
    assert(creation_tick > 0)
    self.tick = creation_tick
    self.dst  = destination
    self.src  = source
    self.last_hop = ""

class PktGen:

  def __init__(self, t_line_rate, t_load, t_num_dsts, t_source, t_neighbors):
    assert(isinstance(t_line_rate, int))
    assert(t_load > 0 and t_load <= 1.0)
    self.line_rate = dict()
    self.load      = t_load
    self.num_dsts  = t_num_dsts
    self.src       = t_source
    self.neighbors    = t_neighbors
    for neighbor in self.neighbors:
      self.line_rate[neighbor] = t_line_rate
    assert(len(self.neighbors) == 1)

  def __str__(self):
    return "PktGen" + str(self.src) + ""

  def tick(self, current_tick):
    the_neighbor = self.neighbors[0]
    num_pkts = 0
    if (self.line_rate[the_neighbor] != 0):
      assert(self.line_rate[the_neighbor] > 0)
      num_pkts = numpy.random.binomial(self.line_rate[the_neighbor], self.load)
    assert(num_pkts <= self.line_rate[the_neighbor])
    for i in range(num_pkts):
      dst  = numpy.random.random_integers(low = 0, high = self.num_dsts - 1)
      while (dst == self.src):
        dst  = numpy.random.random_integers(low = 0, high = self.num_dsts - 1)
      assert(dst >=0 and dst < self.num_dsts and dst != self.src)
      self.neighbor.recv(Packet(creation_tick = current_tick,\
                                source = self.src, \
                                destination = dst))

