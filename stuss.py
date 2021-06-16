#!/usr/bin/env python3
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.display import Display
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor.lego import InfraredSensor
from ev3dev2.led import Leds
from time import sleep
from PIL import Image
import ev3dev2.fonts as fonts
import os
from stuss_utils import bind_buttons_free_move, unbind_all_buttons, menu_handler_function, handler_function, auto_move, bind_buttons_limited_free_move, limited_roll
os.system('setfont Lat15-TerminusBold14')


class Gondola():


    def __init__(self, large_motor_port=OUTPUT_A,  medium_motor_port=OUTPUT_B):


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
    gon.lcd.draw.text((10,10), 'exit', font=fonts.load('luBS14'))
    gon.lcd.update()

def free(gon):
    gon.run_menu = False
    gon.lcd.clear()
    gon.lcd.draw.text((10,10), 'free', font=fonts.load('luBS14'))
    gon.lcd.update()

    # set buttons. Added constant for inacurracy margin, because gondola may sit on the area border after calibration.
    bind_buttons_limited_free_move(gon, gon.vert_length + 10, gon.hori_length + 10)

    gon.menu_exit = False

    def exit_to_menu(gon):
        def on_press(state):
            if(state):
                gon.menu_exit = True
        return on_press
        

    gon.btn.on_enter = exit_to_menu(gon)

    while not gon.menu_exit:
        gon.btn.process()
        gon.rc.process()
        sleep(0.01)
    
    # unbind buttons
    unbind_all_buttons(gon)

def return_to_start(gon):

    gon.sound.beep()
    gon.lcd.clear()
    gon.lcd.update()
    gon.lcd.draw.text((10,10), 'return_to_start', font=fonts.load('luBS14'))
    gon.lcd.update()
    sleep(2)
    gon.run_menu = False
    gon.direction = 1

    gon.vert_motor.run_to_abs_pos(position_sp=gon.vert_length, speed_sp=gon.auto_speed, stop_action="brake")
    gon.vert_motor.wait_while('running')

    gon.hori_motor.run_to_abs_pos(position_sp=0, speed_sp=gon.auto_speed, stop_action="brake")
    gon.hori_motor.wait_while('running')

    gon.vert_motor.run_to_abs_pos(position_sp=0, speed_sp=gon.auto_speed, stop_action="brake")
    gon.vert_motor.wait_while('running')

def auto(gon):
    gon.menu_exit = False
    gon.run_menu = False
    gon.lcd.clear()
    gon.lcd.update()
    logo = Image.open('/home/robot/STUSS/Images/auto_menu.png')
    gon.lcd.image.paste(logo, (0,0))
    gon.lcd.update()
    return_to_start(gon)

    def exit_to_menu(gon):
        def on_press(state):
            if(state):
                gon.menu_exit = True
        return on_press
        

    gon.btn.on_up    = handler_function(auto_move, gon)
    gon.rc.on_channel1_top_left = handler_function(auto_move, gon)
    gon.btn.on_enter = exit_to_menu(gon)

    while not gon.menu_exit:
        gon.btn.process()
        gon.rc.process()
        sleep(0.01)

    # unbind buttons
    unbind_all_buttons(gon)

def calibrate(gon):
    gon.run_menu = False
    gon.lcd.clear()
    gon.lcd.update()
    gon.lcd.draw.text((10,10), 'calibrating.. \nPlease move the gondola to the desired loading position on the right hand side of the bridge. \nIf you have reached the lowest and most right position confirm by pressing Enter.', font=fonts.load('luBS14'))
    gon.lcd.update()

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

    while not gon.menu_exit:
        gon.btn.process()
        gon.rc.process()
        sleep(0.01)

    gon.lcd.draw.text((10,10), 'Start position confirmed', font=fonts.load('luBS14'))
    gon.lcd.update()
    #print(gon.vert_motor.position)
    #print(gon.hori_motor.position)

    sleep(2)

    gon.lcd.clear()
    gon.lcd.update()
    gon.lcd.draw.text((10,10), 'calibrating.. \nPlease move the gondola to the desired travelling height on the left hand side of the bridge. \nIf you have reached to highest and most left position confirm by pressing Enter.', font=fonts.load('luBS14'))
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

    while not gon.menu_exit:
        gon.btn.process()
        gon.rc.process()
        sleep(0.01)

    gon.lcd.draw.text((10,10), 'Travel position confirmed', font=fonts.load('luBS14'))
    gon.lcd.update()
    #print(gon.vert_motor.position)
    #print(gon.hori_motor.position)

    unbind_all_buttons(gon)

    gon.lcd.draw.text((10,10), 'calibration finished.', font=fonts.load('luBS14'))
    gon.lcd.update()

    sleep(2)

def beep(gon):
    # Sound.beep()
    gon.run_menu = False
    gon.lcd.clear()
    gon.lcd.update()
    gon.lcd.draw.text((10,10), 'beep', font=fonts.load('luBS14'))
    gon.lcd.update()
    gon.sound.speak("beep beep I am a sheep", play_type=Sound.PLAY_WAIT_FOR_COMPLETE)
    sleep(2)

def menu(gon):
    logo = Image.open('/home/robot/STUSS/Images/Menu.png')
    gon.lcd.image.paste(logo, (0,0))
    gon.lcd.update()

    gon.btn.on_up    = menu_handler_function(calibrate, gon)
    gon.btn.on_down  = menu_handler_function(beep, gon)
    gon.btn.on_left  = menu_handler_function(free, gon)
    gon.btn.on_right = menu_handler_function(auto, gon)
    gon.btn.on_enter = menu_handler_function(exit, gon)

    while gon.run_menu:
        gon.btn.process()
        sleep(0.01)


# Main

gon = Gondola()

calibrate(gon)

while not gon.exit:
    gon.run_menu = True
    menu(gon)

gon.lcd.clear()
gon.lcd.update()
print('Goodbye')