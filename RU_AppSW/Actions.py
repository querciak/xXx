from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase


class Actions:

    def __init__(self):
        super().__init__()
        self.straight_speed = 100
        self.steering_speed = 45
        self._left_motor = Motor(Port.A)
        self._right_motor = Motor(Port.B)
        self.wheels = DriveBase(self._left_motor, self._right_motor, wheel_diameter=56, axle_track=114)


    def turn(self, angle=0):
        self.wheels.drive_time(0, 45, 1000)

    def straight(self, speed=None):
        self.wheels.drive(speed if speed else self.straight_speed)
