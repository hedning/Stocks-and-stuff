#!/bin/sh

. $HOME/.borsscraperc 
DIR="$HOME/bin"

echo "Installing in $DIR"
cp sync_and_clean_bors.zsh $DIR/sync_and_clean_bors
cp stripcomma.py $REPO/
