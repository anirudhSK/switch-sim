AM_CXXFLAGS = $(PICKY_CXXFLAGS)
LDADD = -lm

bin_PROGRAMS = switch_sim

common_source = ideal_switch.h ideal_switch.cc cell.h cell.cc random.cc random.h \
                traffic_generator.cc traffic_generator.h traffic_generator_templates.cc \
                psm_switch.h psm_switch.cc memory_bank.h memory_bank.cc \
                memory.cc memory.h

switch_sim_SOURCES = $(common_source) switch_sim.cc
