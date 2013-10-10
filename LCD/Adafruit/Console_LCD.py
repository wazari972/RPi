#! /usr/bin/python2

import subprocess
import time

class ConsoleLCD:
    TXT_BLACK = '\033[30m'
    
    BLUE = '\033[44m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m' + TXT_BLACK
    RED = '\033[41m'
    BLACK = '\033[40m'
    TEAL = '\033[46m' + TXT_BLACK
    VIOLET = '\033[45m'
    ON = '\033[47m' + TXT_BLACK
    OFF = BLACK

    ENDC = '\033[0m'
    
    def __init__(self):
        self.color = ConsoleLCD.TEAL

    def begin(self, row=0, col=0):
        subprocess.Popen(['tput', "sc"]).communicate()

    def clear(self):
        print "\n"

    def reset(self):
        subprocess.Popen(['tput', "rc"]).communicate()
        subprocess.Popen(['tput', "ed"]).communicate()

    def backlight(self, color):
        self.color = color

    def message(self, msg):
        self.reset()
        print self.color + msg + ConsoleLCD.ENDC

lcd = ConsoleLCD()
lcd.begin()

lcd.message("hello\nworld")
time.sleep(2)

lcd.backlight(lcd.ON)
lcd.message("salut\nca va")
time.sleep(2)

lcd.backlight(lcd.YELLOW)
lcd.message("salut\nca va")
