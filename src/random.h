#ifndef SRC_RANDOM_H_
#define SRC_RANDOM_H_

// Copyright 2014 Anirudh Sivaraman

#include <boost/random/mersenne_twister.hpp>
typedef boost::random::mt19937 PRNG;

extern PRNG & global_PRNG();
 
#endif  // SRC_RANDOM_H_
