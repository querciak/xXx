# state machine for challange one

#imports:
import Sensing
from pybricks.parameters import Port, Color


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

def isTimerPassed():
    if current_time > sm_challange1_init_timer_threshold:
        return True
    else:
        return False

def stripe_reached():
    #take value from color sensor
    current_color = Sensing.Sensing.get_color()
    if current_color == Color.WHITE:
        return True
    else:
        return False

def sm_challange1_main():
    global CURRENT_STATE
    global transition_to

    if CURRENT_STATE == STATES[0]: # init
        #check valid transition
        #timer()
        if isTimerPassed() == True:
            transition_to = 1

    elif CURRENT_STATE == STATES[1]: # reachstripe
        if stripe_reached() == True:
            transition_to = 3 # maze_followline
        elif wall_reached() == True:
            transition_to = 2 # turningleft

    elif CURRENT_STATE == STATES[2]: # turningleft
        if turning_timer_passed() == True:
            transition_to = 1

    elif CURRENT_STATE == STATES[3]: # maze_followline
        #first check for the yellow button
        if yellow_button_reached() == True:
            transition_to = 5 # maze_yellowbuttonreached
        if line_ended() == True:
            transition_to = 4 # mazeturn

    elif CURRENT_STATE == STATES[4]: # mazeturn
        # check turning timer
        if maze_turningtimer_passed() == True:
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
        pass

    elif CURRENT_STATE == STATES[1]: # reachstripe
        # set speed value
        pass

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
    CURRENT_STATE = STATES[0]
    transition_to = 0