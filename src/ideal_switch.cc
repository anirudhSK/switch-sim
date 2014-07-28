// Copyright 2014 Anirudh Sivaraman

#include <cstdio>
#include "src/ideal_switch.h"
#include "src/cell.h"

IdealSwitch::IdealSwitch(const uint16_t s_num_ports)
    : num_ports_(s_num_ports),
      output_queues_(num_ports_),
      stats_() {
  for (uint16_t i = 0; i < num_ports_; i++)
    for (uint16_t j = 0; j < num_ports_; j++)
      stats_[std::make_pair(i, j)] = 0;
}

void IdealSwitch::accept(const uint64_t tickno __attribute__((unused)),
                         const Cell & cell) {
  output_queues_.at(cell.output()).push(cell);
}

void IdealSwitch::tick(const uint64_t tickno __attribute__((unused))) {
  for (auto &x : output_queues_) {
    auto cell = x.front();
    stats_[std::make_pair(cell.input(), cell.output())]++;
    x.pop();
  }
}

void IdealSwitch::output_stats(void) const {
  for (auto &x : stats_) {
    printf("%u -> %u : %lu pkts\n",
           x.first.first, x.first.second, x.second);
  }
}
