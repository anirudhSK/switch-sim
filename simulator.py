import sys
import numpy.random
import numpy

class Packet:

  def __init__(self, creation_tick, source, destination):
    assert(creation_tick > 0)
    self.tick = creation_tick
    self.dst  = destination
    self.src  = source

class PktGen:

  def __init__(self, t_max_rate, t_load, t_num_dsts, t_source):
    assert(isinstance(t_max_rate, int))
    assert(t_load > 0 and t_load <= 1.0)
    self.max_rate  = t_max_rate
    self.load      = t_load
    self.num_dsts  = t_num_dsts
    self.src       = t_source

  def tick(self, target, current_tick):
    num_pkts = numpy.random.binomial(self.max_rate, self.load)
    assert(num_pkts <= self.max_rate)
    for i in range(num_pkts):
      dst  = numpy.random.random_integers(low = 0, high = self.num_dsts - 1)
      assert(dst >=0 and dst < self.num_dsts)
      target.recv(Packet(creation_tick = current_tick,\
                         source = self.src, \
                         destination = dst))

class SrcNode:

  object_count = 0

  def __str__(self):
    return "leaf"+str(self.id)

  def __init__(self, t_line_rate, t_num_dsts, t_scheme):
    assert(isinstance(t_line_rate, int))
    self.line_rate = t_line_rate
    self.pkt_queue = []
    self.agg_pkt_queue = []
    self.id = SrcNode.object_count
    self.scheme = t_scheme
    SrcNode.object_count += 1
    for i in range(0, t_num_dsts):
      self.pkt_queue.append([])

  def tick(self, targets, current_tick, backpressure_M):

    if (self.scheme == "vlb"):
      assert(len(self.agg_pkt_queue) <= self.line_rate * len(targets));

      for target in numpy.random.permutation(targets):
        if (len(self.agg_pkt_queue) > 0) :
          target.recv(self.agg_pkt_queue.pop(0))
      assert(len(self.agg_pkt_queue) == 0)

    elif (self.scheme == "backpressure"):
      for target in numpy.random.permutation(targets):
        # Find destination with maximum backpressure
        max_backpressure = -sys.maxint - 1
        argmax_list = []
        for dst_id in range(len(self.pkt_queue)):
          backpressure = len(self.pkt_queue[dst_id]) - len(target.pkt_queue[dst_id])
          if (backpressure > max_backpressure) :
            max_backpressure = backpressure
            argmax_list = [dst_id]
          elif (backpressure == max_backpressure):
            argmax_list += [dst_id]

        # Break ties randomly
        argmax = numpy.random.choice(argmax_list)

        if (max_backpressure >= backpressure_M):
          assert(backpressure_M <= 0 or len(target.pkt_queue[argmax]) < len(self.pkt_queue[argmax]))
          for i in range(min(len(self.pkt_queue[argmax]), self.line_rate)):
            target.recv(self.pkt_queue[argmax].pop(0))

    else :
      assert(False)

  def recv(self, pkt):
    if (self.scheme == "vlb"):
      self.agg_pkt_queue.append(pkt)
    elif (self.scheme == "backpressure"):
      self.pkt_queue[pkt.dst].append(pkt)

class SpineNode:

  object_count = 0

  def __str__(self):
    return "spine"+str(self.id)

  def __init__(self, t_line_rate, t_num_dsts):
    assert(isinstance(t_line_rate, int))
    self.line_rate = t_line_rate
    self.pkt_queue = []
    self.id = SpineNode.object_count
    SpineNode.object_count += 1
    for i in range(t_num_dsts):
      self.pkt_queue.append([])

  def tick(self, targets, current_tick):
    for target in numpy.random.permutation(targets):
      # Backpressure is trivial on spine nodes
      # Because queues at destinations are 0
      for i in range(min(self.line_rate, len(self.pkt_queue[target.get_id()]))):
        target.recv(self.pkt_queue[target.get_id()].pop(0))

  def recv(self, pkt):
    self.pkt_queue[pkt.dst].append(pkt)

  def modify_line_rate(self, new_line_rate):
    self.line_rate = new_line_rate

class DstNode:

  def __init__(self, t_line_rate, t_id):
    assert(isinstance(t_line_rate, int))
    self.line_rate = t_line_rate
    self.pkt_queue = []
    self.id = t_id
    self.pkt_stats = dict()
    self.del_stats = dict()

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

  def dump_stats(self):
    total = 0
    for src in self.pkt_stats:
      print "src", src, "dst", self.id, "pkts", self.pkt_stats[src], "del", self.del_stats[src] * 1.0 / self.pkt_stats[src]
      total += self.pkt_stats[src]
    print "total", total

  def get_id(self):
    return self.id
