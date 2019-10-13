# state machine for challenge two

#imports:
from pybricks.parameters import Port, Color
from pybricks.tools import wait

from collections import deque

import Sensing
import Actions

# action parameters
angular_velocity = 90 # 45 deg/s
velocity = -800

# store reflection-time function
maxlen_of_reflection = 21       # storage for half a second
full_white_reflection = 46      # above this value it is considered full white
nominal_reflection = 30         # value corresponding to optimal tracking
threshold_nom_reflection = 6    # threshold in which nominal is accepted
amount_of_change = 10           # amount which shall be changed in the time range below
quick_rate_of_change = 5
slow_rate_of_change = 20
dark_color_threshold = 15
filter_gain = 15

class line_following():
    def __init__(self):
        self.reflection_time = []

    def update_reflection(self):
        new_sample = Sensing.get_sensing().get_reflection()
        if len(self.reflection_time) == maxlen_of_reflection:
            # migrate elements
            for i in range(1,maxlen_of_reflection):
                self.reflection_time[i-1] = self.reflection_time[i]
            self.reflection_time[maxlen_of_reflection-1] = new_sample
        else:
            self.reflection_time.append(new_sample)


    def determine_change_rate(self,rate):
        difference = self.reflection_time[maxlen_of_reflection-1] - self.reflection_time[len(self.reflection_time)-rate]
        if difference >= amount_of_change:
            return True
        else:
            return False
    
    def determine_change_rate_signed(self,rate):
        difference = self.reflection_time[maxlen_of_reflection-1] - self.reflection_time[len(self.reflection_time)-rate]
        if difference > 0:
            return 1
        elif difference < 0:
            return -1

    def follow_the_line(self):
        suggested_long_vel = Actions.get_actions().suggested_longitudinal_speed
        suggested_ang_vel = Actions.get_actions().suggested_left_turn_speed
        longitudinal_velocity = Actions.get_actions().straight_speed
        angular_velocity = Actions.get_actions().steering_speed

        half_length = int(maxlen_of_reflection/2)
        average_of_first_points = 0
        average_of_last_points = 0
        for i in range(0,half_length):
            average_of_first_points += self.reflection_time[i]
            average_of_last_points += self.reflection_time[half_length+i]
        average_of_first_points = int(average_of_first_points/half_length)
        average_of_last_points = int(average_of_last_points/half_length)

        if len(self.reflection_time) == maxlen_of_reflection:
            # do the calculations here
            if int(average_of_last_points) in range(nominal_reflection-threshold_nom_reflection,nominal_reflection+threshold_nom_reflection):
                # track changes
                slow_rate_analysis = self.determine_change_rate(slow_rate_of_change)
                if slow_rate_analysis:
                    # adjust a little by going right
                    longitudinal_velocity = suggested_long_vel/8
                    angular_velocity = -suggested_ang_vel/3
            elif self.determine_change_rate(quick_rate_of_change):
                # we might need to turn left or right
                if filter_gain < len([sample > full_white_reflection for sample in self.reflection_time]):
                    # we have to turn right
                    longitudinal_velocity = 0
                    angular_velocity = -suggested_ang_vel
                else:
                    # we have to turn left
                    longitudinal_velocity = 0
                    angular_velocity = suggested_ang_vel


            #lowest priority
            elif average_of_last_points > full_white_reflection:
                # check history whether it was 
                longitudinal_velocity = suggested_long_vel/3
                angular_velocity = -suggested_ang_vel/2

            else:
                longitudinal_velocity = suggested_long_vel/3
                angular_velocity = 0

        else:
            pass # do nothing -> wait for more sample (it only affects the first half second)

        Actions.get_actions().straight_speed = longitudinal_velocity
        Actions.get_actions().steering_speed = angular_velocity

line_follower = line_following()

def get_line_follower():
    return line_follower