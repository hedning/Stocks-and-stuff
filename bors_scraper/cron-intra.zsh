#!/bin/zsh

PATH=$PATH:$HOME/bin


xls_to_csv_and_clean() {
ERROR=()
	if ! [[ -d xls ]]; then
		mkdir xls
	fi

	for xls in *.xls; do
		out=$(xls2csv $xls)
		if  [[ 0 == $? || -e ${xls/.xls#/.csv} ]]; then
			mv $xls xls
		else
			ERROR+=out
		fi
	done
	if [[ $#ERROR -gt 0 ]]; then
		echo "$ERROR" > xls_to_csv.log
	fi
}


cd ~/docs/oslo-bors/index-intraday
../do-list-delay.zsh ../get-index-intraday.zsh < ../ticker-lists/indexes &>> ../log
xls_to_csv_and_clean

cd ~/docs/oslo-bors/intraday
../do-list-delay.zsh ../get-ticker-intraday.zsh < ../ticker-lists/oslo-bors-tickers &>> ../log
xls_to_csv_and_clean
