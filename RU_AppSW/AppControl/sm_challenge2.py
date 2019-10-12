# state machine for challenge two

#imports:
from pybricks.parameters import Port, Color
from pybricks.tools import wait

from Sensing import Sensing
import Actions
import EmergencySolution

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
8 'lost'
'''

STATES = ['init','buttonreached','buttonpushed','dropportreached',
'payloaddropped','payloadreached','payloadpickedup','exitfound','lost']

#Constants
cycle_time = 10 # 10 ms
init_threshold = 100/cycle_time # 0.1sec
turn_threshold = 1000/cycle_time # 1sec
# mazeturn_counter_threshold = 2000/cycle_time # 2 sec -> time to turn 90 degrees
# searching_line_turn_threshold = 100/cycle_time
# back_to_automation_threshold = 200/cycle_time
# searching_line_turn_threshold
# mazeturn_counter_threshold
# back_to_automation_threshold

# action parameters
angular_velocity = 90 # 45 deg/s
velocity = -800
# adaptline_manuever = []

def is_threshold_passed(counter, threshold):
    if  counter > threshold:
        return True
    else:
        return False

def is_button_reached():
    current_color = sensing.get_color()
    if current_color == Color.WHITE:
        return True
    else:
        return False  

def is_wall_reached():
    distance = sensing.get_distance()
    if distance < 10:
        return True
    else:
        return False 

def is_button_pushed():
    return sensing.is_pressed()

def is_drop_port_reached():
    current_color = sensing.get_color()
    if current_color == Color.WHITE:
        return True
    else:
        return False  

def sm_challenge2_main():

    #check valid transitions
    if CURRENT_STATE == STATES[0]: # init
        if is_threshold_passed(init_counter,init_threshold) == True:
            init_counter = 0
        elif init_counter == 0 and is_button_reached() == True:
            transition_to = 1
        elif init_counter == 0 and is_wall_reached() == True:
            transition_to = 8 #     
    elif CURRENT_STATE == STATES[1]: # buttonreached
        if is_threshold_passed(turn_counter,turn_threshold) == True:
            turn_counter = 0
        elif turn_counter == 0 and is_button_pushed() == True:
            transition_to = 2 # 
        elif turn_counter == 0 and is_wall_reached() == True:
            transition_to = 8 # 
    # elif CURRENT_STATE == STATES[2]: # buttonpushed
    #     if is_drop_port_reached() == True:
    #         transition_to = 3
    # elif CURRENT_STATE == STATES[3]: # dropportreached
    #     #first check for the yellow button
    #     if yellow_button_reached() == True:
    #         transition_to = 5 # maze_yellowbuttonreached
    #     if line_ended() == True:
    #         transition_to = 8 # mazeturn
    # elif CURRENT_STATE == STATES[4]: # payloaddropped
    #     # check turning timer
    #     if isTimerPassed(mazeturn_timer, mazeturn_counter_threshold) == True:
    #         transition_to = 3
    #         mazeturn_timer = 0
    # elif CURRENT_STATE == STATES[5]: # payloadreached
    #     pass
    # elif CURRENT_STATE == STATES[6]: # payloadpickedup
    #     pass
    # elif CURRENT_STATE == STATES[7]: # exitfound
    #     pass

    # do transition
    if CURRENT_STATE != STATES[transition_to]:
        CURRENT_STATE = STATES[transition_to]

    # action
    if CURRENT_STATE == STATES[0] and is_threshold_passed(init_counter,init_threshold) == False: # init
        # wait
        init_counter += 1
    elif CURRENT_STATE == STATES[0] and init_counter == 0: # init
        # set speed value
        Actions.get_actions().straight_speed = int(velocity*1.6)
        Actions.get_actions().steering_speed = 0
    elif CURRENT_STATE == STATES[1] and is_threshold_passed(turn_counter,turn_threshold): # buttonreached
        # set speed value
        Actions.get_actions().straight_speed = 0
        Actions.get_actions().steering_speed = angular_velocity  
    elif CURRENT_STATE == STATES[1] and init_counter == 0: # init
        # set speed value
        Actions.get_actions().straight_speed = int(velocity*1.6)
        Actions.get_actions().steering_speed = 0     
    # elif CURRENT_STATE == STATES[2]: # buttonpushed
    #     # increase timer
    #     searching_line_turn_timer += 1
    #     # update speed values
    #     Actions.get_actions().steering_speed = angular_velocity # 45 deg/s
    #     Actions.get_actions().straight_speed = 0
    # elif CURRENT_STATE == STATES[3]: # dropportreached
    #     Actions.get_actions().straight_speed = velocity
    #     Actions.get_actions().steering_speed = 0
    # elif CURRENT_STATE == STATES[4]: # payloaddropped
    #     # increase timer
    #     mazeturn_timer += 1
    #     # update speed values
    #     Actions.get_actions().straight_speed = 0
    #     Actions.get_actions().steering_speed = angular_velocity # 45 deg/sec
    # elif CURRENT_STATE == STATES[5]: # payloadreached
    #     Actions.get_actions().straight_speed = 0
    #     Actions.get_actions().steering_speed = 0
    # elif CURRENT_STATE == STATES[6]: # payloadpickedup
    #     pass
    # elif CURRENT_STATE == STATES[7]: # exitfound
    #     pass

    # emergency solution
    emergency_evaluation = EmergencySolution.get_emergency_solution().check_for_emergency_solution(CURRENT_STATE)
    if emergency_evaluation[0]:
        # reset counters
        # searching_line_turn_timer = 0
        # adaptline_maneuver_counter = 0
        out_from_emergency_counter = 0

def sm_challenge2_init():
    #initialize values
    global CURRENT_STATE
    global PREVIOUS_STATE
    global transition_to

    #counters
    global init_counter
    global turn_counter
    # searching_line_turn_timer = 0
    # adaptline_maneuver_counter = 0
    global out_from_emergency_counter

    CURRENT_STATE = STATES[0]
    PREVIOUS_STATE = STATES[0]
    transition_to = 0

    init_counter = 0
    turn_counter = 0
    # searching_line_turn_timer = 0
    # adaptline_maneuver_counter = 0
    out_from_emergency_counter = 0
    
    # adaptline_manuever = [angular_velocity]*100 + [-angular_velocity]*100