# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 13:04:17 2016

@author: jesse
"""
from matplotlib import pyplot as plt
import numpy as np
from psychopy import visual, event, monitors

mon = monitors.Monitor("colorTest2", distance = 30, width = 37)

mon.currentCalib['sizePix'] = [1920, 1080]
print mon.currentCalib

mywin = visual.Window(size=[1920,1080],monitor=mon, fullscr = False, allowGUI = True, units="deg", screen =0, winType = 'pyglet')

color = visual.GratingStim(win=mywin, size=200, pos=[0,0], sf=0, color=[-1.0,-1.0,-1.0])

vals = [i/10.0 - 1 for i in range(21)]

def color_step(vals):
    for val in vals:
        color.setColor([val,-1.0,-1.0]) 
        color.draw()
        mywin.flip()
        event.waitKeys()
        event.clearEvents()
    
    color.setColor([-1.0,-1.0,-1.0])  
    for val in vals:
        color.setColor([-1.0,val,-1.0])
        color.draw()
        mywin.flip()
        event.waitKeys()
        event.clearEvents()
    
    color.setColor([-1.0,-1.0,-1.0])
    for val in vals:
        color.setColor([-1.0,-1.0,val])
        color.draw()
        mywin.flip()
        event.waitKeys()
        event.clearEvents()
    
    color.setColor([-1.0,-1.0,-1.0])
    
    for val in vals:
        print val
        color.setColor([val,val,val])
        color.draw()
        mywin.flip()
        event.waitKeys()
        event.clearEvents()

#run the function, comment out when done measuring
color_step(vals)

vals = [i*0.05 for i in range(21)]

Rlvls = [0.4, 0.4, 0.44, 0.56, 0.79, 1.15, 1.57, 2.00, 2.51 ,3.08, 3.68, 4.36, 5.18, 6.04, 6.86, 7.79, 8.72, 9.70, 10.68, 11.83, 13.00]

Glvls = [0.39, 0.42, 0.58, 0.99, 1.84, 3.21, 4.77, 6.39, 8.34, 10.5, 12.82, 15.45, 18.6, 21.8, 25.0, 28.3, 32.2, 35.7, 39.7, 44.2, 48.8]

Blvls = [0.4, 0.4, 0.4, 0.42, 0.45, 0.51, 0.58, 0.65, 0.73, 0.82, 0.91, 1.02, 1.14, 1.27, 1.40, 1.54, 1.68, 1.82, 1.96, 2.13, 2.31]

Wlvls = [0.39, 0.43, 0.65, 1.21, 2.39, 4.28, 6.43, 8.64, 11.28, 14.17, 17.27, 20.7, 24.7, 29.0, 33.2, 37.8, 42.5, 47.3, 52.1, 57.7, 63.4]

#Rlvls = [(val - min(Rlvls))/(max(Rlvls) - min(Rlvls)) for val in Rlvls]
#Glvls = [(val - min(Glvls))/(max(Glvls) - min(Glvls)) for val in Glvls]
#Blvls = [(val - min(Blvls))/(max(Blvls) - min(Blvls)) for val in Blvls]
#Wlvls = [(val - min(Wlvls))/(max(Wlvls) - min(Wlvls)) for val in Wlvls]

plt.title('Gamma')
plt.xlabel('Input')
plt.ylabel('Lums')
plt.plot(vals, Rlvls, color = 'red')
plt.plot(vals, Glvls, color = 'green')
plt.plot(vals, Blvls, color = 'blue')
plt.plot(vals, Wlvls, color = 'black')

Rcalc = monitors.GammaCalculator(inputs = vals, lums = Rlvls)
Gcalc = monitors.GammaCalculator(inputs = vals, lums = Glvls)
Bcalc = monitors.GammaCalculator(inputs = vals, lums = Blvls)
Wcalc = monitors.GammaCalculator(inputs = vals, lums = Wlvls)

Rgamma = Rcalc.gamma
Ggamma = Gcalc.gamma
Bgamma = Bcalc.gamma
Wgamma = Wcalc.gamma

R_steps = [max(Rlvls)*((i/20.0)**(1/Rgamma)) for i in range(21)]
G_steps = [max(Glvls)*((i/20.0)**(1/Ggamma)) for i in range(21)]
B_steps = [max(Blvls)*((i/20.0)**(1/Bgamma)) for i in range(21)]
W_steps = [max(Wlvls)*((i/20.0)**(1/Wgamma)) for i in range(21)]

#plt.plot(vals, R_steps, color = 'red', ls = 'dashed')
plt.plot(vals, G_steps, color = 'green', ls = 'dashed')
#plt.plot(vals, B_steps, color = 'blue', ls = 'dashed')
plt.plot(vals, W_steps, color = 'black', ls = 'dashed')


#Use this section to set gamma for your monitor
#==============================================================================
# 
# grid = mon.getGammaGrid()                   
# 
# grid[0][2] = Wgamma
# 
# grid[1][2] = Rgamma
# 
# grid[2][2] = Ggamma
# 
# grid[3][2] = Bgamma
# 
# mon.setGammaGrid(grid)
# 
# mon.saveMon()
#==============================================================================

sin = np.sin(np.linspace(0, 2 * np.pi, 256)).astype(np.float64)
sin = (sin + 1)/2
sin = sin**(1/Wgamma)
sin = 2* sin -1
texture = np.array([sin for i in range(256)])

stim = visual.GratingStim(tex = texture, win=mywin, mask=None, size=200, pos=[0,0], sf=0.05 , ori=135)
for i in range(120):
    stim.draw()
    mywin.flip()

mywin.close()