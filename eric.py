from ast import Global
import time
import numpy as np
from gpiozero import MCP3008
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.OUT)
#designates what pins to gather data from
chtemp = MCP3008(channel=0, clock_pin=11, mosi_pin=10,miso_pin=9, select_pin=8)
#setting parameters
tsample = 0.5 #how often to get data
tdisp = 1 #how often to display data
tstop = 20 #how long data should be gathered
vref = 3.3 #voltage used
ktemp = 23 #adjusts the temperature
tprev = 0
tcurr = 0
tstart = time.perf_counter() #starts a timer

def temps():
    
    global tsample, tdisp, tstop, vref, ktemp, tprev, tcurr, tstart #This code operates the temperature sensor and outputs the temperature data
    tcurr = time.perf_counter() - tstart #the current time is set to the timer
    valuecurr = chtemp.value #puts the temperature sensor value into a new variable
    tempcurr = vref*ktemp*valuecurr*(9/5)+32 #calculates the temperature
    return int(np.round(tempcurr)) #returns the temperature vlaue
    tprev = tcurr #updates the current amount of time passed
       
#GPIO SETUP

GPIO.setup(5, GPIO.IN)
def callback():
    return GPIO.input(5) # will return input of soil moisture sensor
