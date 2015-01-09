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

  def tick(self, current_tick):
    num_pkts = numpy.random.binomial(self.max_rate, self.load)
    assert(num_pkts <= self.max_rate)
    for i in range(num_pkts):
      dst  = numpy.random.random_integers(low = 0, high = self.num_dsts - 1)
      assert(dst >=0 and dst < self.num_dsts)
      self.neighbor.recv(Packet(creation_tick = current_tick,\
                                source = self.src, \
                                destination = dst))

class DstNode:

  def __init__(self, t_line_rate, t_id):
    assert(isinstance(t_line_rate, int))
    self.line_rate = t_line_rate
    self.pkt_queue = []
    self.id = t_id
    self.pkt_stats = dict()
    self.del_stats = dict()
    self.path_stats = dict()

  def recv(self, pkt):
    assert(pkt.dst == self.id)
    self.pkt_queue.append(pkt)

  def tick(self, current_tick):
    for i in range(min(self.line_rate, len(self.pkt_queue))):
      pkt = self.pkt_queue.pop(0)
      src = pkt.src
      if (src not in self.pkt_stats):
        self.pkt_stats[src] = 1
        assert(current_tick >= pkt.tick)
        self.del_stats[src] = (current_tick - pkt.tick)
      else:
        self.pkt_stats[src] += 1
        self.del_stats[src] += (current_tick - pkt.tick)

      # Measure path stats
      if (pkt.last_hop not in self.path_stats):
        self.path_stats[pkt.last_hop] = 1
      else:
        self.path_stats[pkt.last_hop] += 1

  def dump_stats(self):
    total = 0
    for src in self.pkt_stats:
      print "src", src, "dst", self.id, "pkts", self.pkt_stats[src], "del", self.del_stats[src] * 1.0 / self.pkt_stats[src]
      total += self.pkt_stats[src]
    for path in self.path_stats:
      print "last_hop", path, "pkts", self.path_stats[path]
    print "total", total

  def get_id(self):
    return self.id
