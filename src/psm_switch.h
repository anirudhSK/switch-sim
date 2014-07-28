#ifndef SRC_PSM_SWITCH_H_
#define SRC_PSM_SWITCH_H_

// Copyright 2014 Anirudh Sivaraman

#include <queue>
#include <vector>
#include <map>
#include <utility>
#include <cstdint>

#include "src/cell.h"

/*
   Parallel Shared Memory switch with N shared memories
   where N is the number of ports
 */

class PSMSwitch {
 public:
  explicit PSMSwitch(const uint16_t s_num_ports);
  void output_stats(void) const;
  void tick(const uint64_t tickno);
  void accept(const uint64_t tickno, const Cell & cell);
 private:
  const uint16_t num_ports_ {0};
  std::vector<std::queue<Cell>> output_queues_;
  std::map<std::pair<uint16_t, uint16_t>, uint64_t> stats_;
};

#endif  // SRC_PSM_SWITCH_H_
