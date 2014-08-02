// Copyright 2014 Anirudh Sivaraman

#include "src/traffic_generator.h"
#include "src/cell.h"

template <class NextHop>
void TrafficGenerator::tick(const uint64_t tickno, NextHop & next) {
  for (uint16_t i = 0; i < num_ports_; i++) {
    uint16_t output_port = i;
    while (output_port == i) {
      output_port = distribution_(prng_);
    }
    Cell cell(i, output_port);
    next.accept(tickno, cell);
  }
}
