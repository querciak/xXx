#!/usr/bin/env pybricks-micropython
from time import time

from pybricks.tools import wait

timestep_size = 10

while True:
    begin = time()

    # actions inside here


    # end of actions
    elapsed = begin - time()
    wait(min(timestep_size - int(elapsed), 0))
