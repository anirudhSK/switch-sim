#! /bin/bash

./src/switch_sim 64 1 10000 > /tmp/output
diff /tmp/output unittests/64.1.10000.output
