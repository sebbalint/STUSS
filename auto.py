#!/usr/bin/env python3
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.display import Display
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor.lego import InfraredSensor
from ev3dev2.led import Leds
from time import sleep
from PIL import Image
import os
from stuss_utils import roll
os.system('setfont Lat15-TerminusBold14')

class Gondola():


    def __init__(self, large_motor_port=OUTPUT_A,  medium_motor_port=OUTPUT_B):

        # Set base speed
        #horSpeed = 50
        #verSpeed = 50

        # Connect two large motors on output ports B and C
        # lmotor = LargeMotor('outB')
        # mmotor = MediumMotor('outC')

        # Connect two large motors on output ports B and C
        self.hori_motor = LargeMotor(large_motor_port)
        self.vert_motor = MediumMotor(medium_motor_port)

        # Connect remote control
        self.rc = InfraredSensor()

        self.sound = Sound() 
        self.btn = Button()
        self.lcd = Display()
        self.leds = Leds()

        self.run = True
        self.exit = False
        self.exit_menu = False

        # Boot events
        self.leds.all_off()

        self.vert_length = 500
        self.hori_length = 700

        self.auto_speed = 500
        self.ramp = 3000
        # values 1 and -1
        self.direction = 1


def auto_move(gon):
    # move up
    gon.vert_motor.run_to_rel_pos(ramp_up_sp=gon.ramp,ramp_down_sp=gon.ramp,position_sp=gon.vert_length, speed_sp=gon.auto_speed, stop_action="coast")
    gon.vert_motor.wait_while('running')

    # move left/right
    gon.hori_motor.run_to_rel_pos(ramp_up_sp=gon.ramp,ramp_down_sp=gon.ramp,position_sp=gon.hori_length*gon.direction, speed_sp=gon.auto_speed, stop_action="coast")
    gon.hori_motor.wait_while('running')
    gon.direction = gon.direction * (-1)

    # move down
    gon.vert_motor.run_to_rel_pos(ramp_up_sp=gon.ramp,ramp_down_sp=gon.ramp, position_sp=-gon.vert_length, speed_sp=gon.auto_speed, stop_action="coast")
    gon.vert_motor.wait_while('running')
# Main

gon = Gondola()

print("starting....")
sleep(2)
auto_move(gon)
print("done")
sleep(2)