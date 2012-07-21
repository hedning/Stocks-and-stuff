#!/usr/bin/env python

from matplotlib.pyplot import *
from matplotlib.dates import date2num
from datetime import datetime
from sys import argv
from glob import glob
from csv import reader

strptime = datetime.strptime

data = []
tickers = []
for ticker in argv[1:]:
	ticker = ticker.upper()
	data.extend(glob(ticker + '.daily*.csv'))
	tickers.append(ticker)

print data

style={'linestyle': '-', 'marker': None}
colors = ['b', 'g', 'c', 'm', 'y', 'k', 'w']

for d in data:
	d = [x for x in reader(open(d))]

	columns = zip(*d[2:])

	dates = columns[0]
	dates = [date2num(strptime(d, "%d.%m.%y")) for d in dates]
	prices = list(columns[1])

	print 'tickers: ' + str(tickers)
	style['label'] = tickers[0]; del tickers[0]
	style['color'] = colors[0]; del colors[0]
	print style

	for i, v in enumerate(prices):
		prices[i] = float(v) if len(v) > 0 else float(prices[i-1])

	plot_date(dates, prices, **style)

show()
