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
1 'findline'
2 'turn'
3 'followline'
4 'dropload'
5 'pickupload'
6 'findexit'
'''

STATES = ['init','findline','turn','followline','dropload','pickupload','findexit']

#Constants
cycle_time = 10 # 10 ms
init_threshold = 100/cycle_time # 0.1sec
threshold = 1000 # 1sec

# action parameters
angular_velocity = 90 # 45 deg/s
velocity = -800

def is_threshold_passed(counter, threshold):
    if  counter > threshold:
        return True
    else:
        return False

def is_white_line_reached():
    current_color = sensing.get_color()
    if current_color == Color.WHITE:
        line_counter += 1
        return True
    else:
        return False  

def is_white_line_finished():
    reflection = sensing.get_reflection()
    if reflection < 40:
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
        #wait
        if is_threshold_passed(counter,init_threshold) == True:
            counter = 0
            transition_to = 1
    elif CURRENT_STATE == STATES[1]: # findline
        #follow a line or turn
        if counter == 0 and is_white_line_reached() == True:
            if line_counter == 1:
                rl = -1
                transition_to = 2
            elif line_counter == 3:
                transition_to = 3
        #turn
        elif counter == 0 and is_wall_reached() == True:
            transition_to = 2    
    elif CURRENT_STATE == STATES[2]: # turn
        #find a line
        if counter == 0 and is_threshold_passed(counter,threshold) == True:
            turn_counter += 1
            transition_to = 1
        #follow a line
        if counter == 0 and is_threshold_passed(counter,threshold) == True:
            turn_counter += 1
            transition_to = 3
        #turn
        elif counter == 0 and is_wall_reached() == True:
            transition_to = 2   
    elif CURRENT_STATE == STATES[3]: # followline
        #find a line
        if counter == 0 and is_white_line_finished() == True:
            transition_to = 1
        #turn
        elif counter == 0 and is_wall_reached() == True:
            transition_to = 2   
    # elif CURRENT_STATE == STATES[4]: # dropload
    #     #go to next
    #     elif counter == 0 and is_drop_port_reached() == True:
    #         transition_to = 5 
    #     #go to another state
    #     elif counter == 0 and is_wall_reached() == True:
    #         transition_to = 8 
    # elif CURRENT_STATE == STATES[5]: # pickupload
    #     #go to next
    #     elif counter == 0 and is_drop_port_reached() == True:
    #         transition_to = 6
    #     #go to another state
    #     elif counter == 0 and is_wall_reached() == True:
    #         transition_to = 8 
    #elif CURRENT_STATE == STATES[6]: # find exit

    # do transition
    if CURRENT_STATE != STATES[transition_to]:
        CURRENT_STATE = STATES[transition_to]

    # action
    if CURRENT_STATE == STATES[0] and is_threshold_passed(counter,init_threshold) == False: # init
        # wait
        counter += 1
    elif CURRENT_STATE == STATES[1] and is_threshold_passed(counter,threshold) == False: # findline
        Actions.get_actions().straight_speed = velocity
        Actions.get_actions().steering_speed = 0     
    elif CURRENT_STATE == STATES[2] and is_threshold_passed(counter,threshold) == False: # turn
        Actions.get_actions().straight_speed = 0
        Actions.get_actions().steering_speed = rl*angular_velocity  
    elif CURRENT_STATE == STATES[3]: # followline
        Actions.get_actions().straight_speed = velocity
        Actions.get_actions().steering_speed = 0
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
    global counter
    global line_counter
    global turn_counter
    global rl
    global out_from_emergency_counter

    CURRENT_STATE = STATES[0]
    PREVIOUS_STATE = STATES[0]
    transition_to = 0

    counter = 0
    line_counter = 0
    turn_counter = 0
    rl = 1 #left
    out_from_emergency_counter = 0
    
    # adaptline_manuever = [angular_velocity]*100 + [-angular_velocity]*100