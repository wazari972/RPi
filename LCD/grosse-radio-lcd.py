#! /usr/bin/env python

from lxml.html import html5parser
from httplib2 import Http
from time import sleep
import time

from Adafruit.CharLCDPlate import Adafruit_CharLCDPlate

URL = "http://www.lagrosseradio.com/playerLGR/ajax_player.php?id_radio=3"
h = Http("")

def getNameTitle():
    response, content = h.request(URL+"?dt="+str(time.time()), 'POST')
    content = html5parser.fromstring(content)

    name = content.findall("*")[3].text
    title = content.findall("*")[5].text
    
    return name, title


lcd = Adafruit_CharLCDPlate(busnum = 1)
lcd.begin(16, 2)
lcd.clear()

old = None
message = "Loading"
while 1:
    lcd.clear()
    lcd.message(message)
    lcd.backlight(lcd.GREEN)
    
    message = "\n".join(getNameTitle())
    
    lcd.clear()
    lcd.message(message)

    if message != old:
	lcd.backlight(lcd.YELLOW)
        print message
        print "----"
    else:
	lcd.backlight(lcd.OFF)
    old = message

    for i in range(30):
        if lcd.buttonPressed(lcd.SELECT) or lcd.buttonPressed(lcd.UP) :
            lcd.clear()
            lcd.message(message)
            lcd.backlight(lcd.ON)
        elif lcd.buttonPressed(lcd.DOWN):
            lcd.clear()
            lcd.message(message)
            lcd.backlight(lcd.OFF)
        sleep(1)
