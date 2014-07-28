// Copyright 2014 Anirudh Sivaraman

#include <cstdlib>
#include <cstdio>
#include <string>

#include "src/psm_switch.h"
#include "src/traffic_generator.h"
#include "src/traffic_generator_templates.cc"

int main(const int argc, const char* argv[]) {
  if (argc < 4) {
    printf("Usage: %s num_ports seed ticks\n", argv[0]);
    exit(0);
  }
  const uint16_t num_ports = std::stoi(std::string(argv[1]));
  const uint8_t seed = std::stoi(std::string(argv[2]));
  const uint64_t ticks = std::stoi(std::string(argv[3]));

  PSMSwitch psm_switch(num_ports);
  TrafficGenerator traf_gen(num_ports, seed);
  for (uint64_t i = 0; i < ticks; i++) {
    traf_gen.tick(i, psm_switch);
    psm_switch.tick(i);
  }
  psm_switch.output_stats();
}
