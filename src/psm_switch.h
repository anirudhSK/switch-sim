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
   Parallel Shared Memory switch:
   - num_banks_ shared memories
   - num_ports_ ports
 */

class PSMSwitch {
 public:
  explicit PSMSwitch(const uint16_t s_num_ports,
                     const uint16_t s_num_banks,
                     const uint8_t s_mem_ops_per_tick);
  void output_stats(void) const;
  void tick(const uint64_t tickno);
  void reset(const uint64_t tickno);
  void accept(const uint64_t tickno, const Cell & cell);
  uint16_t find_free_bank(const uint64_t departure_time) const;

 private:
  const uint16_t num_ports_;
  const uint16_t num_banks_;
  Memory cell_memory_;
  MemoryBank bypass_buffer_;
  std::vector<std::queue<Address>> output_queues_;
  std::map<std::pair<uint16_t, uint16_t>, uint64_t> stats_;

  std::vector<uint8_t> current_arrival_counters_;
  std::vector<uint8_t> current_departure_counters_;
  std::map<uint64_t, std::vector<uint8_t>> future_departure_counters_;
};

#endif  // SRC_PSM_SWITCH_H_
