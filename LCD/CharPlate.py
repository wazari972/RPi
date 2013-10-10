import subprocess
import time

import sys
import select
import os, fcntl

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


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
	self.cursor = [0, 0]
        self.cells = None
        self.cols = -1
        self.lines = -1
        
        self.buttons = [0]*(ConsoleCharPlate.LAST + 1)
        self.fifo = open("commands.fifo", 'r')
        fcntl.fcntl(self.fifo, fcntl.F_SETFL, os.O_NONBLOCK)
        
    def begin(self, cols, lines):
        subprocess.Popen(['tput', "sc"]).communicate()
        self.cols = cols
        self.lines = lines
        self.clear()
        
    def clear(self):
        self.cells = [[" "] * self.cols for i in xrange(self.lines)]
        self.return_home()
	#self.refreshDisplay()

    def return_display(self):
        subprocess.Popen(['tput', "rc"]).communicate()
        subprocess.Popen(['tput', "ed"]).communicate()
        
    def return_home(self):
        self.return_display()
        self.cursor[:] = 0, 0
        
    def backlight(self, color):
        self.color = color
        self.refreshDisplay()
        
    def message(self, msg):
        for lno, line in enumerate(msg.split("\n")):
            if lno != 0:
                self.cursor[1] += 1
                self.cursor[0] = 0
            if self.cursor[1] >= self.lines:
                break

            for char in line:
                if self.cursor[0] >= self.cols:
                    break

                self.cells[self.cursor[1]][self.cursor[0]] = char
                self.cursor[0] += 1
        self.refreshDisplay()
        
    def refreshDisplay(self):        
        self.return_display()
        print self.color \
            + "\n".join([''.join(l) for l in self.cells]) \
            + ConsoleCharPlate.ENDC

    def buttonPressed(self, b):
        try:
            line = self.fifo.read()
            for l in line[:-1].split("\n"):
                if l in ("up", "u", "^[[A", "8"):
                    self.buttons[ConsoleCharPlate.UP] = True
                elif l in ("down", "d", "^[[B", "2"):
                    self.buttons[ConsoleCharPlate.DOWN] = True
                elif l in ("left", "l", "^[[D", "4"):
                    self.buttons[ConsoleCharPlate.LEFT] = True
                elif l in ("right", "r", "^[[C", "6"):
                    self.buttons[ConsoleCharPlate.RIGHT] = True
                elif l in ("select", "s", " ", "5"):
                    self.buttons[ConsoleCharPlate.SELECT] = True
                
        except:
            pass

        if self.buttons[b]:
            self.buttons[b] = False
            return True
        else:
            return False
            
    def scrollDisplayRight(self):
        for line in self.cells:
            line[:] = [" "] + line[:-1]
        self.refreshDisplay()
        
    def scrollDisplayLeft(self):
        for line in self.cells:
            line[:] = line[1:] + [" "]
        self.refreshDisplay()
        
    def noDisplay(self):
        self.clear()
        self.message("Display\noff")

    def display(self):
        self.clear()
        
try:
    from Adafruit.CharLCDPlate import Adafruit_CharLCDPlate as CharPlate
except:
     CharPlate = ConsoleCharPlate
