#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# Create your objects here

brick = EV3Brick()

# Write your program here


# Beep. To get your attention.
brick.sound.beep()

# Clear the display
brick.display.clear()

# Print ``Hello`` near the middle of the screen
brick.display.text("Hello", (60, 50))

# Print ``World`` directly underneath it
brick.display.text("World")

# Show the current voltage
brick.display.text("Voltage is: {}".format(brick.battery.voltage()))

# Wait until a button is pressed
while not brick.buttons():
    wait(10)