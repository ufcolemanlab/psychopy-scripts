"""
Free-Moving Behavior Experiment
Usage:
In a separate file with FMB.py in path:
__________________________
from FMB import FMB
experiment = FMB()
experiment.training(screen = 1, reversals = 100, orientation = 45)
__________________________
or simply run this file and use the function call under 
__name__ == "main" at the bottom of the file.

Optional arguments:
screen=1,2 ; default 1
reversals=any positive integer ; default 100
orientation=any positive integer ; default 45
pin="low","high" ; default 'low'

By default, orientations 45 and 135 set the stimulus pin
to low and high respectively. If you specify some other
stimulus, you MUST specify a pin state as well, e.g.
training(screen = 1, reversals = 100, orientation = 90, pin = "high")

Under #Board the serial port is defined as '/dev/tty/ACM1' 
for linux and mac. For windows this should be 'COM1'.
This script is written for three monitors. To use some other 
setup you will need to change monitor width and wx_res under 
#monitor details and #Psychopy windows

Author: Jesse Trinity (Coleman Lab)
"""

import wx
from psychopy import visual, core, event, monitors
from pyfirmata import Arduino, util

#Open serial port
class FMB:
    
    
    
    def __init__(self):
        #board
        self.board = Arduino('/dev/tty/ACM1')
        self.it = util.Iterator(self.board)
        self.it.start()
        self.board.analog[0].enable_reporting()
    
    	#pins
        self.monitor_pin = self.board.get_pin('d:3:p') #is this pins 3?
        self.stim_pin = self.board.get_pin('d:6:p')
        self.off_on = self.board.get_pin('d:9:p')
        self.trigger = self.board.get_pin('d:5:p')
    
    	#monitor details
        self.app = wx.App(False)
        self.wx_res  = wx.GetDisplaySize()
        self.wx_PPI = wx.ScreenDC().GetPPI()
        self.monitor_width = (2.54 * self.wx_res[0]/self.wx_PPI[0])/3 #is this in cm? m?
        self.mon = monitors.Monitor("mymon", distance = 13, width = self.monitor_width)
        self.mon.currentCalib['sizePix'] = [self.wx_res[0], self.wx_res[1]]
        self.mon.saveMon()
        
        #Psychopy windows
        self.window1 = visual.Window(size=[self.wx_res[0]/3,self.wx_res[1]],monitor=self.mon, fullscr = False, units="deg", screen =1)
        self.window2 = visual.Window(size=[self.wx_res[0]/3,self.wx_res[1]],monitor=self.mon, fullscr = False, units="deg", screen =2)
        
        self.fixation1 = visual.GratingStim(win=self.window1, size=100, pos=[0,0], sf=0, color='gray')
        self.fixation2 = visual.GratingStim(win=self.window2, size=100, pos=[0,0], sf=0, color='gray')

  
    def habituation(self, time):
        habitTime = 1800 #added variable
        both_screens_gray(habitTime) #habitTime in seconds
        
    def training(self, **kwargs):
        #get parameters
        if "pin" in kwargs:
            if kwargs["pin"] == "high":
                pin = 1
            elif kwargs["pin"] == "low":
                pin = 0
            else:
                print("invalid pin state, use /'low/' or /'high/'")
                return
            
        if "orientation" in kwargs:
            orientation = kwargs["orientation"]
            if orientation == 135:
                pin = 1
            elif orientation == 45:
                pin = 0
            elif "pin" not in kwargs:
                print("you must specify a pin state")
                return
    
        else:
            print("defaulting to 45 degrees")
            orientation = 45
            pin = 0
            
            
        if "screen" in kwargs:
            if kwargs["screen"]==1:
                window = self.window1
                self.monitor_pin.write(0)
            elif kwargs["screen"]==2:
                window = self.window2
                self.monitor_pin.write(1)
            else:
                print("defaulting to screen 1")
                window = self.window1
                self.monitor_pin.write(0)
                
                
        if "reversals" in kwargs:
            reversals = kwargs["reversals"]
        else:
            reversals = 100
            
        stimulus = visual.GratingStim(tex = "sin", win=window, mask="circle", size=100, pos=[0,0], sf=0.05 , ori=(orientation))
        
        #procedure
        
        self.trigger.write(1.0)
        self.both_screens_gray(5.0)
        for i in range(5):
            self.stim_pin.write(pin)
            self.off_on.write(1)
            for i in range(reversals):
                stimulus.draw()
                window.flip()
                stimulus.setPhase(0.5, '+')
                core.wait(0.5)
            self.off_on.write(0)
            self.both_screens_gray(5.0)
        self.trigger.write(0.0)
            
        event.waitKeys()
        event.clearEvents()
        self.board.exit()
        self.window1.close()
        self.window2.close()
        core.quit()
                
    
    def winflip(self):
        self.window1.flip()
        self.window2.flip()
        
        
    def both_screens_gray(self, time):
        self.fixation1.draw()
        self.fixation2.draw()
        self.winflip()
        core.wait(time)
    
if __name__ == "__main__":
    experiment = FMB()
    #experiment.habituation()
    experiment.training(screen = 2, reversals = 5, orientation = 135) #so if screen = 2, then PR grating shows in 2, and gray on 1?
        


    
    
