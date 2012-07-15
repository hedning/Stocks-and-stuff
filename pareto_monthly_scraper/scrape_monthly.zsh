#!/usr/bin/env zsh
() {
local syncfolder=$PWD
if [[ -n $1 ]]; then
	syncfolder=$1
fi
cd $syncfolder

local cookie=$syncfolder/cookie.txt
# Save your userlogin in auth.txt as postdata in the form:
# username=$user&password=$pass&cmd=4
local post='auth.txt'
local action='Default.aspx'

local base='https://paretoforvaltning.no/'
local file='Download.aspx?file='
local porto='&portifolio=skip_'
local lang='&onlynorwegian=true'
local url=''

wget --post-file $post --save-cookies $cookie --keep-session-cookies $base$action -O - > /dev/null 2> scrape.log

local p=""
local i=-1
for p in 'ingrid' 'varp'; do
	if ! [[ -d $p ]]; then
		mkdir $p
	fi
	cd $p
	while ((++i >= 0)); do
		local name=M$(date -d "$i month ago" "+%Y%m").pdf
		if [[ -f $name ]]; then
			echo "$name already downloaded, presuming $p is up to date."
			break
		fi
		url=$base$file$name$porto$p[1]$lang
		wget --load-cookies $cookie $url --output-document $name
		if [[ $? == 8 ]]; then
			echo "$name not found on server"
			rm $name
			break
		fi
	done
	i=-1
	cd ..
done

} $*
