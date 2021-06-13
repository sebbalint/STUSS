#!/usr/bin/env python3
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.display import Display
from time import sleep
from PIL import Image
import os
os.system('setfont Lat15-TerminusBold14')

class Things():

    # Set base speed
    #horSpeed = 50
    #verSpeed = 50

    # Connect two large motors on output ports B and C
    # lmotor = LargeMotor('outB')
    # mmotor = MediumMotor('outC')

    # Connect remote control
    # rc = RemoteControl()   

    sound = Sound() 
    btn = Button()
    lcd = Display()

    run = True
    exit = False


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