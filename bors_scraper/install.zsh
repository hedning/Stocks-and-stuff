#!/usr/bin/env zsh
DIR=$HOME/bin

if ! [[ -f $HOME/.borsscrape ]]; then
	echo "Installing preferences in $HOME/.borsscraperc"
	cp PREFERENCES $HOME/.borsscraperc
fi

. $HOME/.borsscraperc

if ! [[ -d $REPO ]]; then
	mkdir $REPO
fi

for i in *.zsh *.py; do
	echo "Installing $i in $REPO"
	cp $i $REPO
done

git show | head -n 1 > $REPO/version
