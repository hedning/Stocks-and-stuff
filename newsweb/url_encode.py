import sys
import urllib

kvs = []

for kv in sys.argv[1:]:
	kvs.append(tuple(kv.split("=", 1)))

print urllib.urlencode(kvs)
