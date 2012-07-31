#!/usr/bin/env python

import fileinput
from sys import stdout
import csv
import re
from argparse import ArgumentParser

parser = ArgumentParser(description="strip commas, ',', from numbers in csv files")

parser.add_argument('-i', '--in-place', dest='in_place', action='store_true',
		help='modify files in place.')
parser.add_argument('file', nargs='+')

arguments = parser.parse_args()

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
	out = open(name, 'w') if arguments.in_place else stdout
	writer = csv.writer(out)
	writer.writerows(data)

for name in arguments.file:
	stripfi(name)
