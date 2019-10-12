#!/usr/bin/env pybricks-micropython
from pybricks.tools import wait, StopWatch
import AppControl.appcontrol as appcontrol
import AppControl.sm_challange1 as sm_challenge1
#import threading

import Actions
import Sensing
import Music

timestep_size = 10

# set up robot
watch = StopWatch()


# init components
appcontrol.appcontrol_init()
sm_challenge1.sm_challenge1_init()

while True:
    begin = watch.time() # total elapsed time in ms

    # actions inside here
    # play next note if needed
    # TODO uncomment following line for the competition
    # Music.get_music().play_music()
        
    appcontrol.appcontrol_main()
    sm_challenge1.sm_challenge1_main()

    # actuate

    Actions.get_actions().actuate()

    # end of actions
    elapsed = watch.time() - begin

    wait(max(timestep_size - elapsed, 0))
