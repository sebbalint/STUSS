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

        # Boot events
        self.leds.all_off()


def exit(gon):
    gon.run = False
    gon.exit = True
    gon.lcd.clear()
    gon.lcd.update()
    print('exit')

def free(gon):
    gon.run = False
    gon.lcd.clear()
    gon.lcd.update()
    print('free')

def auto(gon):
    gon.run = False
    gon.lcd.clear()
    gon.lcd.update()
    print('auto')

def return_to_start(gon):
    gon.run = False
    gon.lcd.clear()
    gon.lcd.update()
    print('return_to_start')
    
def calibrate(gon):
    gon.run = False
    gon.lcd.clear()
    gon.lcd.update()
    print('cal')

def beep(gon):
    # Sound.beep()
    gon.lcd.clear()
    gon.lcd.update()
    gon.sound.beep()
    gon.run = False
    print('beep')
    sleep(5)

def menu(gon):
    logo = Image.open('/home/robot/STUSS/Images/Menu.png')
    gon.lcd.image.paste(logo, (0,0))
    gon.lcd.update()


    while gon.run:
        if(gon.btn.right):
            auto(gon)
        if(gon.btn.left):
            free(gon)
        if(gon.btn.up):
            calibrate(gon)
        if(gon.btn.enter):
            beep(gon)
        if(gon.btn.down):
            exit(gon)
        #gon.btn.process()
        sleep(0.01)



# Main

gon = Gondola()

while not gon.exit:
    gon.run = True
    menu(gon)

gon.lcd.clear()
gon.lcd.update()
print('Goodbye')
gon.sound.speak('Goodbye').wait()