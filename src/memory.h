#ifndef SRC_MEMORY_H_
#define SRC_MEMORY_H_

// Copyright 2014 Anirudh Sivaraman

#include <vector>

#include "src/cell.h"
#include "src/address.h"
#include "src/memory_bank.h"

class Memory {
 public:
  Memory(const uint16_t s_num_banks, const uint8_t s_mem_ops_per_tick);
  Address write(const Cell & cell);
  Cell read(const Address & addr) {
    return memory_banks_.at(addr.bank_id()).read(addr);
  }
  void reset(void) {
    bank_cursor_ = 0;
    for (auto &x : memory_banks_) x.reset();
  }

 private:
  /* Number of READ/WRITE ops per tick */
  const uint8_t mem_ops_per_tick_;

  /* Number of banks */
  const uint16_t num_banks_;

  /* Vector of banks */
  std::vector<MemoryBank> memory_banks_;

  /* Bank cursor, which bank to write next? */
  uint16_t bank_cursor_ {0};
};

#endif  // SRC_MEMORY_H_
