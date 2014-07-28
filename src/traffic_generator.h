#ifndef SRC_TRAFFIC_GENERATOR_H_
#define SRC_TRAFFIC_GENERATOR_H_

// Copyright 2014 Anirudh Sivaraman

#include <boost/random/uniform_int_distribution.hpp>
#include "src/random.h"

class TrafficGenerator {
 private:
  const uint16_t num_ports_;
  boost::random::uniform_int_distribution<> distribution_;
  PRNG prng_;
 public:
  explicit TrafficGenerator(const uint16_t s_num_ports, const uint8_t seed);
  template <class NextHop>
  void tick(const uint64_t tickno, NextHop & next);
};

#endif  // SRC_TRAFFIC_GENERATOR_H_
