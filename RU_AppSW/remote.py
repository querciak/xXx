#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

# Write your program here
class Remote():
    def __init__(self) -> None:
        super().__init__()

        self.inf_sensor = InfraredSensor(Port.S3)

    def get_button(self):
        pressButton = self.inf_sensor.buttons(1)
        brick.display.text(str(pressButton))
        return pressButton

    def get_distance(self):
        dist = self.inf_sensor.distance()
        brick.display.text(str(dist))
        return dist

infSensor = Remote()
while True:
    pressed_button = infSensor.get_button()
    wait(1000)