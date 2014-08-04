// Copyright 2014 Anirudh Sivaraman

#include <cassert>

#include "src/cell.h"

Cell::Cell(const uint16_t s_input, const uint16_t s_output)
    : input_(s_input),
      output_(s_output) { assert(input_ != output_); }
