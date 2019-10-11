from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase

class Actions:

    def __init__(self):
        super().__init__()
        self.straight_speed = 0
        self.steering_speed = 0
        self._left_motor = Motor(Port.D)
        self._right_motor = Motor(Port.A)
        self._wheels = DriveBase(self._left_motor, self._right_motor, wheel_diameter=56, axle_track=114)

    def turn(self, angle=0):
        self._wheels.drive_time(0, 45, 1000)

    def straight(self, speed=None):
        self._wheels.drive(speed if speed else self.straight_speed, steering=0)

    def actuate(self):
        self._wheels.drive(self.straight_speed,self.steering_speed)


action = Actions()

def get_actions():
    return action