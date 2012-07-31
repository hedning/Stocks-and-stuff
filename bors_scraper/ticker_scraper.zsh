#!/usr/bin/env zsh

. $HOME/.borsscraperc
url='http://www.oslobors.no/markedsaktivitet/stockList'

cd $REPO
if ! [[ -d ticker-lists ]]; then
	mkdir ticker-lists
fi
cd ticker-lists

selector='tbody.body td.c3 a'

wget "$url" -O - 2>> log | ../cssselector.py "$selector" | sort > oslo-bors-tickers.new

if [[ -s ticker-list.new ]]; then
	if diff oslo-bors-tickers oslo-bors-tickers.new; then
		mv oslo-bors-tickers oslo-bors-tickers.old
		mv oslo-bors-tickers.new oslo-bors-tickers
	fi
fi
