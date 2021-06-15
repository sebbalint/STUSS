from ev3dev2.led import Leds

def roll(motor, direction): # LEDs könnten hier noch blinken, TODO
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

def unbind_all_buttons(gon):

    gon.btn.on_up    = None
    gon.btn.on_down  = None
    gon.btn.on_left  = None
    gon.btn.on_right = None

    gon.rc.on_channel1_top_left    = None
    gon.rc.on_channel1_bottom_left  = None
    gon.rc.on_channel1_top_right   = None
    gon.rc.on_channel1_bottom_right = None

    gon.btn.on_enter = None

def handler_function(func, gon):
    
    def on_press(state):
        print('check1')
        unbind_all_buttons(gon)
        print('check2')
        func(*gon)
    return on_press