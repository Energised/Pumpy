#!/usr/bin/python3
# Pumpy.py
#
# Class encapsulating setup and operation for operating the pump
# including properties and methods
#
# For easy operation of the pump within a GUI

"""
DESCRIPTION OF PIN OUTS

DIR - 20 : Set direction clockwise/counter-clockwise
STEP - 21 : Start/Stop movement of Stepper Motor

MS_MODE - (5,6,13) : 3 pins control microstepping level

MS_RESOLUTION - Dictionary of signals, applied to MS_MODE to set microstepping level
MS_SIZE_STEPS_V1 - <syringe-size(mL)>:{<ms-value>:<steps>}
                 - Given a syringe size and microstep value, return number of
                   steps to infuse the full syringe
MS_SIZE_STEPS_V2 - As above, but for Syringe Pump v2


INFUSE - 1 : CW movement
WITHDRAW - 0 : CCW movement

FRONT_SW - 16 : Limit Switch on Syringe Holder side (Labeled as 1)
BACK_SW - 19 : Limit Switch on Motor End - Variable distance (Labeled as 2)

SETTING UP AS A QOBJECT FOR PYQT MULTI-THREADING

-

"""

from time import sleep
import RPi.GPIO as GPIO

from PyQt5.QtCore import QObject, QThread, pyqtSignal

class Pumpy(QObject):

    INFUSE = 1 # CW
    WITHDRAW = 0 # CCW

    MS_RESOLUTION = {"1": (0,0,0),
                     "1/2": (1,0,0),
                     "1/4": (0,1,0),
                     "1/8": (1,1,0),
                     "1/16": (1,1,1)}

    MS_SIZE_STEPS_V1 = {20:{"1":17500, "1/2":35000, "1/4":70000, "1/8":140000, "1/16":280000},
                        60:{"1":27250, "1/2":54500, "1/4":109000, "1/8":218000, "1/16":436000}}

    MS_SIZE_STEPS_V2 = {20:{"1":7000, "1/2":14000, "1/4":28000, "1/8":56000, "1/16":112000},
                        60:{"1":10900, "1/2":21800, "1/4":43600, "1/8":87200, "1/16":174400}}

    # thread signal objects
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, dir, step, ms1, ms2, ms3, f_switch, b_switch, spr=200):
        super().__init__()
        self.direction_pin = dir
        self.step_pin = step
        #self.microstep_1 = ms1
        #self.microstep_2 = ms2
        #self.microstep_3 = ms3
        self.mode = (ms1,ms2,ms3)
        self.spr = spr
        self.f_switch = f_switch
        self.b_switch = b_switch
        self.setup()

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.mode, GPIO.OUT)
        GPIO.setup(self.f_switch, GPIO.IN)
        GPIO.setup(self.b_switch, GPIO.IN)

    # ms -> string ("1","1/2","1/4","1/8","1/16")
    def set_microstep(self, ms):
        GPIO.output(self.mode, self.MS_RESOLUTION[ms])

    # dir -> variable (INFUSE, WITHDRAW)
    def set_direction(self, dir):
        GPIO.output(self.direction_pin, dir)

    # dir -> variable (INFUSE, WITHDRAW)
    # as a stop condition, will use boolean
    # usign a while loop means no escaping
    def continuous(self, dir, ms):
        self.set_direction(dir)
        self.set_microstep(ms)

        if(dir == 0):
            check = self.b_switch
        else:
            check = self.f_switch

        progress_counter = 0
        while(GPIO.input(check)):
            GPIO.output(self.step_pin, GPIO.HIGH)
            sleep(0.005/4)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(0.005/4)
            # increment progress_counter and emit value to progress signal
            progress_counter += 1
            self.progress.emit(progress_counter)
        self.finished.emit()


    def stop(self):
        GPIO.output(self.step_pin, GPIO.LOW)
        Pumpy.END_CONT = True

    # infuse_time (int) (seconds)
    # syringe_size (int) (mL)
    # ms (string) ("1","1/2","1/4","1/8","1/16")
    def calculate_delay(self, infuse_time, syringe_size, ms):
        total_steps = self.MS_SIZE_STEPS_V2[syringe_size][ms]
        delay = infuse_time/total_steps
        return delay

    # dir -> variable (INFUSE, WITHDRAW)
    # infuse_time (int) (seconds)
    # syringe_size (int) (mL)
    # ms (string) ("1","1/2","1/4","1/8","1/16")
    def pump(self, dir, infuse_time, syringe_size, ms):
        self.set_direction(dir)
        self.set_microstep(ms)
        delay = self.calculate_delay(infuse_time, syringe_size, ms)
        total_steps = self.MS_SIZE_STEPS_V2[syringe_size][ms]
        for i in range(total_steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            sleep(delay/2)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(delay/2)
            # emit progress value
            self.progress.emit(i)
        # tell thread we've finished
        self.finished.emit()

if __name__ == "__main__":
    pump = Pumpy(20,21,5,6,13,16,19)
    #pump.setup()
    # infuse, in 60s, 20mL, with microstepping level 1
    #pump.pump(INFUSE,60,20,"1")
    pump.continuous(Pumpy.WITHDRAW)
    #sleep(5)
    #pump.stop()
