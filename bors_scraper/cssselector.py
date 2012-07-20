#!/usr/bin/env python
from lxml.html import parse
from sys import argv, stdin

doc = stdin

if len(argv) > 1:
	selector = argv[1]

if len(argv) > 2:
	doc = argv[2] if argv[2] != "-" else stdin

try:
	root = parse(doc).getroot()
except:
	print argv[2] + " is not a file"

ticker_list = root.cssselect(selector)

for ticker in ticker_list:
	print ticker.text
