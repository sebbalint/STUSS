from ev3dev2.led import Led
from time import sleep

def roll(motor, direction): # LEDs könnten hier noch blinken, TODO
    """
    Generate remote control event handler. It rolls given motor into given
    direction (1 for forward, -1 for backward).

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

def auto_move(gon): # TODO sleeps zwischen die moves, ramp ups vllt, andere stop action
    
    gon.sound.beep()
    sleep(2)

    # move up
    gon.vert_motor.run_to_rel_pos(ramp_up_sp=gon.ramp,ramp_down_sp=gon.ramp,position_sp=gon.vert_length, speed_sp=gon.auto_speed, stop_action="coast")
    gon.vert_motor.wait_while('running')

    # move left/right
    gon.hori_motor.run_to_rel_pos(ramp_up_sp=gon.ramp,ramp_down_sp=gon.ramp,position_sp=gon.hori_length*gon.direction, speed_sp=gon.auto_speed, stop_action="coast")
    gon.hori_motor.wait_while('running')
    gon.direction = gon.direction * (-1)

    # move down
    gon.vert_motor.run_to_rel_pos(ramp_up_sp=gon.ramp,ramp_down_sp=gon.ramp,position_sp=-gon.vert_length, speed_sp=gon.auto_speed, stop_action="coast")
    gon.vert_motor.wait_while('running')

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

def limited_roll(motor, direction, limit): # LEDs könnten hier noch blinken, TODO
    """
    Generate remote control event handler. It rolls given motor into given
    direction until it has reached the given limit (1 for forward, -1 for backward).

    The on_press function has signature required by RemoteControl class.
    It takes boolean state parameter; True when button is pressed, False
    otherwise.
    """
    def on_press(state):
        if state:
            # Roll when button is pressed
            motor.run_to_abs_pos(position_sp=limit, speed_sp=90*direction, stop_action="brake")
        else:
            # Stop otherwise
            motor.stop(stop_action='brake')

    return on_press

def bind_buttons_limited_free_move(gon, vert_limit, hori_limit): # (Button speed ist extra noch nicht korrekt)
    
    gon.btn.on_up    = limited_roll(gon.vert_motor, 1, vert_limit)
    gon.btn.on_down  = limited_roll(gon.vert_motor, -1, 0)
    gon.btn.on_left  = limited_roll(gon.hori_motor, 1, hori_limit)
    gon.btn.on_right = limited_roll(gon.hori_motor, -1, 0)

    gon.rc.on_channel1_top_left    = limited_roll(gon.vert_motor, 5, vert_limit)
    gon.rc.on_channel1_bottom_left  = limited_roll(gon.vert_motor, -5, 0)
    gon.rc.on_channel1_top_right   = limited_roll(gon.hori_motor, 5, hori_limit)
    gon.rc.on_channel1_bottom_right = limited_roll(gon.hori_motor, -5, 0)

def bind_buttons_free_move(gon): # (Button speed ist extra noch nicht korrekt)

    gon.btn.on_up    = roll(gon.vert_motor, 1)
    gon.btn.on_down  = roll(gon.vert_motor, -1)
    gon.btn.on_left  = roll(gon.hori_motor, 1)
    gon.btn.on_right = roll(gon.hori_motor, -1)

    gon.rc.on_channel1_top_left    = roll(gon.vert_motor, 5)
    gon.rc.on_channel1_bottom_left  = roll(gon.vert_motor, -5)
    gon.rc.on_channel1_top_right   = roll(gon.hori_motor, 5)
    gon.rc.on_channel1_bottom_right = roll(gon.hori_motor, -5)

def menu_handler_function(func, gon):
    
    def on_press(state):
        if(state):
            unbind_all_buttons(gon)
            func(gon)
    return on_press

def handler_function(func, gon):
    def on_press(state):
        if(state):
            func(gon)
    return on_press