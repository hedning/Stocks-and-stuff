#!/bin/zsh

MINDELAY=9
MAXDELAY=20
RANDOM_SCALE=$(( 32767/(MAXDELAY-MINDELAY) ))

SHUFFLE="cat -"
if [[ -x /usr/bin/shuf ]]; then
	SHUFFLE="/usr/bin/shuf"
fi

ERROR=()

$=SHUFFLE | while read ARG; do
	if "$@" $ARG; then
		echo $ARG >> do-list-$(basename $1)-$(date +%F).log
	else
		ERROR+=$ARG
	fi
	sleep $(( RANDOM/RANDOM_SCALE + MINDELAY ))
done

if [[ $#ERROR -gt 0 ]]; then
	echo "Error during:\n$ERROR" 1<&2
	exit 1;
fi
