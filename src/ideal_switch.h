#ifndef SRC_IDEAL_SWITCH_H_
#define SRC_IDEAL_SWITCH_H_

// Copyright 2014 Anirudh Sivaraman

#include <queue>
#include <vector>
#include <cstdint>

#include "src/cell.h"

class IdealSwitch {
 public:
  explicit IdealSwitch(const uint16_t s_num_ports);
  void tick(const uint64_t tickno);
  void accept(const Cell & cell);
 private:
  const uint16_t num_ports_ {0};
  std::vector<std::queue<Cell>> output_queues_;
};

#endif  // SRC_IDEAL_SWITCH_H_
