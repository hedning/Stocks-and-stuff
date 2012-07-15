
-- mode input
local ticker="WWI"
local quarter="1"
local sectors="car-shipping"
local ext_script = "/home/ole/src/scrapers/oslo-bors/menu_system/menusys.py "

-- fincancial items def
local all_keylist_file
local tag_file

local default_keys = {"ebitda", "ebit", "income", "expenses"}

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


local function load_keylist(keylist)
	local file = io.open(keylist)
	out = {}
	for key in file:lines() do
		table.insert(out, key)
	end
	file:close()
	return out
end

local function get_keys(ticker)
	return default_keys
end

local function commit_data(key, value)
	value = "'"..value:gsub("'", "\\'").."' "
	log("commiting data: "..key.."="..value)
	notioncore.exec(ext_script..key..value.." "..ticker.." "..quarter)
end

local function do_menuentry(key)
	local raw_value = get_clipboard()
	commit_data(key, raw_value)
end

local function build_menu()
	local keylist = default_keys
	local menu = {}
	for i,key in ipairs(keylist) do
		-- is the menu/menu name supplied to the handler function?
		table.insert(menu, notioncore.menuentry(key, function() do_menuentry(key) end))
	end

	return menu
end

notioncore.defmenu("keyvalues", build_menu)


defbindings("WScreen", {
	kpress(META.."X", "mod_menu.menu(_, _sub, 'keyvalues')")
})
