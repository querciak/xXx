# state machine for challenge two

#imports:
from pybricks.parameters import Port, Color
from pybricks.tools import wait

from Sensing import Sensing
import Actions
import EmergencySolution

sensing = Sensing()

# action parameters
angular_velocity = 90 # 45 deg/s
velocity = -800

def follow_the_line():
    reflection_value = sensing.get_reflection()
    if reflection_value > 40 and reflection_value < 60:
        Actions.get_actions().straight_speed = velocity
        Actions.get_actions().steering_speed = 0
    elif reflection_value > 40:
        Actions.get_actions().straight_speed = 0
        Actions.get_actions().steering_speed = angular_velocity
    elif reflection_value < 60:
        Actions.get_actions().straight_speed = 0
        Actions.get_actions().steering_speed = -angular_velocity 