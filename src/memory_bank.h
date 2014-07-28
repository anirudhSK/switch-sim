#ifndef SRC_MEMORY_BANK_H_
#define SRC_MEMORY_BANK_H_

// Copyright 2014 Anirudh Sivaraman

#include <cassert>
#include <cstdint>
#include <map>

#include "src/address.h"
#include "src/cell.h"

class MemoryBank {
 public:
  MemoryBank(const uint8_t s_ops_per_tick, const uint16_t s_bank_id);
  Address write(const Cell & cell);
  Cell read(const Address & addr);
  void reset(void) { op_count_ = 0; }
  bool ops_depleted(void) const {
    assert(op_count_ <= mem_ops_per_tick_);
    return op_count_ == mem_ops_per_tick_;
  }

 private:
  /* Number of READ/WRITE ops per tick */
  const uint8_t mem_ops_per_tick_;

  /* ID of bank */
  const uint16_t bank_id_;

  /* Number of write operations so far */
  uint64_t write_count_ {0};

  /* Number of ops this tick */
  uint8_t op_count_ {0};

  /* Cells stored in this memory */
  std::map<Address, Cell> cells_ {};
};

#endif  // SRC_MEMORY_BANK_H_
