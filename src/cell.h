#ifndef SRC_CELL_H_
#define SRC_CELL_H_

// Copyright 2014 Anirudh Sivaraman

#include <cstdint>

class Cell {
 public:
  Cell(const uint16_t s_output, const uint16_t s_input);
  uint16_t output(void) const { return output_; }
  uint16_t input(void) const { return input_; }
 private:
  uint16_t output_ {0};
  uint16_t input_ {0};
};

#endif  // SRC_CELL_H_
