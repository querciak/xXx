#!/usr/bin/env pybricks-micropython
from pybricks.tools import wait, StopWatch
import AppControl.appcontrol as appcontrol
import AppControl.sm_challange1 as sm_challange1

import Actions
import Sensing

timestep_size = 10

# set up robot
watch = StopWatch()


# init components
appcontrol.appcontrol_init()
sm_challange1.sm_challange1_init()

while True:
    begin = watch.time() # total elapsed time in ms

    # actions inside here

    appcontrol.appcontrol_main()
    sm_challange1.sm_challange1_main()

    # actuate

    Actions.get_actions().actuate()

    # end of actions
    elapsed = watch.time() - begin

    wait(max(timestep_size - elapsed, 0))
