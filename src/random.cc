// Copyright 2014 Anirudh Sivaraman

#include <unistd.h>
#include <sys/types.h>
#include <ctime>

#include "src/random.h"

PRNG & global_PRNG(void) {
  unsigned int current_time = static_cast<unsigned int>(time(nullptr));
  unsigned int pid  = getpid();
  static PRNG generator(current_time ^ pid);
  return generator;
}
