#! /usr/bin/env python2

#Daniel Juenger, github.com/sleeepyjack

from time import sleep
from CharPlate import CharPlate
from LCDMenu.menu import Menu

lcd = CharPlate()
menu = Menu()

#The menu can show strings, bash and python expressions

# topElement( Name , Type of content , Lower row content)

network = menu.topElement("< Network >", "STRING", " v")
net_ip = menu.subElement("Network>IP", "BASH", "ping -c 1 $(ip r | grep default | cut -d ' ' -f 3) | grep from | cut -d' ' -f4 | cut -d: -f 1")

system = menu.topElement("< System >", "STRING", " v")
sys_cpu = menu.subElement("System>CPU", "PYTHON", 'str(str(psutil.cpu_percent()) + "%")')
sys_tmp = menu.subElement("System>CPU-Temp.", "BASH", "cat /sys/class/thermal/thermal_zone0/temp | cut -b-2")
sys_ram = menu.subElement("System>RAM", "PYTHON", 'str(str(psutil.phymem_usage()[3])+"% used")')

radio = menu.topElement("< Radio >", "STRING", " v (todo)", lcd.GREEN)
radio_reggae = menu.subElement("Radio>Grosse Radio", "STRING", 'http://hd.lagrosseradio.info:8300/')

power = menu.topElement("< Power Off >", "STRING", " v", lcd.RED)
power_off = menu.subElement("Power>Off", "BASH", 'sudo poweroff')

#Adding elements to the menu
for top, subs in ((radio, ()),
                  (network, [net_ip]),
                  (system, [sys_cpu, sys_tmp, sys_ram]),
                  (power, [power_off])):
    menu.addTopElement(top)
    for subel in subs:
        menu.addSubElement(top, subel)

color = lcd.TEAL

#initializing display
lcd.clear()
lcd.backlight(color)

#little loading animation
i = 0
lcd.message("LOADING\n")
while(i < 16):
    lcd.message(chr(219))
    sleep(.1)
    i += 1

#starting the menu
menu.startMenu(lcd, color)
