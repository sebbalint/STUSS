#!/usr/bin/env python3

#correct imports (ev3dev2)
import logging
import signal
import sys
from threading import Thread, Event
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor.lego import InfraredSensor
from ev3dev2.button import Button
from ev3dev2.led import Leds
from time import sleep



log = logging.getLogger(__name__)

# should be assigned to rc button with the readable event as a parameter, when auto_transit is initiatied. (Could be done permanently, since it will always stop motors. Event can be cleared before a new transit.)
def return_auto_transit(return_event):
    """
    Generate remote control event handler. It signals the waiting auto_transit that the gondola can be returned.
    This function has signature required by RemoteControl class.
    It takes boolean state parameter; True when button is pressed, False otherwise.
    """
    def on_press(state):
        if state:
            # Set return event if button is pressed.
            return_event.set()
        else:
            # Do nothing if it has been released.
            pass

    return on_press

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
    
class MonitorControl(Thread):
    """
    A thread to monitor Gondolas InfraRedSensor and EV3 Buttons.
    """

    def __init__(self, parent):
        Thread.__init__(self)
        self.parent = parent
        self.shutdown_event = Event()
        self.monitor_c = Event()

    def __str__(self):
        return "MonitorControl"

    def run(self):

        while True:
            self.parent.rc.process()
            self.parent.button.process()
            sleep(0.01)

            if self.shutdown_event.is_set():
                log.info('%s: shutdown_event is set' % self)
                break

class MonitorEmergencyShutdown(Thread):
    """
    A thread to monitor if the Shutdown-Button has been pressed.
    """

    def __init__(self, parent): #parent ist hier einfach die main instanz, die 
        Thread.__init__(self)
        self.parent = parent
        self.shutdown_event = Event()  # Ausschalten des EmergencyShutdownThread
        # Möglichkeit den EmergencyShutdown temporär außer Kraft zu setzen.
        self.monitor_emergency = Event()

    def __str__(self):
        return "MonitorEmergencyShutdown"

    def run(self):

        while True:

            if self.monitor_emergency.is_set():

                # We only wait for 1000ms so that we can wake up to see if
                # our shutdown_event has been set
                if self.button.wait_for_pressed([backspace], timeout_ms=1000): # [backspace] ist die Liste mit Buttons auf die gewartet werden soll. 
                                                                        # Ich weiß nicht, ob das Element "backspace" das ist was zu der Taste korrespondiert, ich glaube es nur zu 95%.
                                                                        # Hab's aber nachgeschaut in der doc und da stand nur backspace
                    # TODO implement stop motors in parent
                    self.parent.stop_motors(True)

            if self.shutdown_event.is_set():
                log.info('%s: shutdown_event is set' % self)
                break


"""
# Environment variables fehlen komplett noch (x,y Koords usw.)
Müssen als Klassenvariablen initiiert werden.
# Gondola has to be set to a fixed start position (ev3 side, loading position)
gibt es sowas als Attribute des ev3??? TODO
"""
class Gondola():

    #constants
    VERT_TOP_SPEED = 0 #TODO
    HORI_TOP_SPEED = 0 #TODO

    def __init__(self, large_motor_port=OUTPUT_A,  medium_motor_port=OUTPUT_B):
        #Objektvariablen (immer mit self. aufrufen bzw. parent. in Threads.)
        self.hori_motor = LargeMotor(large_motor_port)
        self.vert_motor = MediumMotor(medium_motor_port)
        self.rc = InfraredSensor()
        self.mes = MonitorEmergencyShutdown(self)
        self.mc = MonitorControl(self)
        self.button = Button()
        self.leds = Leds()
        self.shutdown_event = Event()


        self.loop = False

        # Register our signal_term_handler() to be called if the user sends
        # a 'kill' to this process or does a Ctrl-C from the command line
        signal.signal(signal.SIGTERM, self.signal_term_handler)
        signal.signal(signal.SIGINT, self.signal_int_handler)

        #boot events hier
        self.leds.all_off()
            # menü anzeigen oder den Kalibrierungsmodus starten TODO

        self.free_transit(True) # nur provisorisch, solang es kein Menü gibt




    def shutdown_gondola(self):

        if self.shutdown_event.is_set():
            return

        self.shutdown_event.set()
        log.info('shutting down')
        self.mes.shutdown_event.set()
        self.mc.shutdown_event.set()
        self.remote.on_channel4_top_left = None #extend this to set all used button events to None TODO
        self.remote.on_channel4_bottom_left = None
        self.hori_motor.off(brake=False)
        self.vert_motor.off(brake=False)
        self.mes.join()
        self.mc.join()

    def signal_term_handler(self, signal, frame):
        log.info('Caught SIGTERM')
        self.shutdown_gondola()

    def signal_int_handler(self, signal, frame):
        log.info('Caught SIGINT')
        self.shutdown_gondola()

    """
    Hier einfügen der transit- und Menü-Funktionen
    Der state-Parameter in den Transit-Funktionen macht es möglich, dass die Funktionen direkt als EventHandler für die Buttons
    im Menü eingesetzt werden können.
    """

    def menu(self, state): #TODO
        if state:
            pass


    def free_transit(self, state): #TODO
        if state:
            """
            This function allows the user to freely move the gondola without any restrictions.

            Die Gondel soll nach Beeindigung des free_transit wieder an eine Startposition automatisch gefahren werden mit return_to_start TODO
            """

            # Show a picture of maybe "free movement enabled" TODO
            #ev3.screen.load_image('(was Tasten machen).png')

            # Assign event handler to each of the buttons
            self.button.on_up    = roll(self.vert_motor, self.leds.LEFT,   1)
            self.button.on_down  = roll(self.vert_motor, self.leds.LEFT,  -1)
            self.button.on_left  = roll(self.hori_motor, self.leds.RIGHT,  1)
            self.button.on_right = roll(self.hori_motor, self.leds.RIGHT, -1)
            self.button.on_enter = self.menu
            # TODO update Lokalitätsvariablen nachdem sie implementiert sind


    def auto_transit(self, state): #TODO
        if state:
            pass


    def calibrate(self, state): #TODO
        if state:
            pass

    def return_to_start(self, state): #TODO
        if state:
            pass

    def stop_motors(self, state): #TODO
        if state:
            self.hori_motor.stop(stop_action='brake')
            self.vert_motor.stop(stop_action='brake')

    

    def main(self):
        self.mts.start()
        self.mrc.start() # Hier läuft jetzt alles und wartet auf die externe Beendigung des Prozesses.
        """
        In der Init wurde das Startmenü bzw. die Kalibrierung in Form einer Methode aufgerufen. Die Beendigung dieser erfolgt immer im Aufruf einer Folgemethode.
        Das heißt zum Beispiel, wenn man einen transit-Modus beendet, dann wird danach immer die Menü-Methode aufgerufen.
        Anderes Beispiel ist, dass die aufgerufene Menü-Methode, dann die entsprechend ausgewählte Transit-Methode aufruft.
        """
        self.shutdown_event.wait()


if __name__ == '__main__':

    # Change level to logging.DEBUG for more details
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)5s %(filename)s: %(message)s")
    log = logging.getLogger(__name__)

    # Color the errors and warnings in red
    logging.addLevelName(logging.ERROR, "\033[91m  %s\033[0m" % logging.getLevelName(logging.ERROR))
    logging.addLevelName(logging.WARNING, "\033[91m%s\033[0m" % logging.getLevelName(logging.WARNING))

    log.info("Starting GRIPP3R")
    gripper = Gripper()
    gripper.main()
    log.info("Exiting GRIPP3R")