// Copyright 2014 Anirudh Sivaraman

#include <cassert>
#include <cstdio>
#include "src/memory.h"

Memory::Memory(const uint16_t s_num_banks, const uint8_t s_mem_ops_per_tick)
    : mem_ops_per_tick_(s_mem_ops_per_tick),
      num_banks_(s_num_banks),
      memory_banks_() {
  for (uint16_t i = 0; i < num_banks_; i++) {
    memory_banks_.emplace_back(s_mem_ops_per_tick, i);
  }
}

Address Memory::write(const Cell & cell, const uint16_t bank_cursor) {
  return memory_banks_.at(bank_cursor).write(cell);
}
