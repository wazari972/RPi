#! /usr/bin/env python2

#Daniel Juenger, github.com/sleeepyjack

from time import sleep
from CharPlate import CharPlate
from LCDMenu.menu import Element, Menu

lcd = CharPlate()
menu = Menu(lcd, lcd.TEAL)

# The menu can show strings, bash and python expressions

network = Element(menu, "Network")
net_ip = Element(network, "IP", Menu.BASH, "/sbin/ifconfig eth0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'")

system = Element(menu, "System")
sys_cpu = Element(system, "CPU", Menu.PYTHON, 'str(str(psutil.cpu_percent()) + "%")')
sys_tmp = Element(system, "CPU-Temp.", Menu.BASH, "cat /sys/class/thermal/thermal_zone0/temp | cut -b-2")
sys_ram = Element(system, "RAM", Menu.PYTHON, 'str(str(psutil.phymem_usage()[3])+"% used")')

radio = Element(menu, "Radio", color=lcd.GREEN)
radio_reggae = Element(radio, "Grosse Radio", Menu.STRING, 'http://hd.lagrosseradio.info:8300/', once=True, confirm=True)

power = Element(menu, "Power", color=lcd.RED)
power_off = Element(power, "Off", Menu.BASH, 'echo sudo poweroff', confirm=True)

#initializing display
lcd.begin(16, 2)
lcd.backlight(lcd.TEAL)

#little loading animation
i = 0
lcd.message("LOADING\n")
while(i < 16):
    lcd.message("+")
    sleep(.1)
    i += 1

#starting the menu
menu.startMenu()
