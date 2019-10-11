# state machine for challange one

#imports:
from Sensing import Sensing
from pybricks.parameters import Port, Color
from Actions import Actions

action = Actions()
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

sm_challange1_init_timer_threshold = 1000 # 1sec
mazeturn_counter_threshold = 1500 # 1,5 sec -> time to turn 90 degrees
searching_line_turn_threshold = 100


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
        if isTimerPassed(mazeturn_timer,mazeturn_counter_threshold) == True:
            transition_to = 3

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
        action.straight_speed = 100
        action.steering_speed = 0

    elif CURRENT_STATE == STATES[2]: # turningleft
        pass

    elif CURRENT_STATE == STATES[3]: # maze_followline
        pass

    elif CURRENT_STATE == STATES[4]: # mazeturn
        pass

    elif CURRENT_STATE == STATES[5]: # mazepressbutton
        pass

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