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

Under #Board the serial port is defined as '/dev/tty/AFMB CM1' 
for linux and mac. For windows this should be 'COM1'.
This script is written for three monitors. To use some other 
setup you will need to change monitor width and wx_res under 
#monitor details and #Psychopy windows

Author: Jesse Trinity (Coleman Lab)


FMB
Modified 9/16/15, JEC - add key press after gray; print feedback
Modified 1/10/16, JEC - lines 89,96,223 - lines to toggle screensaver on/off (xset s on or off)
"""
import wx, sys
from psychopy import visual, core, event, monitors
from pyfirmata import Arduino, util

#Open serial port
class FMB:
    
    
    
    def __init__(self):
        #board
        #self.board = Arduino('/dev/ttyACM0')
        self.board = Arduino('/dev/ttyUSB0') #for NANO 328
        self.it = util.Iterator(self.board)
        self.it.start()
        self.board.analog[0].enable_reporting()
    
    	#pins
        self.monitor_pin = self.board.get_pin('d:3:p')
        self.stim_pin = self.board.get_pin('d:6:p')
        self.off_on = self.board.get_pin('d:9:p')
        self.trigger = self.board.get_pin('d:5:p')
    
    	#monitor details
        self.res = [1280,1024]
        self.monitor_width = 37.5 #cm
        self.monitor_distance = 14 #14 #14=small box) #cm from middle #20 #20=normal box) #cm from middle
        self.mon = monitors.Monitor("mymon", distance = self.monitor_distance, width = self.monitor_width)
        self.mon.currentCalib['sizePix'] = [self.res[0], self.res[1]]
        self.mon.saveMon()
        
        #Psychopy windows
        self.window1 = visual.Window(size=[self.res[0],self.res[1]],monitor=self.mon, fullscr = False,allowGUI=False, units="deg", screen =1)
        self.window2 = visual.Window(size=[self.res[0],self.res[1]],monitor=self.mon, fullscr = False,allowGUI=False, units="deg", screen =2)
        
        #can't change gamma values; color set above middle gray to maintain the same brightness as grating
        self.fixation1 = visual.GratingStim(win=self.window1, size=300, colorSpace ='rgb255', pos=[0,0], sf=0, color=(143,143,143))
        self.fixation2 = visual.GratingStim(win=self.window2, size=300, colorSpace ='rgb255', pos=[0,0], sf=0, color=(143,143,143))
        
  
    def habituation(self, time):
        #pause on gray screens until key press (make space key?)
        self.both_screens_gray(1.0)
        print "Press any key to begin..."
        sys.stdout.flush() #ensure msg appears now, regardless of print buffering
        
        event.waitKeys()
        self.trigger.write(1.0)
        print "Now recording for "+str(time)+" s"
        self.both_screens_gray(time)
        self.trigger.write(0.0)
        print "Habituation complete..."
        #xset s on
        from subprocess import call
        screensaver_ON = ('xset s on')
        call ([screensaver_ON], shell=True)
        print('screen saver ON')
        
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
                print("*** Stim on screen 1 ***")

                window = self.window1
                self.monitor_pin.write(0)
            elif kwargs["screen"]==2:
                print("*** Stim on screen 2 ***")
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
        
        if "startdelay" in kwargs:
            startdelay = kwargs["startdelay"]
        else:
            startdelay = 300.0
            
        if "interval" in kwargs:
            interval = kwargs["interval"]
        else:
            interval = 30.0
            
        if "blocks" in kwargs:    
            blocks = kwargs["blocks"]
        else:
            blocks = 5
        
        stimulus = visual.GratingStim(tex = "sin", win=window, mask="circle", size=300, pos=[0,0], sf=0.05 , ori=(orientation))
        

        #pause on gray screens until key press (make space key?)
        self.both_screens_gray(1.0)
        print "Press any key to begin..."
        sys.stdout.flush() #ensure msg appears now, regardless of print buffering
        
        event.waitKeys()
        
        #procedure
        print "TRIAL RUNNING"
        sys.stdout.flush() #ensure msg appears now, regardless of print buffering
        
        self.trigger.write(1.0)
        self.both_screens_gray(startdelay)
        for i in range(blocks):
            self.stim_pin.write(pin)
            self.off_on.write(1)
            print('Session '+str(i+1)+' of '+str(blocks))
            sys.stdout.flush()
            for i in range(reversals):
                stimulus.draw()
                window.flip()
                stimulus.setPhase(0.5, '+'
)
                core.wait(0.5)
                stimulus.draw()
                window.flip()
                stimulus.setPhase(0.5, '+')
                core.wait(0.5)
            self.off_on.write(0)
            self.both_screens_gray(interval)
            
        self.trigger.write(0.0)
        
        print "TRIAL COMPLETE"
        
        event.waitKeys()
        
        #xset s on
        from subprocess import call
        screensaver_ON = ('xset s on')
        call ([screensaver_ON], shell=True)
        print('screen saver ON')
        
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
    #xset s off (cann this be added to a class function?)
    from subprocess import call
    screensaver_OFF = ('xset s off')
    call ([screensaver_OFF], shell=True)
    print('screen saver OFF')
    
    experiment = FMB()
    sys.stdout.flush() #ensure msg appears now, regardless of print buffering
    
    # TEST THE SYSTEM
    experiment.training(screen = 2, reversals = 100, orientation = 45, startdelay = 5 , blocks = 1, interval = 2)
    
    # Coleman Lab habituation:
    # experiment.habituation(1800) #enter habituation time (for trigger in sec)
    
    # Coleman Lab "familiar" (for training and testing):
    #experiment.training(screen = 2, reversals = 100 , orientation = 45, startdelay = 300, blocks = 5, interval = 30)
    
    # Coleman Lab "novel" (only for testing day):
    #experiment.training(screen = 2, reversals = 100 , orientation = 135, startdelay = 300, blocks = 5, interval = 30)
    
    # Sarkisian Lab:
    #habituation
    #experiment.habituation(600) #enter habituation time (for trigger in sec)
    
    #training
    #experiment.training(screen = 2, reversals = 100 , orientation = 45, startdelay = 180, blocks = 3, interval = 30)
    
    #testing
    #experiment.training(screen = 2, reversals = 100 , orientation = 135, startdelay = 180, blocks = 3, interval = 30)
 


    
    