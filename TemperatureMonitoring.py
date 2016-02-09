#!/usr/bin/python3

import numpy
from math import floor, sqrt, exp, ceil, log


# variables
T = 253.15
T0 = 25.0
ABSOLUTE0 = 273.15
T0 = ABSOLUTE0 + 25.0


R = 6.06        # the current resistance
R0 = 10.0       # zero point of thermistor calibration curve
RBridge = 6.04   # The fixed resistor in the half bridge
beta = 3492.0

temperatures = []
resistances = []

index = 1

def calculateR(T):
    global R
    temp = exp(beta*(1/T - 1/T0))
    R0 = 10.0
    R = R0 * temp
    print ("R = %.2f    T = %.2f"  % (R, T))

def calculateT(R):
    global T
    temp = 1.0/(T0) + (1.0/beta) * log(R/R0)
    T = 1/temp
    Fahr = (T - ABSOLUTE0)*9.0/5.0 + 32
    print ("T = %.2f   R = %.2f Tc = %.2f, Fahr = %.2f" %(T,R,T - ABSOLUTE0, Fahr))

def convertRawDataToR(RawData):
    global R
    VOverV0 = RawData/10240.0
    denominator = 1.0 - VOverV0
    R = RBridge * VOverV0/denominator
    print ("RawData = " +str(RawData)+ " R = %.2f " %(R))


for index in range (0,10):
    T = index * 5.0
    calculateR(T + ABSOLUTE0)


for index in range (0,10):
    R = 5.0 + index + .04
    calculateT(R)


for index in range (0,10):
    RawData = 5120 + 25 * (5 - index)
    convertRawDataToR(RawData)
    calculateT(R)

