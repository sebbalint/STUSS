#!/usr/bin/env python3
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.display import Display
from time import sleep
from PIL import Image
import os
os.system('setfont Lat15-TerminusBold14')



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


def exit():
    run = False
    exit = True
    lcd.clear()
    lcd.update()
    print('exit')

def free():
    run = False
    lcd.clear()
    lcd.update()
    print('free')

def auto():
    run = False
    lcd.clear()
    lcd.update()
    print('auto')

def return_to_start():
    run = False
    lcd.clear()
    lcd.update()
    print('return_to_start')

def calibrate():
    run = False
    lcd.clear()
    lcd.update()
    print('cal')

def beep():
    lcd.clear()
    lcd.update()
    sound.beep()
    run = False
    print('beep')
    sleep(5)

def menu():
    logo = Image.open('/home/robot/STUSS/Images/Menu.png')
    lcd.image.paste(logo, (0,0))
    lcd.update()


    while run:
        if(btn.right):
            auto()
        if(btn.left):
            free()
        if(btn.up):
            calibrate()
        if(btn.enter):
            beep()
        if(btn.down):
            exit()
        sleep(0.01)



# Main

while not exit:
    run = True
    menu()

lcd.clear()
lcd.update()
print('Goodbye')
sound.speak('Goodbye').wait()