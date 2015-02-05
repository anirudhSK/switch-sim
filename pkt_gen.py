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

  def __init__(self, t_max_rate, t_load, t_num_dsts, t_source, t_neighbor):
    assert(isinstance(t_max_rate, int))
    assert(t_load > 0 and t_load <= 1.0)
    self.max_rate  = t_max_rate
    self.load      = t_load
    self.num_dsts  = t_num_dsts
    self.src       = t_source
    self.neighbor    = t_neighbor

  def __str__(self):
    return "PktGen" + str(self.src) + ""

  def tick(self, current_tick):
    num_pkts = numpy.random.binomial(self.max_rate, self.load)
    assert(num_pkts <= self.max_rate)
    for i in range(num_pkts):
      dst  = numpy.random.random_integers(low = 0, high = self.num_dsts - 1)
      assert(dst >=0 and dst < self.num_dsts)
      self.neighbor.recv(Packet(creation_tick = current_tick,\
                                source = self.src, \
                                destination = dst))

