// Copyright 2014 Anirudh Sivaraman

#include <cstdio>

#include "src/psm_switch.h"
#include "src/traffic_generator.h"
#include "src/traffic_generator_templates.cc"

int main() {
  PSMSwitch psm_switch(64);
  TrafficGenerator traf_gen(64);
  for (uint64_t i = 0; i < 10000; i++) {
    traf_gen.tick(i, psm_switch);
    psm_switch.tick(i);
  }
  psm_switch.output_stats();
}
