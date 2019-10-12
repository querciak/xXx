# state machine for challenge one

#imports:
import Sensing
from pybricks.parameters import Port, Color
import Actions
import EmergencySolution

from pybricks.tools import wait


''' STATES for challenge1
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
sm_challenge1_init_timer_threshold = 100/cycle_time # 0.1sec
mazeturn_counter_threshold = 2000/cycle_time # 2 sec -> time to turn 90 degrees
searching_line_turn_threshold = 100/cycle_time


# action parameters
adaptline_manuever = []


def isTimerPassed(counter, threshold):
    if  counter > threshold:
        return True
    else:
        return False

def stripe_reached():
    # take value from color sensor
    current_color = Sensing.get_sensing().get_color()
    if current_color == Color.WHITE:
        return True
    else:
        return False

def yellow_button_reached():
    # check whether color sensor shows yellow
    current_color = Sensing.get_sensing().get_color()
    if current_color == Color.YELLOW:
        return True
    else:
        return False

def line_ended():
    # check whether color sensor does not show white anymore
    current_color = Sensing.get_sensing().get_color()
    if current_color != Color.WHITE:
        return True
    else:
        return False    

def wall_reached():
    #TODO determine whether wall is reached using ultrasonic sensor
    pass

def sm_challenge1_main():
    global CURRENT_STATE
    global transition_to
    global sm_challenge1_init_timer
    global mazeturn_timer
    global searching_line_turn_timer
    global searching_line_turn_threshold
    global mazeturn_counter_threshold
    global adaptline_maneuver_counter
    global previous_state
    global out_from_emergency_counter

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
        Actions.get_actions().straight_speed = int(Actions.get_actions().suggested_longitudinal_speed*1.6)
        Actions.get_actions().steering_speed = 0

    elif CURRENT_STATE == STATES[2]: # turningleft
        # increase timer
        searching_line_turn_timer += 1
        # update speed values
        Actions.get_actions().steering_speed = Actions.get_actions().suggested_left_turn_speed # 45 deg/s
        Actions.get_actions().straight_speed = 0

    elif CURRENT_STATE == STATES[3]: # maze_followline
        Actions.get_actions().straight_speed = Actions.get_actions().suggested_longitudinal_speed
        Actions.get_actions().steering_speed = 0

    elif CURRENT_STATE == STATES[4]: # mazeturn
        # increase timer
        mazeturn_timer += 1
        # update speed values
        Actions.get_actions().straight_speed = 0
        Actions.get_actions().steering_speed = Actions.get_actions().suggested_left_turn_speed # 45 deg/sec

    elif CURRENT_STATE == STATES[5]: # mazepressbutton
        Actions.get_actions().straight_speed = 0
        Actions.get_actions().steering_speed = 0

    elif CURRENT_STATE == STATES[6]: # mazeturnaround
        pass

    elif CURRENT_STATE == STATES[7]: # mazewait_for_obstacletomove
        pass

    elif CURRENT_STATE == STATES[8]:
        # perform_maneuver
        Actions.get_actions().straight_speed = Actions.get_actions().suggested_longitudinal_speed/10
        Actions.get_actions().steering_speed = adaptline_manuever[adaptline_maneuver_counter]
        adaptline_maneuver_counter += 1

    # emergency solution
    emergency_evaulation = EmergencySolution.get_emergency_solution().check_for_emergency_solution(CURRENT_STATE)
    if emergency_evaulation[0]:
        # reset counters
        searching_line_turn_timer = 0
        adaptline_maneuver_counter = 0
        out_from_emergency_counter = 0
    # update state
    CURRENT_STATE = emergency_evaulation[1]



def sm_challenge1_init():
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
    
    adaptline_manuever = [Actions.get_actions().suggested_left_turn_speed]*100 + [-Actions.get_actions().suggested_left_turn_speed]*100