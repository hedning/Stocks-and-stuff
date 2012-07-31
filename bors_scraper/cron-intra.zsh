#!/bin/zsh

. $HOME/.borsscraperc

for type in index-intraday intraday; do
	if ![[ -d $type ]]; then
		mkdir $type
	fi
done


cd $REPO/index-intraday
if [[ -f ../ticker-lists/indexes ]]; then
	../do-list-delay.zsh ../get-index-intraday.zsh < ../ticker-lists/indexes &>> ../log
fi

cd $REPO/intraday
../do-list-delay.zsh ../get-ticker-intraday.zsh < ../ticker-lists/oslo-bors-tickers &>> ../log

