#! /usr/bin/env python

import sys

from Adafruit.CharLCDPlate import Adafruit_CharLCDPlate

lcd = Adafruit_CharLCDPlate(debug=True)
lcd.begin(16, 2)
#lcd.clear()

message = sys.argv[1] + "\n" + sys.argv[2]
print message
lcd.message(message)

col = (('Red' , lcd.RED) , ('Yellow', lcd.YELLOW), ('Green' , lcd.GREEN),
           ('Teal', lcd.TEAL), ('Blue' , lcd.BLUE) , ('Violet', lcd.VIOLET),
           ('Off' , lcd.OFF) , ('On' , lcd.ON))


try:
  color = col[int(sys.argv[1])]
  lcd.backlight(color[1])
  print color[0]
except:
  lcd.backlight(lcd.ON)

