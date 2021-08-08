#!/usr/bin/python3
# pump_testing.py
#
# Set of functions for basic operations including
# - Single revolution with direction choice
# - Microstepping for each mode
# - Full length movement from end to end
# - Proper delay calculation (derivation will be availiable on GitLab)

from time import sleep
import RPi.GPIO as GPIO

DIR = 20
STEP = 21
#SPR = 200

CW = 1 # infuse
CCW = 0 # withdraw

MODE = (5,6,13)

FRONT_SW = 16
BACK_SW = 19

RESOLUTION = {'1':(0,0,0),
              '1/2':(1,0,0),
              '1/4':(0,1,0),
              '1/8':(1,1,0),
              '1/16':(1,1,1)}

STEPS = {'1':200,
         '1/2':400,
         '1/4':800,
         '1/8':1600,
         '1/16':3200}

DELAY = {'1':0.005,
         '1/2':0.005/2,
         '1/4':0.005/4,
         '1/8':0.005/8,
         '1/16':0.005/16}

MS = ['1','1/2','1/4','1/8','1/16']

def setup():
    GPIO.setwarnings(False) # DIR and STEP pins being reinitialised, so warnings show
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.setup(MODE, GPIO.OUT)
    GPIO.setup(FRONT_SW, GPIO.IN)
    GPIO.setup(BACK_SW, GPIO.IN)


# delay between .001 and .005 for full step (200) seems good

def revolution(dir, res):
    GPIO.output(DIR, dir)
    GPIO.output(MODE, RESOLUTION[res])
    for _ in range(STEPS[res]):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(DELAY[res])
        GPIO.output(STEP, GPIO.LOW)
        sleep(DELAY[res])
    print("1 rev completed")

# microstep("1/2")
# would recalculate steps and delay, put into revolution

def microstep(dir, res):
    GPIO.output(MODE, RESOLUTION[res])
    revolution(dir, res)

def all_microsteps(dir):
    for key in MS:
        revolution(dir, key)
        sleep(0.5)

# testing the above functions
def test_1():
    for _ in range(50):
        microstep(CW,"1")
    all_microsteps(CW)
    # 1/4 - minimal vibration, lowest steps
    for _ in range(30):
        microstep(CW,"1/4")

# new operation functions, above is fine for tests but need something more suitable

# since this will be calculated by the program, will give its own function for now
# take ms as a string
# using the RESOLUTION dictionary to define pin outs
def set_microstep(ms):
    GPIO.output(MODE, RESOLUTION[ms])

# will take either variable: CW or CCW
# CW -> infuse
# CCW -> withdraw
def set_direction(dir):
    GPIO.output(DIR, dir)

# some extra functions i need for ease of testing

def withdraw_continuous():
    set_direction(CCW)
    set_microstep('1')
    while 1:
        GPIO.output(STEP, GPIO.HIGH)
        sleep(0.005/4) # smooth delay to reduce vibration
        GPIO.output(STEP, GPIO.LOW)
        sleep(0.005/4)

def infuse_continuous():
    set_direction(CW)
    set_microstep('1')
    while 1:
        GPIO.output(STEP, GPIO.HIGH)
        sleep(0.005/4)
        GPIO.output(STEP, GPIO.LOW)
        sleep(0.005/4)

# testing flow rate maths from project book
# taking into account syringe size, conversion rates, microstepping

# steps to infuse the entire syringe
# more efficient to pre-calculate these values
# BASED ON BD Plastipak Syringes

# 20ml
ms_to_steps_20 = {'1':17500, '1/2':35000, '1/4':70000, '1/8':140000, '1/16':280000}

# 60ml
ms_to_steps_60 = {'1':27250, '1/2':54500, '1/4':109000, '1/8':218000, '1/16':436000}

# combine these

ms_size_steps = {20:{'1':17500, '1/2':35000, '1/4':70000, '1/8':140000, '1/16':280000},
                 60:{'1':27250, '1/2':54500, '1/4':109000, '1/8':218000, '1/16':436000}}


# now the above for syringe pump v2

v2_ms_size_steps = {20:{'1':7000, '1/2':14000, '1/4':28000, '1/8':56000, '1/16':112000},
                    60:{'1':10900, '1/2':21800, '1/4':43600, '1/8':87200, '1/16':174400}}

# given microstepping value, time to infuse (seconds) and syringe size
# calculate the delay per step final delay will be halved, to delay
# before and after pin out signal
def calculate_delay(ms, infuse_time, syringe_size):
    if(syringe_size == 20):
        total_steps = ms_to_steps_20[ms]
    elif(syringe_size == 60):
        total_steps = ms_to_steps_60[ms]
    else:
        print("Invalid syringe size")
    delay = infuse_time/total_steps
    return delay


# dir -> variable : Infuse/withdraw the syringe
# ms -> String : Chosen microstepping value
# infuse_time -> int (seconds) : how long it should take
# syringe_size -> int : in mL,
def pump(dir, ms, infuse_time, syringe_size):
    # setup dir and ms
    set_direction(dir)
    set_microstep(ms)
    delay = calculate_delay(ms, infuse_time, syringe_size)
    if(syringe_size == 20):
        total_steps = ms_to_steps_20[ms]
    elif(syringe_size == 60):
        total_steps = ms_to_steps_60[ms]
    for _ in range(total_steps):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay/2)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay/2)
    print("operation complete")

# test the calculate delay function in operation with pump
def test_2():
    # infuse 20ml in 1 minute, ms=1
    pump(CW, '1/2', 60, 20)
    print("test complete")

# limit switch testing

def infuse_continuous_switch():
    set_direction(CW)
    set_microstep('1')
    # while switch isnt pressed
    while(GPIO.input(FRONT_SW)):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(0.005/4)
        GPIO.output(STEP, GPIO.LOW)
        sleep(0.005/4)

def withdraw_continuous_switch():
    set_direction(CCW)
    set_microstep('1')
    while(GPIO.input(BACK_SW)):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(0.005/4)
        GPIO.output(STEP, GPIO.LOW)
        sleep(0.005/4)

if __name__ == "__main__":
    setup()
    #infuse_continuous()
    #test_1()
    #withdraw_continuous()
    #test_2()
    withdraw_continuous_switch()
    #infuse_continuous_switch()
