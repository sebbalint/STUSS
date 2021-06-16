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
from stuss_utils import bind_buttons_free_move, unbind_all_buttons, menu_handler_function, handler_function, auto_move
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

        self.run_menu = True
        self.exit = False

        # Funktionsvariablen
        self.menu_exit = True

        # Boot events
        self.leds.all_off()

        self.vert_length = 500
        self.hori_length = 700

        self.auto_speed = 200
        # values 1 and -1
        self.direction = 1


def exit(gon):
    gon.run_menu = False
    gon.exit = True
    gon.lcd.clear()
    gon.lcd.update()
    print('exit')

def free(gon):
    gon.run_menu = False
    gon.lcd.clear()
    gon.lcd.update()
    print('free')

    # set buttons

    bind_buttons_free_move(gon)

    print('free roll passed')

    gon.menu_exit = False

    def exit_to_menu(gon):
        def on_press(state):
            if(state):
                gon.menu_exit = True
        return on_press
        

    gon.btn.on_enter = exit_to_menu(gon)
    print('enter assigned')

    while not gon.menu_exit:
        gon.btn.process()
        gon.rc.process()
        sleep(0.01)
    
    # unbind buttons
    unbind_all_buttons(gon)

    print('leaving free transit mode')


def auto(gon):
    gon.menu_exit = False
    gon.run_menu = False
    gon.lcd.clear()
    gon.lcd.update()
    print('auto')

    def exit_to_menu(gon):
        def on_press(state):
            if(state):
                gon.menu_exit = True
        return on_press
        

    gon.btn.on_up    = handler_function(auto_move, gon)
    gon.rc.on_channel1_top_left = handler_function(auto_move, gon)
    gon.btn.on_enter = exit_to_menu(gon)

    print('buttons assigned')

    # gon.return_to_start()

    while not gon.menu_exit:
        gon.btn.process()
        gon.rc.process()
        sleep(0.01)

    # unbind buttons
    unbind_all_buttons(gon)

def return_to_start(gon):
    gon.run_menu = False
    gon.lcd.clear()
    gon.lcd.update()
    print('return_to_start')
    
def calibrate(gon):
    gon.run_menu = False
    gon.lcd.clear()
    gon.lcd.update()
    print('calibrating')

    bind_buttons_free_move(gon)

    def set_start_position(gon):
        def on_press(state):
            if(state):
                gon.vert_motor.position = 0
                gon.hori_motor.position = 0 # TODO geht das wirklich?
                gon.menu_exit = True
                
        return on_press
    
    gon.menu_exit = False
    gon.btn.on_enter = set_start_position(gon)

    print('Please move the gondola to the desired loading position on the right hand side of the bridge.')
    print('If you have reached to lowest and most right position confirm by pressing Enter.')


    while not gon.menu_exit:
        gon.btn.process()
        sleep(0.01)

    print('Start position confirmed at ' + gon.vert_motor.position + ' ' + gon.hori_motor.position)

    sleep(2)

    gon.lcd.clear()
    gon.lcd.update()

    def set_travel_position(gon):
        def on_press(state):
            if(state):
                gon.vert_length = gon.vert_motor.position
                gon.hori_length = gon.hori_motor.position # TODO geht das wirklich?
                gon.menu_exit = True
                
        return on_press
    
    gon.menu_exit = False
    gon.btn.on_enter = set_travel_position(gon)

    print('Please move the gondola to the desired traveling height on the left hand side of the bridge.')
    print('If you have reached to highest and most left position confirm by pressing Enter.')

    while not gon.menu_exit:
        gon.btn.process()
        sleep(0.01)

    print('Travel position confirmed at ' + gon.vert_motor.position + ' ' + gon.hori_motor.position)

    unbind_all_buttons(gon)

    print('calibration finished')


def beep(gon):
    # Sound.beep()
    gon.lcd.clear()
    gon.lcd.update()
    gon.sound.beep()
    gon.run_menu = False
    print('beep')
    sleep(5)

def menu(gon):
    logo = Image.open('/home/robot/STUSS/Images/Menu.png')
    gon.lcd.image.paste(logo, (0,0))
    gon.lcd.update()

    gon.btn.on_up    = menu_handler_function(calibrate, gon)
    gon.btn.on_down  = menu_handler_function(exit, gon)
    gon.btn.on_left  = menu_handler_function(free, gon)
    gon.btn.on_right = menu_handler_function(auto, gon)
    gon.btn.on_enter = menu_handler_function(beep, gon)

    while gon.run_menu:
        gon.btn.process()
        sleep(0.01)



# Main

gon = Gondola()

while not gon.exit:
    gon.run_menu = True
    menu(gon)

gon.lcd.clear()
gon.lcd.update()
print('Goodbye')
# gon.sound.speak('Goodbye').wait()