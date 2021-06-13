#!/usr/bin/env python3
# This demo shows how to remote control an Explor3r robot
#
# Red buttons control left motor, blue buttons control right motor.
# Leds are used to indicate movement direction.

from time import sleep
from ev3dev2.motor import MediumMotor, OUTPUT_B, OUTPUT_C, LargeMotor
from ev3dev2.sensor.lego import InfraredSensor

# Connect two large motors on output ports B and C
lmotor = LargeMotor(OUTPUT_B)
rmotor = MediumMotor(OUTPUT_C)

# Connect remote control
rc = RemoteControl()

ir = InfraredSensor()

# Initialize button handler
# button = Button()   # not working so disabled

# Turn leds off
Leds.all_off()

def roll(motor, direction):
    """
    Generate remote control event handler. It rolls given motor into given
    direction (1 for forward, -1 for backward). When motor rolls forward, the
    given led group flashes green, when backward -- red. When motor stops, the
    leds are turned off.

    The on_press function has signature required by RemoteControl class.
    It takes boolean state parameter; True when button is pressed, False
    otherwise.
    """
    def on_press(state):
        if state:
            # Roll when button is pressed
            motor.run_forever(speed_sp=90*direction)
        else:
            # Stop otherwise
            motor.stop(stop_action='brake')

    return on_press

# Assign event handler to each of the remote buttons
ir.on_channel1_top_left    = roll(lmotor,    5)
ir.on_channel1_bottom_left  = roll(lmotor,   -5)
ir.on_channel1_top_right   = roll(rmotor,   5)
ir.on_channel1_bottom_rightn = roll(rmotor,  -5)

# Enter event processing loop
#while not button.any():   #not working so commented out
while True:   #replaces previous line so use Ctrl-C to exit
    ir.process()
    sleep(0.01)
    
# Press Ctrl-C to exit