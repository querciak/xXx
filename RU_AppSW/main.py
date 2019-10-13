#!/usr/bin/env pybricks-micropython
from pybricks.tools import wait, StopWatch
import AppControl.appcontrol as appcontrol
import AppControl.sm_challange1 as sm_challenge1
import AppControl.sm_challenge2 as sm_challenge2
#import threading

#import Actions
import Sensing
<<<<<<< HEAD
#import Music
=======
import Music
import line_following
>>>>>>> f7fe0d8723e5bfcff277506316c1187c083b12a7

timestep_size = 10

# set up robot
watch = StopWatch()


# init components
#appcontrol.appcontrol_init()
#sm_challenge1.sm_challenge1_init()
#sm_challenge2.sm_challenge2_init()

counter = 0
reset_counter = 20

finished = False

while True:
    begin = watch.time() # total elapsed time in ms

    # actions inside here
    # TODO uncomment following line for the competition
    # Music.get_music().play_music()

    # update reflection_time function for line_following
    line_following.get_line_follower().update_reflection()
        
    #appcontrol.appcontrol_main()
    #sm_challenge1.sm_challenge1_main()
#    sm_challenge2.sm_challenge2_main()

    # actuate

    #Actions.get_actions().actuate()
    # filled_list = []
    # for i in range(0,1000):
    #     filled_list.append(Sensing.get_sensing().get_reflection())

    # with open("measurement.txt","w") as fout:
    #     for element in filled_list:
    #         fout.write(str(element) + "\n")
    #     finished = True

    counter += 1
    if counter == reset_counter:
        counter = 0
        print(Sensing.get_sensing().get_reflection())

    # end of actions
    elapsed = watch.time() - begin

    wait(max(timestep_size - elapsed, 0))
