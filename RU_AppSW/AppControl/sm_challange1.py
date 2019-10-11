# state machine for challange one

#imports:
from Sensing import Sensing
from pybricks.parameters import Port, Color
import Actions

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
'''

STATES = ['init','reachstripe','turningleft','maze_followline',
'mazeturn','mazepressbutton','mazeturnaround','mazewait']

# parameters
cycle_time = 10 # 10 ms
sm_challange1_init_timer_threshold = 100/cycle_time # 1sec
mazeturn_counter_threshold = 200/cycle_time # 2 sec -> time to turn 90 degrees
searching_line_turn_threshold = 10/cycle_time

# action parameters
left_turning_speed = -90 # 45 deg/s
longitudinal_speed = -150


def isTimerPassed(counter, threshold):
    if  counter > threshold:
        return True
    else:
        return False

def stripe_reached():
    #take value from color sensor
    current_color = sensing.get_color()
    if current_color == Color.WHITE:
        return True
    else:
        return False

def yellow_button_reached():
    #check whether color sensor shows yellow
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

    print(sensing.get_color())

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
            transition_to = 4 # mazeturn

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

    # do transition
    if CURRENT_STATE != STATES[transition_to]:
        CURRENT_STATE = STATES[transition_to]

    # action
    if CURRENT_STATE == STATES[0]: # init
        # wait
        sm_challange1_init_timer += 1

    elif CURRENT_STATE == STATES[1]: # reachstripe
        # set speed value
        Actions.get_actions().straight_speed = longitudinal_speed
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


def sm_challange1_init():
    #initiate variables used in sm_challange1.py
    global CURRENT_STATE
    global transition_to
    global sm_challange1_init_timer
    global mazeturn_timer
    global searching_line_turn_timer

    CURRENT_STATE = STATES[0]
    transition_to = 0
    sm_challange1_init_timer = 0
    mazeturn_timer = 0
    searching_line_turn_timer = 0