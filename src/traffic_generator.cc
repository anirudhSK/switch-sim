// Copyright 2014 Anirudh Sivaraman

#include "src/traffic_generator.h"

TrafficGenerator::TrafficGenerator(const uint16_t s_num_ports,
                                   const uint8_t seed)
    : num_ports_(s_num_ports),
      distribution_(0, num_ports_ - 1),
      prng_(seed) {}
