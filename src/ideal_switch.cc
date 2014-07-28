#include <cstdio>
#include "src/ideal_switch.h"
#include "src/cell.h"

// Copyright 2014 Anirudh Sivaraman

IdealSwitch::IdealSwitch(const uint16_t s_num_ports)
    : num_ports_(s_num_ports),
      output_queues_(num_ports_) {}

void IdealSwitch::accept(const Cell & cell) {
  output_queues_.at(cell.output()).push(cell);
}

void IdealSwitch::tick(const uint64_t tickno) {
  for (auto &x : output_queues_) {
    auto cell = x.front();
    printf("Tick: %lu, input: %u, output: %u\n", tickno,
           cell.input(), cell.output());
    x.pop();
  }
}
