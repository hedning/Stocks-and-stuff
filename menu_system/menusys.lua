
# mode input
local ticker
local quarter
local sectors
local ext_script = "menusys.py "

# fincancial items def
local all_keylist_file
local tag_file


local function get_keylist(keylist)
	local file = io.open(keylist)
	out = {}
	for i in file:lines() do
		table.insert(out, i)
	end
	return out
end


local function build_menu(keylist)
	local menu = {}
	return menu
end


local function commit_data(key, value)
	value = "'"..value.gsub("'", "\\'").."' "
	notioncore.exec(ext_script..key..value.." "..ticker.." "..quarter)
end
