from transit_util import util

def auto_transit(ev3, rc, lr_M, ud_M):
    """
    This function transitions the gondola from one side to the other.

    Richtung hier als Parameter? also links nach rechts oder so TODO

    Returns true on termination
    """

    # Show a picture of maybe "transition in progress" TODO
    #ev3.screen.load_image('auto_transition.png')

    # Tip: add text or icons to the image to help you
    # remember what each button will do in your program.

    
    return true


def free_transit(ev3, rc, lr_M, ud_M):
    """
    This function allows the user to freely move the gondola without any restrictions.

    Soll die Gondel nach Beeindigung des free_transit wieder an eine Startposition automatisch gefahren werden? TODO

    Returns (?)
    """

    # Show a picture of maybe "free movement enabled" TODO
    #ev3.screen.load_image('(was Tasten machen).png')

    # Assign event handler to each of the remote buttons
    rc.on_red_up    = roll(lr_M, Leds.LEFT,   5)
    rc.on_red_down  = roll(lr_M, Leds.LEFT,  -5)
    rc.on_blue_up   = roll(lr_M, Leds.RIGHT,  5)
    rc.on_blue_down = roll(lr_M, Leds.RIGHT, -5)

    # Enter event processing loop
    #while not button.any():   #not working so commented out
    while True:   #replaces previous line so use Ctrl-C to exit
    rc.process()
    sleep(0.01)
    
#    Press Ctrl-C to exit


"""
TODO functions:

free_transit (TODO soll hier dann am Ende )
calibrate (returns sind dann die Dimensionen)
"""