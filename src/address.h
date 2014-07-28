#ifndef SRC_ADDRESS_H_
#define SRC_ADDRESS_H_

// Copyright 2014 Anirudh Sivaraman

class Address {
 public:
  explicit Address(const uint16_t s_bank_id, const uint64_t s_addr)
      : bank_id_(s_bank_id),
        address_(s_addr) {}
  uint16_t bank_id(void) const { return bank_id_; }
  uint64_t address(void) const { return address_; }
  bool operator< (const Address & other) const {
    return (bank_id_ != other.bank_id_) ?
           bank_id_ < other.bank_id_    :
           address_ < other.address_;
  }

 private:
  uint16_t bank_id_;
  uint64_t address_;
};

#endif  // SRC_ADDRESS_H_
