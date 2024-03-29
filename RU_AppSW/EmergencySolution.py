import Sensing
import Actions

left_top = 128
left_bottom = 2
right_top = 512
right_bottom = 8

switch_button = 256

class EmergencySolution():
    def __init__(self):
        self.previous_state = ''
        self.leave_emergency_state_counter = 0
        self.leave_emergency_state_threshold = 1000
        self.automotive_switch = True
        self.just_switched = False
        self.turn_automotive_counter = 0
        self.automotive_counter_threshold = 200

    def check_for_emergency_solution(self,current_state):
        #if button pressed, channels etc..
        pressed_buttons_list = Sensing.get_sensing().get_button()

        ch1_pressed_buttons = pressed_buttons_list[0]
        ch4_pressed_buttons = pressed_buttons_list[3]

        if len(ch1_pressed_buttons) > 0:
            self.leave_emergency_state_counter = 0
            # enterred to emergency_state
            ret_val = True

            CURRENT_STATE = 'emergency_state' # emergency solution -> remote control
            sum_buttons = 0
            for button in ch1_pressed_buttons:
                sum_buttons += button
            
            if sum_buttons == (left_top+right_top):
                # move forward
                Actions.get_actions().straight_speed = Actions.get_actions().suggested_longitudinal_speed
                Actions.get_actions().steering_speed = 0
            elif sum_buttons == left_top:
                # turn left
                Actions.get_actions().straight_speed = int(Actions.get_actions().suggested_longitudinal_speed/2)
                Actions.get_actions().steering_speed = Actions.get_actions().suggested_left_turn_speed
            elif sum_buttons == right_top:
                # turn right
                Actions.get_actions().straight_speed = int(Actions.get_actions().suggested_longitudinal_speed/2)
                Actions.get_actions().steering_speed = -Actions.get_actions().suggested_left_turn_speed
            elif sum_buttons == (left_bottom+right_bottom):
                # move backward
                Actions.get_actions().straight_speed = -Actions.get_actions().suggested_longitudinal_speed
                Actions.get_actions().steering_speed = 0
            elif sum_buttons == left_bottom:
                # turn right
                Actions.get_actions().straight_speed = 0
                Actions.get_actions().steering_speed = -Actions.get_actions().suggested_left_turn_speed
            elif sum_buttons == right_bottom:
                # turn left
                Actions.get_actions().straight_speed = 0
                Actions.get_actions().steering_speed = Actions.get_actions().suggested_left_turn_speed
            elif sum_buttons == switch_button:
                if self.just_switched:
                    if self.turn_automotive_counter <= self.automotive_counter_threshold:
                        self.turn_automotive_counter += 1
                    else:
                        self.just_switched = False

                else:
                    if self.automotive_switch:
                        self.automotive_switch = False
                        self.just_switched = True
                        self.turn_automotive_counter = 0
                    else:
                        self.automotive_switch = True
                        self.just_switched = True
                        self.turn_automotive_counter = 0

        elif len(ch4_pressed_buttons) > 0:
            self.leave_emergency_state_counter = 0
            ret_val = True

            CURRENT_STATE = 'emergency_state' # emergency solution -> remote control
            sum_buttons = 0
            for button in ch4_pressed_buttons:
                sum_buttons += button

            if sum_buttons == left_top:
                Actions.get_actions().arm_speed = -100
            elif sum_buttons == right_top:
                Actions.get_actions().arm_speed = 100
            elif sum_buttons == left_bottom:
                Actions.get_actions().arm_speed = 0
                Actions.get_actions().steering_speed = 0
                Actions.get_actions().straight_speed = 0
            elif sum_buttons == right_bottom:
                Actions.get_actions().steering_speed = 0
                Actions.get_actions().straight_speed = 0

                # if self.just_switched:
                #     if self.turn_automotive_counter <= self.automotive_counter_threshold:
                #         self.turn_automotive_counter += 1
                #     else:
                #         self.just_switched = False

                # else:
                #     if self.automotive_switch:
                #         self.automotive_switch = False
                #         self.just_switched = True
                #         self.turn_automotive_counter = 0
                #     else:
                #         self.automotive_switch = True
                #         self.just_switched = True
                #         self.turn_automotive_counter = 0

        elif current_state == 'emergency_state':
            Actions.get_actions().straight_speed = 0
            Actions.get_actions().steering_speed = 0
            Actions.get_actions().arm_speed = 0
            if self.automotive_switch == True:
                self.leave_emergency_state_counter += 1
                if self.leave_emergency_state_counter > self.leave_emergency_state_threshold:
                    ret_val = False
                    CURRENT_STATE = self.previous_state # back to state before corrigation
        else:
            ret_val = False
            CURRENT_STATE = current_state

        #return boolean stating we are in emergency state or not and the current state
        return [ret_val,CURRENT_STATE]

    def transit_to_emergency_state(self,current_state):
        self.previous_state = current_state


emergency_solution = EmergencySolution()

def get_emergency_solution():
    return emergency_solution