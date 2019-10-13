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
maxlen_of_reflection = 60       # storage for half a second
full_white_reflection = 46      # above this value it is considered full white
nominal_reflection = 30         # value corresponding to optimal tracking
threshold_nom_reflection = 6    # threshold in which nominal is accepted
amount_of_change = 10           # amount which shall be changed in the time range below
quick_rate_of_change = 10
slow_rate_of_change = 40
dark_color_threshold = 15
filter_gain = 30

class line_following():
    def __init__(self):
        self.reflection_time = []
        self.turning_counter = 0
        self.turning_limit = 100
        self.turn_back_performed = False
        self.turn_currently_performed = False
        self.maneuver_direction = 0 # 0-left, 1-right

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
        # dR = r2 - r1
        difference = self.reflection_time[maxlen_of_reflection-1] - self.reflection_time[len(self.reflection_time)-rate]
        # difference is positive meaning the reflection value is increased
        if difference >= amount_of_change:
            return True
        else:
            return False
    
    def determine_change_rate_signed(self,rate):
        difference = self.reflection_time[maxlen_of_reflection-1] - self.reflection_time[len(self.reflection_time)-rate]
        if difference >= amount_of_change:
            return 1 # difference is positive and bigger then threshold
        elif difference <= amount_of_change:
            return -1 # difference is positive and smaller than threshold
        else:
            return 0 # we are following the track

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
            slow_rate_analysis = self.determine_change_rate_signed(slow_rate_of_change)
            # 1  -> adjustment to right
            # -1 -> adjusment to left
            # 0  -> keep ahead
            quick_change_analysis = self.determine_change_rate_signed(quick_rate_of_change)
            # 1  -> line found
            # -1 -> line left
            # 0  -> keep ahead
            
            # check whether turning is currently performed
            if self.turn_currently_performed or self.turn_back_performed:
                # check for path, if line found then stop turning
                if average_of_last_points > (nominal_reflection - threshold_nom_reflection):
                    self.turn_currently_performed = False
                    self.turning_counter = 0
                    angular_velocity = 0
                    longitudinal_velocity = suggested_long_vel/2
                # limit reached, no line found -> turn back and move ahead
                elif self.turning_counter >= self.turning_limit:
                    if self.turn_currently_performed:
                        #stop manuever and turn back
                        self.turn_currently_performed = False
                        self.turn_back_performed = True
                        self.turning_counter = 0
                        # set back direction accordingly
                        if self.maneuver_direction == 0:
                            #left , now to right
                            angular_velocity = -suggested_ang_vel/2
                            longitudinal_velocity = 0
                        else:
                            angular_velocity = suggested_ang_vel/2
                            longitudinal_velocity = 0
                    else: #self.turn_back_performed
                        self.turn_currently_performed = False
                        self.turn_back_performed = False
                        self.turning_counter = 0
                    
                else:
                    self.turning_counter += 1


            # around the nominal value
            elif int(average_of_last_points) in range(nominal_reflection-threshold_nom_reflection,nominal_reflection+threshold_nom_reflection):
                # track changes slowly
                if slow_rate_analysis == 1:
                    # adjust a little by going right
                    longitudinal_velocity = suggested_long_vel/6
                    angular_velocity = -suggested_ang_vel/3
                elif slow_rate_analysis == -1:
                    # adjust a little by going left
                    longitudinal_velocity = suggested_long_vel/6
                    angular_velocity = suggested_ang_vel/3
                else:
                    longitudinal_velocity = suggested_long_vel/4
                    angular_velocity = 0
            elif quick_change_analysis == 1: # we just arrived to the path or nominal increased
                # we might need to turn left or right
                if filter_gain < len([sample > full_white_reflection for sample in self.reflection_time]):
                    # we have to turn right
                    longitudinal_velocity = 0
                    angular_velocity = -suggested_ang_vel
                    self.turn_currently_performed = True
                    self.maneuver_direction = 1
                else:
                    # we have to turn left
                    longitudinal_velocity = 0
                    angular_velocity = suggested_ang_vel
                    self.turn_currently_performed = True
                    self.maneuver_direction = 0
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