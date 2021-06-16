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

def auto_move(gon): # TODO sleeps zwischen die moves, ramp ups vllt, andere stop action
    
    print("moving")
    # move up
    gon.vert_motor.run_to_rel_pos(position_sp=gon.vert_length, speed_sp=gon.auto_speed, stop_action="coast")
    gon.vert_motor.wait_while('running')

    # move left/right
    gon.hori_motor.run_to_rel_pos(position_sp=gon.hori_length*gon.direction, speed_sp=gon.auto_speed, stop_action="coast")
    gon.hori_motor.wait_while('running')
    gon.direction = gon.direction * (-1)

    # move down
    gon.vert_motor.run_to_rel_pos(position_sp=-gon.vert_length, speed_sp=gon.auto_speed, stop_action="coast")
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

def menu_handler_function(func, gon):
    
    def on_press(state):
        if(state):
            unbind_all_buttons(gon)
            func(gon)
    return on_press

def handler_function(func, gon):
    print("button p")
    def on_press(state):
        print("on_Press")
        if(state):
            print("funky")
            func(gon)
    return on_press