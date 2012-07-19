#!/bin/zsh

IFS=$'\n\t'

# start stop date inclusive. Format: dd.mm.yyyy
DATEFORMAT="%d.%m.%y"

TICKER=$1
STOP=$(date +$DATEFORMAT)
shift
if [[ -n $1 ]]; then
	START=$(date +$DATEFORMAT --date="$1")
	shift
fi
if [[ -n $1 ]]; then
	STOP=$(date +$DATEFORMAT --date="$1")
	shift
fi

URL="http://oslobors.no/markedsaktivitet/servlets/newt/tradesExcel-stock?ticker=${TICKER}&exch=ose&period=&start=${START}&stop=${STOP}"

wget $URL -O ${TICKER}.${START}-${STOP}.xls
