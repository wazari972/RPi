#Daniel Juenger, github.com/sleeepyjack

from time import sleep
import commands
import psutil

COLUMNS = 16

class Element:
    def __init__(self, parent, name, type_=Menu.STRING, once=False, content=None, color=None, confirm=False):
        self.parent = parent
        self.name = name
        self.type = type_
        self.content = content
        self.color = color
        self.once = once
        self.execution_msg = None
        self.confirm = confirm
        self.children = []

        self.isTop = not isinstance(parent, Element)

        if self.isTop:
            prev = (COLUMNS - 2 - len(name)) / 2
            after = prev if 2 * prev == COLUMNS else prev + 1
            self.longName = "<%s%s%s>" % (" " * prev, name, " " * after)
        else:
            self.longName = "%s>%s" % (self.parent.name, self.name)
        
        if not self.content:
            prev = (COLUMNS - 2 - 1) / 2
            after = prev if 2 * prev == COLUMNS else prev + 1
            self.content = "%sV%s" % (" " * prev, " " * after)
            
        self.parent.declareChild(self)

    def declareChild(self, child):
        self.children.append(child)

class Menu():
    STRING = "STRING"
    PYTHON = "PYTHON"
    BASH = "BASH"
    
    def __init__(self, lcd, defaultColor):
        self.lcd = lcd
        self.isInterrupted = False
        self.isOn = True
        self.isOnCount = 0
        self.defaultColor = defaultColor
        
        self.currentElement = None
        self.children = []

    def declareChild(self, child):
        self.children.append(child)
	
    def buttonPressed(self):
        return (self.lcd.buttonPressed(self.lcd.SELECT) or
                self.lcd.buttonPressed(self.lcd.UP)     or
                self.lcd.buttonPressed(self.lcd.DOWN)   or
                self.lcd.buttonPressed(self.lcd.LEFT)   or
                self.lcd.buttonPressed(self.lcd.RIGHT))

    def __clearMenuSide(self, right=True):
        for i in xrange(16):
            if right: self.lcd.scrollDisplayRight()
            else: self.lcd.scrollDisplayLeft()
            sleep(.03)

    def __returnToTopElement(self):
        while self.currentElement.parent != self:
            self.currentElement = self.currentElement.parent
		
    def __firstTopElement(self):
        self.currentElement = self.children[0]

    def __nextPrevTopElement(self, do_next):
	self.__returnToTopElement()
        currentIndex = self.children.index(self.currentElement)
        inc = 1 if do_next else -1
        newIndex = (len(self.children) + currentIndex + inc) % len(self.children)
        self.currentElement = self.children[newIndex]

    def __nextTopElement(self):
        self.__nextPrevTopElement(do_next=True)
        
    def __prevTopElement(self):
        self.__nextPrevTopElement(do_next=False)

    def __nextPrevSubElement(self, do_next):
        if self.currentElement.parent == self:
            self.currentElement = self.currentElement.children[0]
            return

        subelements = self.currentElement.parent.children
        currentIndex = subelements.index(self.currentElement)
        inc = 1 if do_next else -1
        newIndex = currentIndex + inc
        
        if newIndex in (0, len(subelements)):
            self.__returnToTopElement()
            return
        self.currentElement = subelements[newIndex]

    def __nextSubElement(self):
        self.__nextPrevSubElement(do_next=True)
        
    def __prevSubElement(self):
        self.__nextPrevSubElement(do_next=False)

    def __handleMenu(self):
	if self.isOn:
            if not self.once or not self.execution_msg:
                if self.currentElement.type == "STRING":
                    msg = self.currentElement.content
                elif self.currentElement.type == "PYTHON":
                    msg = str(eval(self.currentElement.content))
                elif self.currentElement.type == "BASH":
                    msg = commands.getoutput(self.currentElement.content)

                if self.once:
                    self.execution_msg = msg

            if self.once:
                msg = self.execution_msg
                    
	    self.lcd.clear()
            
            name = self.currentElement.longName
	    self.lcd.message(name + "\n" + msg)
            self.lcd.backlight(self.currentElement.color if self.currentElement.color else self.defaultColor)

    def startMenu(self):
        self.lcd.clear()
	self.lcd.backlight(self.defaultColor)
        
	self.isOn = True
	self.isOnCount = 0
	self.isInterrupted = False

        self.__firstTopElement()
	self.__handleMenu()
        
	while not self.isInterrupted:
	    try:
    		if self.isOn:
                    if self.buttonPressed():
                        self.isOnCount = 0
                        if self.lcd.buttonPressed(self.lcd.RIGHT):
                            self.__nextTopElement()
                        elif self.lcd.buttonPressed(self.lcd.LEFT):
                            self.__prevTopElement()
                        elif self.lcd.buttonPressed(self.lcd.DOWN):
                            self.__nextSubElement()
                        elif self.lcd.buttonPressed(self.lcd.UP):
                            self.__prevSubElement()
                        elif self.lcd.buttonPressed(self.lcd.SELECT):
                            self.__returnToTopElement()

                    self.__handleMenu()
                    self.isOnCount += 1
                    
                    if self.isOnCount > 100:
                        self.lcd.backlight(self.lcd.OFF)
                        self.lcd.noDisplay()
                        self.isOn = False
                    
                    sleep(.3)
    		else:
                    if self.buttonPressed():
                        self.lcd.display()
                        self.lcd.backlight(self.defaultColor)
                        self.isOnCount = 0
                        self.isOn = True
                        sleep(.3)
                        
	    except KeyboardInterrupt:
		self.stopMenu()
                
    def stopMenu(self):
	self.lcd.backlight(self.lcd.OFF)
	self.lcd.noDisplay()
	self.isInterrupted = True

