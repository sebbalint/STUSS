from ev3dev2.led import Leds

def roll(motor, leds, led_group, direction):
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
            leds.set_color(led_group, Leds.GREEN if direction > 0 else Leds.RED)
        else:
            # Stop otherwise
            motor.stop(stop_action='brake')
            leds.all_off()

    return on_press