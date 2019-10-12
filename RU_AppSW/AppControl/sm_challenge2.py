# state machine for challenge two

#imports:
from Sensing import Sensing
from pybricks.parameters import Port, Color
import Actions

from pybricks.tools import wait

sensing = Sensing()

''' STATES for challenge2
0 'init'
1 'buttonreached'
2 'buttonpushed'
3 'dropportreached'
4 'payloaddropped'
5 'payloadreached'
6 'payloadpickedup'
7 'exitfound'
'''

STATES = ['init','buttonreached','buttonpushed','dropportreached',
'payloaddropped','payloadreached','payloadpickedup','exitfound']

# parameters
cycle_time = 10 # 10 ms
sm_challenge1_init_timer_threshold = 100/cycle_time # 0.1sec
mazeturn_counter_threshold = 2000/cycle_time # 2 sec -> time to turn 90 degrees
searching_line_turn_threshold = 100/cycle_time
back_to_automation_threshold = 200/cycle_time

# left_top = 128
# left_bottom = 2
# right_top = 512
# right_bottom = 8

# action parameters
angular_velocity = 90 # 45 deg/s
velocity = -800
# adaptline_manuever = []


# def isTimerPassed(counter, threshold):
#     if  counter > threshold:
#         return True
#     else:
#         return False

def is_button_reached():
    # take value from color sensor
    current_color = sensing.get_color()
    if current_color == Color.WHITE:
        return True
    else:
        return False  

def sm_challenge2_main():
    global CURRENT_STATE
    global transition_to
    global sm_challenge1_init_timer
    global mazeturn_timer
    global searching_line_turn_timer
    global searching_line_turn_threshold
    global mazeturn_counter_threshold
    global adaptline_maneuver_counter
    global left_top
    global left_bottom
    global right_top
    global right_bottom
    global previous_state
    global out_from_emergency_counter
    global back_to_automation_threshold

    # parse input data
    pressed_buttons = sensing.get_button()

    if CURRENT_STATE == STATES[0]: # init
        #check valid transition
        #timer()
        if isTimerPassed(sm_challenge1_init_timer,sm_challenge1_init_timer_threshold) == True:
            sm_challenge1_init_timer = 0
            transition_to = 1

    elif CURRENT_STATE == STATES[1]: # reachstripe
        if stripe_reached() == True:
            transition_to = 3 # maze_followline
        elif wall_reached() == True:
            transition_to = 2 # turningleft

    elif CURRENT_STATE == STATES[2]: # turningleft
        if isTimerPassed(searching_line_turn_timer,searching_line_turn_threshold) == True:
            transition_to = 1
            searching_line_turn_timer = 0

    elif CURRENT_STATE == STATES[3]: # maze_followline
        #first check for the yellow button
        if yellow_button_reached() == True:
            transition_to = 5 # maze_yellowbuttonreached
        if line_ended() == True:
            transition_to = 8 # mazeturn

    elif CURRENT_STATE == STATES[4]: # mazeturn
        # check turning timer
        if isTimerPassed(mazeturn_timer, mazeturn_counter_threshold) == True:
            transition_to = 3
            mazeturn_timer = 0

    elif CURRENT_STATE == STATES[5]: # mazepressbutton
        pass

    elif CURRENT_STATE == STATES[6]: # mazeturnaround
        pass
    elif CURRENT_STATE == STATES[7]: # mazewait
        pass
    elif CURRENT_STATE == STATES[8]: # adaptline
        if isTimerPassed(adaptline_maneuver_counter,len(adaptline_manuever)-1):
            transition_to = 4 # mazeturn
            adaptline_maneuver_counter = 0
        elif stripe_reached() == True:
            transition_to = 3 # maze_followline

    # do transition
    if CURRENT_STATE != STATES[transition_to]:
        CURRENT_STATE = STATES[transition_to]

    # action
    if CURRENT_STATE == STATES[0]: # init
        # wait
        sm_challenge1_init_timer += 1

    elif CURRENT_STATE == STATES[1]: # reachstripe
        # set speed value
        Actions.get_actions().straight_speed = int(longitudinal_speed*1.6)
        Actions.get_actions().steering_speed = 0

    elif CURRENT_STATE == STATES[2]: # turningleft
        # increase timer
        searching_line_turn_timer += 1
        # update speed values
        Actions.get_actions().steering_speed = left_turning_speed # 45 deg/s
        Actions.get_actions().straight_speed = 0

    elif CURRENT_STATE == STATES[3]: # maze_followline
        Actions.get_actions().straight_speed = longitudinal_speed
        Actions.get_actions().steering_speed = 0

    elif CURRENT_STATE == STATES[4]: # mazeturn
        # increase timer
        mazeturn_timer += 1
        # update speed values
        Actions.get_actions().straight_speed = 0
        Actions.get_actions().steering_speed = left_turning_speed # 45 deg/sec

    elif CURRENT_STATE == STATES[5]: # mazepressbutton
        Actions.get_actions().straight_speed = 0
        Actions.get_actions().steering_speed = 0

    elif CURRENT_STATE == STATES[6]: # mazeturnaround
        pass

    elif CURRENT_STATE == STATES[7]: # mazewait_for_obstacletomove
        pass

    elif CURRENT_STATE == STATES[8]:
        # perform_maneuver
        Actions.get_actions().straight_speed = longitudinal_speed/10
        Actions.get_actions().steering_speed = adaptline_manuever[adaptline_maneuver_counter]
        adaptline_maneuver_counter += 1

    # emergency solution
    # if len(pressed_buttons) > 0:
    #     # reset counters
    #     searching_line_turn_timer = 0
    #     adaptline_maneuver_counter = 0
    #     out_from_emergency_counter = 0

    #     CURRENT_STATE = STATES[9] # emergency solution -> remote control
    #     sum_buttons = 0
    #     for button in pressed_buttons:
    #         sum_buttons += button
        
    #     if sum_buttons == (left_top+right_top):
    #         # move forward
    #         Actions.get_actions().straight_speed = longitudinal_speed
    #         Actions.get_actions().steering_speed = 0
    #         Actions.get_actions().arm_speed = 100
    #     elif sum_buttons == left_top:
    #         # turn left
    #         Actions.get_actions().straight_speed = int(longitudinal_speed/2)
    #         Actions.get_actions().steering_speed = left_turning_speed
    #     elif sum_buttons == right_top:
    #         # turn right
    #         Actions.get_actions().straight_speed = int(longitudinal_speed/2)
    #         Actions.get_actions().steering_speed = -left_turning_speed
    #     elif sum_buttons == (left_bottom+right_bottom):
    #         # move backward
    #         Actions.get_actions().straight_speed = -longitudinal_speed
    #         Actions.get_actions().steering_speed = 0
    #         Actions.get_actions().move_backward_arm()
    #     elif sum_buttons == left_bottom:
    #         # turn right
    #         Actions.get_actions().straight_speed = 0
    #         Actions.get_actions().steering_speed = -left_turning_speed
    #     elif sum_buttons == right_bottom:
    #         # turn left
    #         Actions.get_actions().straight_speed = 0
    #         Actions.get_actions().steering_speed = left_turning_speed
    # elif CURRENT_STATE == STATES[9]:
    #     Actions.get_actions().straight_speed = 0
    #     Actions.get_actions().steering_speed = 0
    #     out_from_emergency_counter += 1
    #     if out_from_emergency_counter > back_to_automation_threshold:
    #         CURRENT_STATE = previous_state # back to state before corrigation



def sm_challenge2_init():
    #initiate variables used in sm_challenge1.py
    global CURRENT_STATE
    global transition_to
    global sm_challenge1_init_timer
    global mazeturn_timer
    global searching_line_turn_timer
    global adaptline_maneuver_counter
    global adaptline_manuever 
    global previous_state
    global out_from_emergency_counter

    CURRENT_STATE = STATES[0]
    transition_to = 0
    sm_challenge1_init_timer = 0
    mazeturn_timer = 0
    searching_line_turn_timer = 0
    adaptline_maneuver_counter = 0
    out_from_emergency_counter = 0
    previous_state = STATES[0]
    
    adaptline_manuever = [left_turning_speed]*100 + [-left_turning_speed]*100