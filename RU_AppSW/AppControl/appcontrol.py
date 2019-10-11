# this file is supposed to alter between the state machines of the different challanges
# main application control, selects components to execute

CHALLANGES = ['first','second','third','fourth','fifth','sixth','fight']

# init
def appcontrol_init():
    global PERFORMED_CHALLANGE
    PERFORMED_CHALLANGE = CHALLANGES[0]

# dummy functions
def isFirstChallangeFinished():
    return False

def isSecondChallangeFinished():
    return False

def isThirdChallangeFinished():
    return False


def appcontrol_main():
    global PERFORMED_CHALLANGE
    
    if PERFORMED_CHALLANGE[0]:
        # transition to challange 2
        if isFirstChallangeFinished() == True:
            PERFORMED_CHALLANGE = CHALLANGES[1] # transition to challange 2
        if isSecondChallangeFinished() == True:
            PERFORMED_CHALLANGE = CHALLANGES[2] # transition to challange 3
        if isThirdChallangeFinished() == True:
            PERFORMED_CHALLANGE = CHALLANGES[3] # transition to challange 4
        # etc..
        
    
