#!/bin/zsh
() {
# globs with no match won't cause an error
# this does weird ass shit
unsetopt nullglob

# Preferences
REMOTEPATH="/mnt/lacie/bors"
LOCALPATH="$HOME/docs/bors"
DROPBOX="$HOME/Dropbox/bors"

. $HOME/.borsscraperc

TYPENAME=""

relname() {
	echo $PWD | sed -e "s=^$REMOTEPATH=="
}

first_match() {
	find . -maxdepth 1 -name "$1" -print -quit
}

glob_exist() {
	match=$(first_match "$1")
	[[ -n "$match" ]]
}

copy() {
	echo "Starting to copy $*[1]"
	cp -v -n --preserve=timestamps $* $LOCALPATH$(relname)
	echo "copy done"
}


tar_day() {
	DATE=$1
	NAME=$TYPENAME.$DATE.$2.tar
	echo "\nTarring $DATE"
	if ! [[ -f "$NAME" ]]; then
		tar -v --remove-files -vcf $NAME *$DATE.$2
	else 
		echo "Already done $NAME"
	fi
}

tar_days() {
	i=-1
	while ((++i > -1)); do
		DATE=$(date -d "$i days ago" "+%F")
		if glob_exist "*$DATE.$1"; then
			echo "Tarring $DATE"
			tar_day $DATE $1
		else
			if ! glob_exist "*.$1"; then
				echo "No $1 files to process"
				break
			fi
		fi
	done
}

tar_gzip_copy() {
	echo "\nStarting copy and gzip in $PWD"
	if glob_exist "*.csv"; then
		copy *.csv
	fi
	tar_days csv
	echo "Entering xls"
	cd xls
	tar_days xls
	if glob_exist "*.tar"; then
		gzip --verbose *.tar
	fi
	if glob_exist "*gz"; then
		copy *gz
	fi
	cd ..
	echo "Done tarring and moving in $TYPENAME"
}

xls_to_csv_and_clean() {
	local ERROR=()
	if ! [[ -d xls ]]; then
		mkdir xls
	fi

	if ! glob_exist "*.xls"; then
		return 
	fi
	for xls in *.xls; do
		CSV=${xls/.xls/.csv}
		echo $CSV
		out=$(xls2csv $xls)
		if  [[ 0 == $? || -e $CSV ]]; then
			mv $xls xls
			sed -i -e "3s/^Date.*//" -e "/^\w*$/d" $CSV
			tr -d '\r' < $CSV | sponge $CSV
			$LOCALPATH/stripcomma.py -i $CSV
			sed -i -r 's/([0-9]{2}).([0-9]{2}).([0-9]{2})/20\3-\2-\1/' $CSV
		else
			ERROR+=out
		fi
	done
	if [[ $#ERROR -gt 0 ]]; then
		echo "$ERROR" > xls_to_csv.log
	fi
}


if cd $REMOTEPATH; then 

	local TODAY=$(date "+%F")
	for i in index-intraday intraday; do
		TYPENAME=$i
		cd $REMOTEPATH/$i
		xls_to_csv_and_clean
		tar_gzip_copy
		if [[ -f $(first_match "*$TODAY.csv.tar") ]]; then
			gzip -c *$TODAY.csv.tar > $DROPBOX/$TYPENAME.$TODAY.csv.tar.gz
		fi
	done

fi
} $*
