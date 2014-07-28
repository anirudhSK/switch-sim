#! /bin/bash

./src/switch_sim 64 1 10000 1 128 > /tmp/output
diff /tmp/output unittests/64.1.10000.output

./src/switch_sim 64 1 10000 64 3 > /tmp/output
diff /tmp/output unittests/64.1.10000.output

./src/switch_sim 64 1 10000 64 2 > /tmp/output
diff /tmp/output unittests/64.1.10000.output
