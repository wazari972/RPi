#! /usr/bin/env python2

from lxml.html import html5parser
from httplib2 import Http
from time import sleep
import time

from CharPlate import CharPlate

URL = "http://www.lagrosseradio.com/playerLGR/ajax_player.php?id_radio=3"
SLEEP = 10

h = Http("")

def getNameTitle():
    response, content = h.request(URL+"?dt="+str(time.time()), 'POST')
    content = html5parser.fromstring(content)

    name = content.findall("*")[3].text
    title = content.findall("*")[5].text
    
    return name, title


lcd = CharPlate(busnum = 1)
lcd.begin(16, 2)
lcd.clear()

count = 0
old = None
message = "Loading"
while 1:
    lcd.clear()
    lcd.message(message)
    lcd.backlight(lcd.GREEN)
    
    message = "\n".join(getNameTitle())
    
    lcd.clear()

    if message != old:
        lcd.backlight(lcd.YELLOW)
        count = 0
    else:
        lcd.backlight(lcd.OFF)

    lcd.message(message)
    
    old = message
    
    for i in range(SLEEP):
        if lcd.buttonPressed(lcd.SELECT) or lcd.buttonPressed(lcd.UP):
            lcd.clear()
            lcd.backlight(lcd.ON)
        elif lcd.buttonPressed(lcd.DOWN):
            lcd.clear()
            lcd.backlight(lcd.OFF)
        count += 1
        lcd.message(str(count) + "s "+ message)
        sleep(1)
