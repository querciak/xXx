# state machine for challange one

#imports:
from Sensing import Sensing
from pybricks.parameters import Port, Color
import Actions

from pybricks.tools import wait

sensing = Sensing()

''' STATES for challange1
0 'init'
1 'reachstripe'
2 'turningleft'
3 'maze_followline'
4 'mazeturn'
5 'mazepressbutton'
6 'mazeturnaround'
7 'mazewait'
8 'adaptline'
9 'emergency_state'
'''

STATES = ['init','reachstripe','turningleft','maze_followline',
'mazeturn','mazepressbutton','mazeturnaround','mazewait','adaptline','emergency_state']

# parameters
cycle_time = 10 # 10 ms
sm_challange1_init_timer_threshold = 100/cycle_time # 1sec
mazeturn_counter_threshold = 2000/cycle_time # 2 sec -> time to turn 90 degrees
searching_line_turn_threshold = 100/cycle_time

left_top = 128
left_bottom = 2
right_top = 512
right_bottom = 8



# action parameters
left_turning_speed = 90 # 45 deg/s
longitudinal_speed = -800
adaptline_manuever = []


def isTimerPassed(counter, threshold):
    if  counter > threshold:
        return True
    else:
        return False

def stripe_reached():
    # take value from color sensor
    current_color = sensing.get_color()
    if current_color == Color.WHITE:
        return True
    else:
        return False

def yellow_button_reached():
    # check whether color sensor shows yellow
    current_color = sensing.get_color()
    if current_color == Color.YELLOW:
        return True
    else:
        return False

def line_ended():
    # check whether color sensor does not show white anymore
    current_color = sensing.get_color()
    if current_color != Color.WHITE:
        return True
    else:
        return False    

def wall_reached():
    #TODO determine whether wall is reached using ultrasonic sensor
    pass

def sm_challange1_main():
    global CURRENT_STATE
    global transition_to
    global sm_challange1_init_timer
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

    # parse input data
    pressed_buttons = sensing.get_button()

    if CURRENT_STATE == STATES[0]: # init
        #check valid transition
        #timer()
        if isTimerPassed(sm_challange1_init_timer,sm_challange1_init_timer_threshold) == True:
            sm_challange1_init_timer = 0
            transition_to = 1

    elif CURRENT_STATE == STATES[1]: # reachstripe
        if stripe_reached() == True:
            transition_to = 3 # maze_followline
        elif wall_reached() == True:
            transition_to = 2 # turningleft

    elif CURRENT_STATE == STATES[2]: # turningleft
        if isTimerPassed(searching_line_turn_timer,searching_line_turn_threshold) == True:
            transition_to = 1

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
        sm_challange1_init_timer += 1

    elif CURRENT_STATE == STATES[1]: # reachstripe
        # set speed value
        Actions.get_actions().straight_speed = int(longitudinal_speed*1.6)
        Actions.get_actions().steering_speed = 0

    elif CURRENT_STATE == STATES[2]: # turningleft
        # increase timer
        searching_line_turn_threshold += 1
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
    if len(pressed_buttons) > 0:
        # reset counters
        searching_line_turn_timer = 0
        adaptline_maneuver_counter = 0
        out_from_emergency_counter = 0

        CURRENT_STATE = STATES[9]
        sum_buttons = 0
        for button in pressed_buttons:
            sum_buttons += button
        
        if sum_buttons == (left_top+right_top):
            # move forward
            Actions.get_actions().straight_speed = longitudinal_speed
            Actions.get_actions().steering_speed = 0
        elif sum_buttons == left_top:
            # turn left
            Actions.get_actions().straight_speed = 0
            Actions.get_actions().steering_speed = left_turning_speed
        elif sum_buttons == right_top:
            # turn right
            Actions.get_actions().straight_speed = 0
            Actions.get_actions().steering_speed = -left_turning_speed
        elif sum_buttons == (left_bottom+right_bottom):
            # move backward
            Actions.get_actions().straight_speed = -longitudinal_speed
            Actions.get_actions().steering_speed = 0
        elif sum_buttons == left_bottom:
            # turn right
            Actions.get_actions().straight_speed = 0
            Actions.get_actions().steering_speed = -left_turning_speed
        elif sum_buttons == right_bottom:
            # turn left
            Actions.get_actions().straight_speed = 0
            Actions.get_actions().steering_speed = left_turning_speed
    elif CURRENT_STATE == STATES[9]:
        Actions.get_actions().straight_speed = 0
        Actions.get_actions().steering_speed = 0
        out_from_emergency_counter += 1
        if out_from_emergency_counter > 20:
            CURRENT_STATE = previous_state

        '''
        button = pressed_buttons[0]
        if button == left_top:
            Actions.get_actions().steering_speed = longitudinal_speed
        elif button == left_bottom:
            Actions.get_actions().steering_speed = -longitudinal_speed
        elif button == right_top:
            Actions.get_actions().straight_speed = longitudinal_speed
        elif button == right_bottom:
        '''



def sm_challange1_init():
    #initiate variables used in sm_challange1.py
    global CURRENT_STATE
    global transition_to
    global sm_challange1_init_timer
    global mazeturn_timer
    global searching_line_turn_timer
    global adaptline_maneuver_counter
    global adaptline_manuever 
    global previous_state
    global out_from_emergency_counter

    CURRENT_STATE = STATES[0]
    transition_to = 0
    sm_challange1_init_timer = 0
    mazeturn_timer = 0
    searching_line_turn_timer = 0
    adaptline_maneuver_counter = 0
    out_from_emergency_counter = 0
    previous_state = STATES[0]

    for i in range(1,180):
        adaptline_manuever.append(left_turning_speed + 10)