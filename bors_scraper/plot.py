#!/usr/bin/env python

from matplotlib.pyplot import *
from matplotlib.dates import date2num
from datetime import datetime
from numpy import array, sum
import argparse
from glob import glob
from csv import reader

opts = argparse.ArgumentParser(description='Plot graphs for different tickers')

opts.add_argument('tickers', metavar='TICKER', type=str, nargs='+',
		help='The tickers you want to plot')

args = opts.parse_args()
data = []
tickers = []
for ticker in (x.upper() for x in args.tickers):
	data.extend(glob(ticker + '.daily*.csv'))
	tickers.append(ticker)

strptime = datetime.strptime

style={'linestyle': '-', 'marker': None}
colors = ['b', 'g', 'c', 'm', 'y', 'k', 'w']

for d in data:
	d = [x for x in reader(open(d))]

	columns = zip(*d[2:])

	dates = [date2num(strptime(d, "%d.%m.%y")) for d in columns[0]]
	dates = array(dates)
	prices = list(columns[1])

	print 'tickers: ' + str(tickers)
	style['label'] = tickers[0]; del tickers[0]
	style['color'] = colors[0]; del colors[0]
	print style

	for i, v in enumerate(prices):
		prices[i] = float(v) if len(v) > 0 else float(prices[i-1])
	prices = array(prices)

	plot_date(dates, prices, **style)

show()
