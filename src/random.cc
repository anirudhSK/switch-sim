// Copyright 2014 Anirudh Sivaraman

#include <unistd.h>
#include <sys/types.h>
#include <ctime>

#include "src/random.h"

PRNG & global_PRNG(void) {
  static PRNG generator(time(nullptr) ^ getpid());
  return generator;
}
