#!/bin/zsh

() {
# globs with no match won't cause an error
setopt nullglob

# Preferences
local REMOTEPATH="/mnt/lacie/bors"
local LOCALPATH="$HOME/docs/bors"
local DROPBOX="$HOME/Dropbox/bors"

local TYPENAME=""

local relname() {
	echo $PWD | sed -e "s=^$REMOTEPATH=="
}

local copy() {
	echo $LOCALPATH$(relname)
	cp -v -n --preserve=timestamps $* $LOCALPATH$(relname)
	echo "copy done"
}


local tar_day() {
	local DATE=$1
	local NAME=$TYPENAME.$DATE.$2.tar
	echo "\nTarring $DATE"
	if ! [[ -f "$NAME" ]]; then
		tar --remove-files -vcf $NAME *$DATE.$2
	else 
		echo "Already done $NAME"
	fi
}

local tar_days() {
	local i=-1
	while ((i++ < 400)); do
		local DATE=$(date -d "$i days ago" "+%F")
		local DAY=$(date -d "$DATE" "+%a")
		echo $i
		if [[ $DAY != Sun && $DAY != Sat ]]; then
			# from stackoverflow should be possible to use the nullglob
			local FILE=$(find . -maxdepth 1 -name "*$DATE.$1" -print -quit)
			echo $FILE
			if test -f "$FILE"; then
				tar_day $DATE $1
			else
				break 
			fi
			
		fi
	done
}

local tar_gzip_copy() {
	echo "starting copy and gzip"
	copy *csv
	tar_days csv
	cd xls
	tar_days xls
	gzip --force --verbose *tar
	copy *gz
	cd ..
}

local xls_to_csv_and_clean() {
	local ERROR=()
	if ! [[ -d xls ]]; then
		mkdir xls
	fi

	local xls
	for xls in *.xls; do
		CSV=${xls/.xls/.csv}
		echo $CSV
		out=$(xls2csv $xls)
		if  [[ 0 == $? || -e $CSV ]]; then
			mv $xls xls
			sed -i -e "3s/^Date.*//" -e "/^\w*$/d" $CSV
			sleep 4
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
		gzip -c *$TODAY.csv.tar > $DROPBOX/intraday.$TODAY.csv.tar.gz
	done

fi
}
