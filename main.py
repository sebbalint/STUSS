#!/usr/bin/env python3
from ev3dev.ev3 import *
import os

from pybricks.hubs import EV3Brick
from pybricks.parameters import Button

#menu button functions
from menu import wait_for_button
from transit import auto_transit





#setup und inits

ev3 = EV3Brick()
os.system('setfont Lat15-TerminusBold14') # TODO checken ob das funktioniert

# Connect remote control
rc = RemoteControl()

# Connect two large motors on output ports B and C
lr_M = LargeMotor('outB'); mL.stop_action = 'hold'
ud_M = MediumMotor('outC'); mR.stop_action = 'hold'

# Turn leds off
Leds.all_off()


# Environment variables
# Gondola has to be set to a fixed start position (ev3 side, loading position)
max_heigt = 0
max_width = 0
curr_y = 0
curr_x = 0 # gibt es sowas als Attribute des ev3??? TODO

#program
"""
print('Hello, my name is EV3!')
Sound.speak('Hello, my name is EV3!').wait()
mL.run_to_rel_pos(position_sp = 840, speed_sp = 250)
mR.run_to_rel_pos(position_sp = -840, speed_sp = 250)
mL.wait_while('running')
mR.wait_while('running')
"""

#forced calibrate
# entweder mit rumfahren und dann jeweils drücken wenn links ist, rechts, unten, oben (wird angezeigt was grad gefordert ist)
# oder man kann die Höhenwerte und so eingeben (mit Zahl wird angezeigt und button hoch erhöht die Zahl usw.)

#While-Execute-Schleife (Hauptprogramm)
while True:
    # Show the menu and wait for one button to be selected.
    button = wait_for_button(ev3)

    # Now you can do something, based on which button was pressed.

    # In this demo, we just play a different sound for each button.
    if button == Button.LEFT:
        free_transit(ev3, rc, lr_M, ud_M)
        
    elif button == Button.RIGHT:
        autotransit(ev3, rc, lr_M, ud_M)
        
    elif button == Button.UP:
        calibrate(ev3, rc, lr_M, ud_M)
        
    elif button == Button.DOWN:
        ev3.speaker.beep(200)

    elif button == Button.CENTER:
        ev3.speaker.beep(400)
        