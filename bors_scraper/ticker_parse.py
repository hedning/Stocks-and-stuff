#!/usr/bin/env python
from lxml.html import parse
import sys

doc = sys.stdin

if len(sys.argv) > 1:
	doc = sys.argv[1] if sys.argv[1] != "-" else sys.stdin

try: 
	root = parse(doc).getroot()
except:
	print sys.argv[1] + " is not a file"

ticker_list = root.cssselect('tbody.body td.c3 a')

for ticker in ticker_list:
	print ticker.text
