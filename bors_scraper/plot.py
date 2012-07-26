#!/usr/bin/env python

from subprocess import check_output
from matplotlib.pyplot import *
from matplotlib.dates import date2num
from datetime import datetime
from numpy import array, sum
import argparse
from glob import glob
from csv import reader

def normalize(array):
	return 100*array/array[0]

opts = argparse.ArgumentParser(description='Plot graphs for different tickers')

opts.add_argument('tickers', metavar='TICKER', type=str, nargs='+',
		help='The tickers you want to plot')
opts.add_argument('--normalize', '-n', dest='normalize', default=lambda x: x,
		const=normalize, action='store_const',
		help='Normalize the start values of the tickers')
opts.add_argument('--from', '-f', type=str, dest='start',
		help='From when you want the plot to start, defaults to as far back as possible. Specify in date\'s humanreadable form')
opts.add_argument('--to', '-t', type=str, dest='to',
		help='When you want to the plot to stop, defaults to the current date.Specify in date\'s humanreadable form.')

args = opts.parse_args()
data = []
tickers = []
for ticker in (x.upper() for x in args.tickers):
	data.extend(glob(ticker + '.daily*.csv'))
	tickers.append(ticker)

strptime = datetime.strptime

def get_date(string):
	date = check_output(['date', '-d', string, '+%F'])
	return date2num(datetime(*(int(x) for x in date.split('-'))))

def get_index(date, dates):
	for i, v in enumerate(dates):
		if v >= date:
			break
	return i

def strp2num(d):
	return date2num(strptime(d, "%Y-%m-%d"))

def str2float(s):
#	print 'string: "' + str(len(s)) +'"'
	return float(s) if len(s) > 0 else 0

def parse_columns(li, form):
	columns = zip(*li)
	for i, v in enumerate(columns):
		if len(form) > i and form[i] != None:
			columns[i] = [form[i](x) for x in v]
	return columns


style={'linestyle': '-', 'marker': None}
colors = ['b', 'g', 'c', 'm', 'y', 'k', 'w']

for d in data:
	d = open(d); d.readline(); d.readline()
	d = (x for x in reader(d))

	forms = [strp2num, str2float]
	dates, prices = parse_columns(d, forms)[0:2]

	i = 0
	while i < len(prices):
		if  prices[i] == 0:
			del prices[i], dates[i]
			continue
		i += 1

	if args.start != None:
		start = get_date(args.start)
		i = get_index(start, dates)
		dates, prices = dates[i:], prices[i:]
	if args.to !=None:
		to = get_date(args.to)
		i = get_index(to, dates)
		dates, prices = dates[:i+1], prices[:i+1]

	style['color'] = colors[0]; del colors[0]

	prices = args.normalize(array(prices))

	plot_date(dates, prices, **style)

grid(True)
legend(tickers)
show()
