#ifndef SRC_PSM_SWITCH_H_
#define SRC_PSM_SWITCH_H_

// Copyright 2014 Anirudh Sivaraman

#include <queue>
#include <vector>
#include <map>
#include <utility>
#include <cstdint>

#include "src/cell.h"
#include "src/memory.h"

/*
   Parallel Shared Memory switch with N shared memories
   where N is the number of ports
 */

class PSMSwitch {
 public:
  explicit PSMSwitch(const uint16_t s_num_ports,
                     const uint16_t s_num_banks,
                     const uint8_t s_mem_ops_per_tick);
  void output_stats(void) const;
  void tick(const uint64_t tickno);
  void accept(const uint64_t tickno, const Cell & cell);
  void reset(void) { cell_memory_.reset(); }

 private:
  const uint16_t num_ports_;
  Memory cell_memory_;
  std::vector<std::queue<Address>> output_queues_;
  std::map<std::pair<uint16_t, uint16_t>, uint64_t> stats_;
};

#endif  // SRC_PSM_SWITCH_H_
