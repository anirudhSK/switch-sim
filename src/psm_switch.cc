// Copyright 2014 Anirudh Sivaraman

#include <cstdio>
#include "src/psm_switch.h"
#include "src/cell.h"

PSMSwitch::PSMSwitch(const uint16_t s_num_ports,
                     const uint16_t s_num_banks,
                     const uint8_t s_mem_ops_per_tick)
    : num_ports_(s_num_ports),
      cell_memory_(s_num_banks, s_mem_ops_per_tick),
      output_queues_(num_ports_),
      stats_() {
  for (uint16_t i = 0; i < num_ports_; i++)
    for (uint16_t j = 0; j < num_ports_; j++)
      stats_[std::make_pair(i, j)] = 0;
}

void PSMSwitch::accept(const uint64_t tickno __attribute__((unused)),
                       const Cell & cell) {
  Address address = cell_memory_.write(cell);
  output_queues_.at(cell.output()).push(address);
}

void PSMSwitch::tick(const uint64_t tickno __attribute__((unused))) {
  for (auto &x : output_queues_) {
    if (x.empty()) continue;
    auto cell = cell_memory_.read(x.front());
    stats_[std::make_pair(cell.input(), cell.output())]++;
    x.pop();
  }
}

void PSMSwitch::output_stats(void) const {
  for (auto &x : stats_) {
    printf("%u -> %u : %lu pkts\n",
           x.first.first, x.first.second, x.second);
  }
}
