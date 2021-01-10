local utils = require("mp.utils")
local mpopts = require("mp.options")

prev_sub_text = nil

local BinaryFormat = package.cpath:match("%p[\\|/]?%p(%a+)")
if BinaryFormat == "dll" then
    function os.name()
        return "Windows"
    end
elseif BinaryFormat == "so" then
    function os.name()
        return "Linux"
    end
elseif BinaryFormat == "dylib" then
    function os.name()
        return "MacOS"
    end
end
BinaryFormat = nil

function enable_subtitle_timer()
    if timer:is_enabled() then
        timer:kill()

        mp.osd_message('['..os.name()..'] Subtitle UDP flood disabled.')
    else
        timer:resume()

        mp.osd_message('['..os.name()..'] Subtitle UDP flood enabled.')
    end
end

function retranslate_subtitles()
  local sub_text = mp.get_property('sub-text')

  if sub_text == prev_sub_text or sub_text == '' or sub_text == nil then
    return
  end

  prev_sub_text = sub_text

  if os.name() == 'MacOS' or os.name() == 'Linux' then
      io.popen('echo "'..sub_text..'" | nc -4u -w1 127.0.0.1 5005')
  else
      -- not yet implemented
      exit()
  end
end

mp.add_key_binding('ALT+SHIFT+s', enable_subtitle_timer)

timer = mp.add_periodic_timer(0.1, retranslate_subtitles)
timer:kill()