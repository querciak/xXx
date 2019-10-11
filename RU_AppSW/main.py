#!/usr/bin/env pybricks-micropython
from time import time

from pybricks.tools import wait
import AppControl.appcontrol as appcontrol
import AppControl.sm_challange1 as sm_challange1


timestep_size = 10

# init
appcontrol.appcontrol_init()
sm_challange1.sm_challange1_init()

while True:
    begin = time()

    # actions inside here
    appcontrol.appcontrol_main()
    sm_challange1.sm_challange1_main()

    # end of actions
    elapsed = begin - time()
    wait(max(timestep_size - int(elapsed), 0))
