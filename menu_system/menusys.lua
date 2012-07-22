
-- mode input
local ticker="WWI"
local quarter="1"
local year="2012"
local sectors="car-shipping"
local ext_script = "/home/ole/src/scrapers/oslo-bors/menu_system/menusys.py "

local config_path = os.getenv("HOME").."/.stock-key-numbers"

-- fincancial items def
local all_keylist_file
local tag_file

local default_keys = {"EBIDTA", "EBIT", "income", "expenses", "equity", "debt"}

local function log(str)
	debug.log(str)
end

---- generic utils

-- incomplete shell quoteing
local function shell_quote(str)
	return "'"..str.gsub("'", "\\'").."' "
end

local function cmd(shell_str)
	log("running shell command: "..shell_str)
	local stdout = io.popen(shell_str)
	local output = ""
	for line in stdout:lines() do
		output = output..line
	end
	return output, stdout:close()
end

local function get_clipboard() 
	return cmd("xclip -out")
end

local function read_lines(path)
	local file, error_message = io.open(path)
	local lines = {}
	if file == nil then
		log("Path not found: "..path.."error: "..error_message)
		return lines
	end

	for line in file:lines() do
		table.insert(lines, line)
	end
	file:close()
	return lines
end

local function append_to_file(path, ...)
	local file, error_message = io.open(path, "a")
	if file == nil then
		log("Error appending to "..path.." error: "..error_message)
		return
	end
	local args = {...}
	for i, line in ipairs(args) do
		file:write(line,"\n")
	end
	file:close()
end



local function load_keys(ticker)
	local ticker_specific = read_lines(config_path.."/"..ticker..".keys")
	local keys = {}
	table.icat(keys, default_keys)
	table.icat(keys, ticker_specific)
	return keys
	--return table.pack(table.unpack(default_keys), table.unpack(ticker_specific))
end

function join_with_separator(sep, ...)
	return table.concat({...}, sep)
end

local function commit_data(key, value)
	value = "'"..value:gsub("'", "\\'").."'"
	log("commiting data: "..key.."="..value)
	notioncore.exec(
		join_with_separator(" ", ext_script, key, value, ticker, year, quarter))
end

local function do_menuentry(key)
	local raw_value = get_clipboard()
	commit_data(key, raw_value)
end


local function build_menu()
	local keylist = load_keys(ticker)
	local menu = {}
	for i,key in ipairs(keylist) do
		-- is the menu/menu name supplied to the handler function?
		table.insert(menu, notioncore.menuentry(key, function() do_menuentry(key) end))
	end

	return menu
end

local function commit_new_keyvalue_def(mplex, keyvalue_name)
	append_to_file(config_path.."/"..ticker..".keys", keyvalue_name)
	do_menuentry(keyvalue_name)
end

function query_new_key_value(mplex)
	mod_query.query(mplex, "New keyvalue name: ", "", commit_new_keyvalue_def)
end

notioncore.defmenu("keyvalues", build_menu)


defbindings("WScreen", {
	submap(META.."J", {
		kpress("AnyModifier+J", "mod_menu.menu(_, _sub, 'keyvalues')"),
		kpress("AnyModifier+K", "query_new_key_value(_)")
	})
})

defbindings("WMenu", {
	mclick("Button1", "WMenu.finish(_)")
})

