#!/usr/bin/env python

from sys import argv, stdout
import csv
import re

digits = re.compile('\d|\.')

def strip(string):
	out = ""
	for i in string:
		if re.match(digits, i) != None:
			out += i
		elif i != ',':
			return string
	return out

def stripfi(name):
	data = [[strip(s) for s in x ]for x in csv.reader(open(name))]
	writer = csv.writer(stdout)
	writer.writerows(data)

for name in argv[1:]:
	stripfi(name)
