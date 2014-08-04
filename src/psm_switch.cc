// Copyright 2014 Anirudh Sivaraman

#include <cstdio>
#include "src/psm_switch.h"
#include "src/cell.h"

PSMSwitch::PSMSwitch(const uint16_t s_num_ports,
                     const uint16_t s_num_banks,
                     const uint8_t s_mem_ops_per_tick)
    : num_ports_(s_num_ports),
      num_banks_(s_num_banks),
      cell_memory_(s_num_banks, s_mem_ops_per_tick),
      bypass_buffer_(UINT8_MAX, UINT16_MAX),
      output_queues_(num_ports_),
      stats_(),
      current_arrival_counters_(num_banks_),
      current_departure_counters_(num_banks_),
      future_departure_counters_() {
  for (uint16_t i = 0; i < num_ports_; i++)
    for (uint16_t j = 0; j < num_ports_; j++)
      stats_[std::make_pair(i, j)] = 0;
}

void PSMSwitch::reset(const uint64_t tickno) {
  /* Reset op counts on memory banks */
  cell_memory_.reset();
  bypass_buffer_.reset();

  /* Clear out arrival counters */
  std::fill(current_arrival_counters_.begin(),
            current_arrival_counters_.end(),
            0);

  /* Clear out departure counters */
  std::fill(current_departure_counters_.begin(),
            current_departure_counters_.end(),
            0);

  /* Clear out departures that are no longer *future* (http://stackoverflow.com/a/16597048) */
  for (auto it = future_departure_counters_.begin(); it != future_departure_counters_.end(); ) {
    if (it->first <= tickno) {
      it = future_departure_counters_.erase(it);
    } else {
      ++it;
    }
  }

  /* Set current_departure_counters_ */
  for (uint16_t i = 0; i < output_queues_.size(); i++) {
    if (! output_queues_.at(i).empty()) {
      current_departure_counters_.at(output_queues_.at(i).front().bank_id())++;
      assert(current_departure_counters_.at(output_queues_.at(i).front().bank_id()) <=
             cell_memory_.mem_ops_per_tick());
    }
  }
}

/* Ingress routine */
void PSMSwitch::accept(const uint64_t tickno,
                       const Cell & cell) {
  uint64_t departure_time = tickno + output_queues_.at(cell.output()).size();
  if (departure_time == tickno) {
    Address address = bypass_buffer_.write(cell);
    output_queues_.at(cell.output()).push(address);
  } else {
    assert(departure_time > tickno);
    uint16_t free_bank_id = find_free_bank(departure_time);

    /* Increment arrival counters and future departures */
    current_arrival_counters_.at(free_bank_id)++;
    if (future_departure_counters_.find(departure_time) != future_departure_counters_.end()) {
      future_departure_counters_.at(departure_time).at(free_bank_id)++;
    } else {
      future_departure_counters_[departure_time] = std::vector<uint8_t>(num_banks_);
      future_departure_counters_.at(departure_time).at(free_bank_id) = 1;
    }
    assert(current_arrival_counters_.at(free_bank_id) <= cell_memory_.mem_ops_per_tick());

    Address address = cell_memory_.write(cell, free_bank_id);
    output_queues_.at(cell.output()).push(address);
  }
}

uint16_t PSMSwitch::find_free_bank(const uint64_t departure_time) const {
  /* Search all banks */
  for (uint16_t i = 0; i < num_banks_; i++) {
    /* Check for conflicts in the current time slot */
    auto already_scheduled_ops = current_departure_counters_.at(i) +
                                 current_arrival_counters_.at(i);
    assert (already_scheduled_ops <= cell_memory_.mem_ops_per_tick());
    if (already_scheduled_ops == cell_memory_.mem_ops_per_tick()) continue;

    /* Check for conflicts when you depart */
    uint16_t already_scheduled_future_departures = 0;
    if (future_departure_counters_.find(departure_time) != future_departure_counters_.end()) {
      already_scheduled_future_departures = future_departure_counters_.at(departure_time).at(i);
    } else {
      already_scheduled_future_departures = 0;
    }
    assert (already_scheduled_future_departures <= cell_memory_.mem_ops_per_tick());
    if (already_scheduled_future_departures == cell_memory_.mem_ops_per_tick()) continue;

    /* Doesn't conflict */
    return i;
  }
  assert(false);
  return UINT16_MAX;
}

void PSMSwitch::tick(const uint64_t tickno __attribute__((unused))) {
  for (auto &x : output_queues_) {
    if (x.empty()) continue;
    Address hol = x.front();
    auto cell = (hol.bank_id() == UINT16_MAX) ? bypass_buffer_.read(x.front()) :
                                                cell_memory_.read(x.front());
    stats_[std::make_pair(cell.input(), cell.output())]++;
    x.pop();
  }
}

void PSMSwitch::output_stats(void) const {
  for (auto &x : stats_) {
    printf("%u -> %u : %lu pkts\n",
           x.first.first, x.first.second, x.second);
  }
}
