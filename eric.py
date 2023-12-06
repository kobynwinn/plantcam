from ast import Global
import time
import numpy as np
from gpiozero import MCP3008
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.OUT)
#designates the pins
chtemp = MCP3008(channel=0, clock_pin=11, mosi_pin=10,miso_pin=9, select_pin=8)

tsample = 0.5 #how often to get data
tdisp = 1 #how often to display data
tstop = 20 #how long data should be gathered
vref = 3.3 #voltage used
ktemp = 23 #

tprev = 0
tcurr = 0
tstart = time.perf_counter()

def temps():
    
    global tsample, tdisp, tstop, vref, ktemp, tprev, tcurr, tstart
    tcurr = time.perf_counter() - tstart
    valuecurr = chtemp.value
    tempcurr = vref*ktemp*valuecurr*(9/5)+32
    return int(np.round(tempcurr))
    tprev = tcurr
       
#GPIO SETUP

GPIO.setup(5, GPIO.IN)
def callback():
    return GPIO.input(5)
