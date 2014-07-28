// Copyright 2014 Anirudh Sivaraman

#include <cassert>
#include "src/memory_bank.h"

MemoryBank::MemoryBank(const uint8_t s_ops_per_tick, const uint16_t s_bank_id)
    : mem_ops_per_tick_(s_ops_per_tick),
      bank_id_(s_bank_id) {}

Address MemoryBank::write(const Cell & cell) {
  auto write_addr = Address(bank_id_, ++write_count_);
  assert(cells_.find(write_addr) == cells_.end());
  cells_[write_addr] = cell;
  op_count_++;
  assert(op_count_ <= mem_ops_per_tick_);
  return write_addr;
}

Cell MemoryBank::read(const Address & addr) {
  auto it = cells_.find(addr);
  assert(it != cells_.end());
  Cell cell = it->second;
  cells_.erase(it);
  op_count_++;
  assert(op_count_ <= mem_ops_per_tick_);
  return cell;
}
