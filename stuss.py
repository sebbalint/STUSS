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

class Things():


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


def exit(things):
    things.run = False
    things.exit = True
    things.lcd.clear()
    things.lcd.update()
    print('exit')

def free(things):
    things.run = False
    things.lcd.clear()
    things.lcd.update()
    print('free')

def auto(things):
    things.run = False
    things.lcd.clear()
    things.lcd.update()
    print('auto')

def return_to_start():
    run = False
    lcd.clear()
    lcd.update()
    print('return_to_start')
    
def calibrate(things):
    things.run = False
    things.lcd.clear()
    things.lcd.update()
    print('cal')

def beep(things):
    # Sound.beep()
    things.lcd.clear()
    things.lcd.update()
    things.sound.beep()
    things.run = False
    print('beep')
    sleep(5)

def menu(things):
    logo = Image.open('/home/robot/STUSS/Images/Menu.png')
    things.lcd.image.paste(logo, (0,0))
    things.lcd.update()


    while things.run:
        if(things.btn.right):
            auto(things)
        if(things.btn.left):
            free(things)
        if(things.btn.up):
            calibrate(things)
        if(things.btn.enter):
            beep(things)
        if(things.btn.down):
            exit(things)
        #things.btn.process()
        sleep(0.01)



# Main

things = Things()

while not things.exit:
    things.run = True
    menu(things)

things.lcd.clear()
things.lcd.update()
print('Goodbye')
things.sound.speak('Goodbye').wait()