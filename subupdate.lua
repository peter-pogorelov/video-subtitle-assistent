local utils = require("mp.utils")
local mpopts = require("mp.options")

prev_sub_text = nil

function retranslate_subtitles()
  local sub_text = mp.get_property('sub-text')

  if sub_text == prev_sub_text or sub_text == '' or sub_text == nil then
    return
  end

  prev_sub_text = sub_text

  io.popen('echo "'..sub_text..'" | nc -4u -w1 127.0.0.1 5005')
end


timer = mp.add_periodic_timer(0.1, retranslate_subtitles)