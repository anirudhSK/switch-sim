// Copyright 2014 Anirudh Sivaraman

#include "src/traffic_generator.h"
#include "src/cell.h"

template <class NextHop>
void TrafficGenerator::tick(const uint64_t tickno, NextHop & next) {
  for (uint16_t i = 0; i < num_ports_; i++) {
    Cell cell(i, distribution_(prng_));
    next.accept(tickno, cell);
  }
}
