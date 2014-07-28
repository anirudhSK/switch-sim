#! /bin/bash

./src/switch_sim 64 1 10000 1 128 > /tmp/output
diff /tmp/output unittests/64.1.10000.output
