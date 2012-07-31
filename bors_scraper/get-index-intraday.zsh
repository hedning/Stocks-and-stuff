#!/bin/zsh

IFS=$'\n\t'

TICKER=$1

URL="http://oslobors.no/markedsaktivitet/servlets/newt/tradesExcel-stockIndex?ticker=${TICKER}&exch=ose&period=intraday&start=&stop="

wget "$URL" -O ${TICKER}.index.intraday.$(date +%F).xls
