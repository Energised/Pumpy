# Pump Testing Suite

The files here contain functions that test the operation of the stepper motors,
limit switches and the lookup tables I calculated to define the number of steps
it takes to infuse a set size BD PlastiPak syringe at a given micro-stepping rate.

---
<b> NOTE: </b> These functions are written in Python 3.x.x and require the `RPi.GPIO` library to run.

## `pump-test.py`

### Tests for Syringe Pump v1

#### Variables

```
DIR = 20         # sets revolution direction
STEP = 21        # activates the stepper motor
CW = 1           # identifier for clockwise
CCw = 0          # identifier for anticlockwise
MODE = (5,6,13)  # setting micro-step resolution

FRONT_SW = 16    # detect front limit switch is pressed
BACK_SW = 19     # detect back limit switch is pressed

RESOLUTION = {'1':(0,0,0),  # signal map for micro-step resolutions
            '1/2':(1,0,0),
            '1/4':(0,1,0),
            '1/8':(1,1,0),
            '1/16':(1,1,1)}

STEPS = {'1':200,           # steps per revolution for each resolution level
         '1/2':400,
         '1/4':800,
         '1/8':1600,
         '1/16':3200}

DELAY = {'1':0.003,         # map of delay times for testing purposes
         '1/2':0.005/4,
         '1/4':0.005/4,
         '1/8':0.005/4,
         '1/16':0.005/4}

MS = ['1','1/2','1/4','1/8','1/16'] # list of micro-step resolutions

```
#### Methods
---
`def setup()`

Warnings are disabled due to the `STEP` and `DIR` pins being reinitialised.

Then we setup our output pins: `STEP`, `DIR` and `MODE`.

Finally we setup our input pins: `FRONT_SW` and `BACK_SW`.

---
`def revolution(dir, res)`

Given a direction `dir={0|1}` and a micro-step resolution `res={'1'|'1/2'|'1/4'|'1/8'|'1/16'}` it will
complete a single revolution with the number of steps required by the given resolution string.

---
`def all_microsteps(dir)`

For every possible micro-step resolution defined in the list `MS` perform one revolution of
the stepper motor.

---
`def test_1()`

Runs 50 revolutions with a micro-step resolution of `'1'`.

Then runs 30 revolutions with a micro-step resolution of `'1/4'`.

---
`def set_microstep(ms)`

Sets the output pins in `MODE` to the given resolution `ms` as a string mapped in the dictionary
`RESOLUTION`.

---
`def set_direction(dir)`

Sets the `DIR` pin to the identifier passed as `dir={CW|CCW}`.

---
`def withdraw_continuous()`

Sets direction to `CCW` and micro-step resolution to `'1'` and runs the stepper motor
indefinitely.

---
`def infuse_continuous()`

Sets direction to `CW` and micro-step resolution to `'1'` and runs the stepper motor
indefinitely.

### Tests for Syringe Pump v2

#### Variables

```
# micro-step resolution -> step : maps for syringe pump v1

# steps for infusing/withdrawing the entire 20ml syringe
ms_to_steps_20 = {'1':17500, '1/2':35000, '1/4':70000, '1/8':140000, '1/16':280000}

# steps for infusing/withdrawing the entire 60ml syringe
ms_to_steps_60 = {'1':27250, '1/2':54500, '1/4':109000, '1/8':218000, '1/16':436000}

# combine the above dictionaries into one dictionary

ms_size_steps = {20:{'1':17500, '1/2':35000, '1/4':70000, '1/8':140000, '1/16':280000},
                 60:{'1':27250, '1/2':54500, '1/4':109000, '1/8':218000, '1/16':436000}}


# micro-step resolution -> step : maps for syringe pump v2

v2_ms_size_steps = {20:{'1':7000, '1/2':14000, '1/4':28000, '1/8':56000, '1/16':112000},
                    60:{'1':10900, '1/2':21800, '1/4':43600, '1/8':87200, '1/16':174400}}
```

#### Methods
---
`def calculate_delay(ms, infuse_time, syringe_size)`

Using the `ms_to_steps_20` and `ms_to_steps_60` dictionaries, based on the given `syringe_size`
we get the total number of steps to infuse the syringe at the given `ms`.

Then we calculate the delay with `delay = total_steps/infuse_time` and return it.

---
`def pump(dir, ms, infuse_time, syringe_size)`

Uses `set_microstep(ms)` and `set_direction(dir)` to initialise the outputs.

Then calculated the delay using `calculate_delay(ms, infuse_time, syringe_size)`.

Finally it gets the total number of steps required using `syringe_size` and runs the pump, delaying
each step using the delay value calculated.

---
`def test_2()`

Runs the function `pump(CW, '1/2', 60, 20)`

---
`def infuse_continuous_switch()`

Uses `set_microstep('1')` and `set_direction(CW)` to initialise the outputs.

Then it starts a loop to operate the pump until a signal is detected on the front limit switch
using `GPIO.input(FRONT_SW)`

---
`def withdraw_continuous_switch()`

Uses `set_microstep('1')` and `set_direction(CCW)` to initialise the outputs.

Then it starts a loop to operate the pump until a signal is detected on the back limit switch
using `GPIO.input(BACK_SW)`.

This switch will be activated by a stopper that sits on one of the rails of the pump.

---

## `Pumpy.py`

Initial version of the `Pumpy` class that encapsulates all the behaviour of the functions written
in `pump-test.py` into a single object that can be easily instantiated and run.

The dictionaries `MS_SIZE_STEPS_V1` and `MS_SIZE_STEPS_V2` are lookup tables calculated using the
formulea described [here](./pump-maths.md).

### Class Variables

```
INFUSE = 1                          # CW
WITHDRAW = 0                        # CCW

MS_RESOLUTION = {"1": (0,0,0),      # Micro-stepping resolution mapping
               "1/2": (1,0,0),
               "1/4": (0,1,0),
               "1/8": (1,1,0),
               "1/16": (1,1,1)}

# lookup table for number of steps required to fully infuse one of 2 sizes of syringe
# at a chosen micro-step resolution, with a table for each pump version

MS_SIZE_STEPS_V1 = {20:{"1":17500, "1/2":35000, "1/4":70000, "1/8":140000, "1/16":280000},
                    60:{"1":27250, "1/2":54500, "1/4":109000, "1/8":218000, "1/16":436000}}

MS_SIZE_STEPS_V2 = {20:{'1':7000, '1/2':14000, '1/4':28000, '1/8':56000, '1/16':112000},
                    60:{'1':10900, '1/2':21800, '1/4':43600, '1/8':87200, '1/16':174400}}

# DEFINED IN CONSTRUCTOR

self.direction_pin           # output pin for setting direction
self.step_pin                # output pin for moving motor
self.mode = (ms1,ms2,ms3)    # output pin for setting micro-step resolution
self.spr = spr               # default steps per revolution for the motor
self.f_switch = f_switch     # input pin for front limit switch
self.b_switch = b_switch     # input pin for back limit switch

```
---
`def __init__(self, dir, step, ms1, ms2, ms3, f_switch, b_switch, spr=200)`

Constructor for Pumpy class with input and output pin parameters and a default steps per revolution
value - the NEMA 17 motor in use has a default steps per revolution of 200.

---
`def setup(self)`

Basic GPIO setup functions to disable warnings (direction and step pins get reinitialised on each operation),
set the pin description mode to BCM (Broadcom) and setting the pin input and outputs.

---
`def set_microstep(self, ms)`

Sets the pins of `self.mode` to the micro-step resolution given by `ms` - the key in the dictionary
`MS_RESOLUTION`.

---
`def set_direction(self, dir)`

Sets the `self.direction_pin` output pin to an integer variable, either `INFUSE` or `WITHDRAW`.
Their values as integers are 1 and 0 respectively.

---
`def continuous(self, dir)`

Sets the `self.direction_pin` output pin to `dir`, sets the micro-step resolution to `'1'`, sets up
which limit switch will be activated using `dir` and runs the motor until the limit switch input is
activated

---
`def stop(self)`

Sets the `self.step_pin` output to `GPIO.LOW` - it is used to stop any operation of the pump.

---
`def calculate_delay(self, infuse_time, syringe_size, ms)`

Based on the given `syringe_size` and `ms` it finds the total number of steps required to infuse
the syringe as `self.MS_SIZE_STEPS_V(1/2)[syringe_size][ms]`. This value is divided by `infuse_time` to
give the delay required per step

---
`def pump(self, dir, infuse_time, syringe_size, ms)`

Uses `set_direction(self, dir)` and `set_microstep(self, ms)` to set the correct outputs and calculates the
delay per step using `calculate_delay(self, infusion_time, syringe_size, ms)`.

Finally it gets the total number of steps from `self.MS_SIZE_STEPS_V(1/2)[syringe_size][ms]` and runs the motor
for that many steps, delaying between each pin output call.
