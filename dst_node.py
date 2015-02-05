import sys
class DstNode:

  def __init__(self, t_line_rate, t_id):
    assert(isinstance(t_line_rate, int))
    self.line_rate = t_line_rate
    self.pkt_queue = []
    self.id = t_id
    self.pkt_stats = dict()
    self.del_stats = dict()
    self.path_stats = dict()

  def __str__(self):
    return "Dst" + str(self.id)

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
    assert(len(self.pkt_queue) == 0)
    # Periodically dump stats
    if (current_tick % 1000 == 0):
      self.dump_stats()

  def dump_stats(self):
    total = 0
    for src in self.pkt_stats:
      print >> sys.stderr, "src", src, "dst", self.id, "pkts", self.pkt_stats[src], "del", self.del_stats[src] * 1.0 / self.pkt_stats[src]
      total += self.pkt_stats[src]
    for path in self.path_stats:
      print >> sys.stderr,  "last_hop", path, "pkts", self.path_stats[path]
    print >> sys.stderr, "total", total

  def get_id(self):
    return self.id
