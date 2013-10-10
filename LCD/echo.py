#! /usr/bin/env python2

import sys

from CharPlate import CharPlate

lcd = CharPlate(debug=True)
lcd.begin(16, 2)
#lcd.clear()

message = sys.argv[1] + "\n" + sys.argv[2]
lcd.message(message)

col = (('Red' , lcd.RED) , ('Yellow', lcd.YELLOW), ('Green' , lcd.GREEN),
           ('Teal', lcd.TEAL), ('Blue' , lcd.BLUE) , ('Violet', lcd.VIOLET),
           ('Off' , lcd.OFF) , ('On' , lcd.ON))


try:
  color = col[int(sys.argv[1])]
  lcd.backlight(color[1])
except:
  lcd.backlight(lcd.ON)


  
