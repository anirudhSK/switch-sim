// Copyright 2014 Anirudh Sivaraman

#include <cstdio>

#include "src/ideal_switch.h"
#include "src/traffic_generator.h"
#include "src/traffic_generator_templates.cc"

int main() {
  IdealSwitch ideal_switch(64);
  TrafficGenerator traf_gen(64);
  for (uint64_t i = 0; i < 10000; i++) {
    traf_gen.tick(i, ideal_switch);
    ideal_switch.tick(i);
  }
  ideal_switch.output_stats();
}
