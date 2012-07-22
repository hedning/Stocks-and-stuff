#!/usr/bin/env python

import sys

out = open("key-numbers.db", "a")
out.write(" ".join(sys.argv[1:])+"\n")
out.close()
