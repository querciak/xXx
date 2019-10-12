from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase

class Actions:

    def __init__(self):
        super().__init__()
        self.straight_speed = 0
        self.steering_speed = 0
        self.arm_speed = 0
        self.suggested_longitudinal_speed = -120 # going forward
        self.suggested_left_turn_speed = 90
        self._left_motor = Motor(Port.D)
        self._right_motor = Motor(Port.A)
        self._arm_motor = Motor(Port.C)
        self._wheels = DriveBase(self._left_motor, self._right_motor, wheel_diameter=56, axle_track=114)

    def turn(self, angle=0):
        self._wheels.drive_time(0, 45, 1000)

    def straight(self, speed=None):
        self._wheels.drive(speed if speed else self.straight_speed, steering=0)

    def actuate(self):
        self._wheels.drive(self.straight_speed,self.steering_speed)

    def move_arm(self):
        self._arm_motor.run(self.arm_speed)

    def get_speed_of_motors(self):
        return [self._left_motor.speed(),self._right_motor.speed()]


action = Actions()

def get_actions():
    return action