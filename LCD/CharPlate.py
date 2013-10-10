import subprocess
import time

import sys
import select
import os, fcntl

class ConsoleCharPlate:
    TXT_BLACK = '\033[30m'
    BLACK = '\033[40m'

    # LED colors
    OFF = BLACK
    RED = '\033[41m'
    GREEN = '\033[42m'
    BLUE = '\033[44m'
    YELLOW = '\033[43m' + TXT_BLACK    
    TEAL = '\033[46m' + TXT_BLACK
    VIOLET = '\033[45m'
    WHITE = '\033[47m' + TXT_BLACK
    ON = WHITE
    
    ENDC = '\033[0m'

    # Port expander input pin definitions
    SELECT                  = 0
    RIGHT                   = 1
    DOWN                    = 2
    UP                      = 3
    LEFT                    = 4
    LAST                    = LEFT
    
    def __init__(self, busnum=-1, addr=0x20, debug=False):
        self.color = ConsoleCharPlate.ON
	self.currline = 0
	self.lines = 0
        self.buttons = [0]*(ConsoleCharPlate.LAST + 1)
        self.fifo = open("commands.fifo", 'r')
        fcntl.fcntl(self.fifo, fcntl.F_SETFL, os.O_NONBLOCK)
        
    def begin(self, cols, lines):
        subprocess.Popen(['tput', "sc"]).communicate()
	self.numcols = cols
        self.numlines = lines
        self.clear()
	
    def clear(self):
	self.return_home()
	
    def return_home(self):
        subprocess.Popen(['tput', "rc"]).communicate()
        subprocess.Popen(['tput', "ed"]).communicate()

    def backlight(self, color):
        self.color = color

    def message(self, msg):
        self.return_home()
        print self.color + msg + ConsoleCharPlate.ENDC

    def buttonPressed(self, b):
        try:
            line = self.fifo.read()
            for l in line.split("\n"):
                self.buttons[int(l)] = True
        except:
            pass

        if self.buttons[b]:
            self.buttons[b] = False
            return True
        else:
            return False
            

    def noDisplay(self):
        self.message("Display\noff")

    def display(self):
        self.clear()
        
try:
    from Adafruit.CharLCDPlate import Adafruit_CharLCDPlate as CharPlate
except:
     CharPlate = ConsoleCharPlate
