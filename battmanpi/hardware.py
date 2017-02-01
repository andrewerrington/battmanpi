#!/usr/bin/env python3
"""BattMan Pi hardware control"""

#
# Copyright 2007 Capable Computing, Inc. (CCI)
# Copyright 2017 Andrew Errington
#
# This file is part of BattMan Pi.
#
# BattMan Pi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# BattMan Pi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with BattMan Pi.  If not, see <http://www.gnu.org/licenses/>.
#


import time

import RPi.GPIO as GPIO

import settings

D_TO_A_BITS = 12

class AtoDCalibration:
    def __init__(self):
        self.bitWeights = None
        self.lowMultiplier = None
        self.highMultiplier = None
        

GPIO.setmode(GPIO.BCM)


class battman:

    def __init__(self):

        self.D_TO_A_BITS = 12
        self.calib = AtoDCalibration()
        self.calib.bitWeights = settings.bitWeights
        
        self.calib.lowMultiplier=settings.DAClowMultiplier
        self.calib.highMultiplier=settings.DAChighMultiplier
        
        # Use BCM numbering for GPIO pins
        # These could be configurable, but probably the BattMan Pi PCB
        # will be used, so the GPIO pins are fixed.  DIY hardware can
        # use different GPIOs, but it's easy to edit the source here.
        
        # Output bits.
        self.DA_RESET = 18
        self.DA_INCREMENT = 17
        self.CONNECT_RELAY = 4
        self.CHARGE_RELAY = 27 
        
        #define RATE_MASK 0x0F
        # Rate mask is built bitwise
        self.RATE_MASK_0 = 22   # lsb
        self.RATE_MASK_1 = 23
        self.RATE_MASK_2 = 24
        self.RATE_MASK_3 = 25   # msb

        # Input bits.
        self.LOW_SENSE = 6
        self.HIGH_SENSE = 5

        GPIO.setup(self.DA_RESET, GPIO.OUT, initial=0)
        GPIO.setup(self.DA_INCREMENT, GPIO.OUT, initial=0)
        GPIO.setup(self.CONNECT_RELAY, GPIO.OUT, initial=0)
        GPIO.setup(self.CHARGE_RELAY, GPIO.OUT, initial=0)

        GPIO.setup(self.RATE_MASK_3, GPIO.OUT, initial=0)
        GPIO.setup(self.RATE_MASK_2, GPIO.OUT, initial=0)
        GPIO.setup(self.RATE_MASK_1, GPIO.OUT, initial=0)
        GPIO.setup(self.RATE_MASK_0, GPIO.OUT, initial=0)

        GPIO.setup(self.LOW_SENSE, GPIO.IN)     # No pullup.  Pullup is on PCB.
        GPIO.setup(self.HIGH_SENSE, GPIO.IN)    # No pullup.  Pullup is on PCB.


    def OpenBattMan(self):
        self.CloseBattMan()
        self.StopAndDisconnect()


    def CloseBattMan(self):
        self.StopAndDisconnect()


    def ChargeMode(self, rateCode):

        # Make sure current is off before doing anything.
        self.ZeroCurrent()

        # Turn on relays and give them 100ms to settle.
        GPIO.output(self.CONNECT_RELAY, 1)
        GPIO.output(self.CHARGE_RELAY, 1)

        time.sleep(0.1)

        self.NewChargeRate(rateCode)
        #GPIO.output(self.RATE_MASK_0, rateCode & 0x01)
        #GPIO.output(self.RATE_MASK_1, rateCode & 0x02)
        #GPIO.output(self.RATE_MASK_2, rateCode & 0x04)
        #GPIO.output(self.RATE_MASK_3, rateCode & 0x08)


    def NewChargeRate(self, rateCode):
        
        # Turn on current.
        #  controlByte += rateCode & RATE_MASK;
        # We can't write a nibble directly, but writing
        # the LSB first should minimise disturbance.
        # controlByte = (controlByte & ~RATE_MASK) | (rateCode & RATE_MASK);
        GPIO.output(self.RATE_MASK_0, rateCode & 0x01)
        GPIO.output(self.RATE_MASK_1, rateCode & 0x02)
        GPIO.output(self.RATE_MASK_2, rateCode & 0x04)
        GPIO.output(self.RATE_MASK_3, rateCode & 0x08)


    def DischargeMode(self, rateCode):
        #  Make sure current is off before doing anything.
        self.ZeroCurrent()

        # Turn on relays and give them 100ms to settle.
        GPIO.setoutput(self.CONNECT_RELAY, 1)
        
        time.sleep(0.1)

        # Turn on current.
        self.NewChargeRate(rateCode)

        # controlByte += rateCode & RATE_MASK;
        #GPIO.output(self.RATE_MASK_0, rateCode & 0x01)
        #GPIO.output(self.RATE_MASK_1, rateCode & 0x02)
        #GPIO.output(self.RATE_MASK_2, rateCode & 0x04)
        #GPIO.output(self.RATE_MASK_3, rateCode & 0x08)


    def StopAndDisconnect(self):
        # Make sure current is off before doing anything.
        self.ZeroCurrent()

        # Turn off relays and give them 100ms to settle.
        GPIO.output(self.CONNECT_RELAY, 0)
        GPIO.output(self.CHARGE_RELAY, 0)
        time.sleep(0.1)


    def ZeroCurrent(self):
        
        GPIO.output(self.RATE_MASK_0, 0)
        GPIO.output(self.RATE_MASK_1, 0)
        GPIO.output(self.RATE_MASK_2, 0)
        GPIO.output(self.RATE_MASK_3, 0)

        time.sleep(0.001)


    def bitsToVolts(self, count, weights):

        v = 0.0

        # Add up the weights corresponding to the 1-bits in count.
        for bit in range(D_TO_A_BITS):
            if (count & 1):
                v += weights[bit]
            count >>= 1

        return v


    def ReadVoltage(self, calib=None):

        if calib is None:
            calib = self.calib
    
        # Reset 12-bit D-to-A counter and wait 1ms.
        GPIO.output(self.DA_RESET, 1)
        time.sleep(0.001)
        GPIO.output(self.DA_RESET, 0)
        time.sleep(0.001);

        # Increment counter and monitor sense bits.
        lastVolts = 0.0
        lowCount = None
        highCount = None

        for count in range(4096):
            # Check if we've triggered the low-side sensor.
            if (lowCount is None and not GPIO.input(self.LOW_SENSE)):
                lowCount = count

            # Check if we've triggered the high-side sensor. If so, there's no
            # need to go on.
            if not GPIO.input(self.HIGH_SENSE):
                highCount = count
                break

            # Because of less than perfect R-2R ladder resistors, the voltage for
            # count N+1 can actually be less than that for count N. So instead of
            # just incrementing once, we increment until we have a voltage that's
            # higher than the previous voltage.
            while (self.bitsToVolts(count,calib.bitWeights) <= lastVolts):
                GPIO.output(self.DA_INCREMENT, 1)
                time.sleep(0.001)
                GPIO.output(self.DA_INCREMENT, 1)
                time.sleep(0.001)
                if (++count == 4096):
                    break


        # If we failed to trigger one or both sensors, we don't have a valid
        # reading. Return None to indicate this.
        if (lowCount is None or highCount is None):
            return None

        return (self.bitsToVolts(highCount,calib.bitWeights) * calib.highMultiplier
            - self.bitsToVolts(lowCount,calib.bitWeights) * calib.lowMultiplier)


    def SetAll(self, rateCode, charge, connect_):

        # First set current to zero and wait 1ms.
        self.ZeroCurrent()

        # Next change state of relays as requested and wait 100ms.
        GPIO.output(self.CONNECT_RELAY, bool(connect_))
        GPIO.output(self.CHARGE_RELAY, bool(charge))

        time.sleep(0.1)

        # Finally turn on current at desired rate.
        self.NewChargeRate(rateCode)
        #GPIO.output(self.RATE_MASK_0, rateCode & 0x01)
        #GPIO.output(self.RATE_MASK_1, rateCode & 0x02)
        #GPIO.output(self.RATE_MASK_2, rateCode & 0x04)
        #GPIO.output(self.RATE_MASK_3, rateCode & 0x08)


    def SetCount(self, count):

        # Reset 12-bit D-to-A counter and wait 1ms.
        GPIO.output(self.DA_RESET, 1)
        time.sleep(0.001)
        GPIO.output(self.DA_RESET, 0)
        time.sleep(0.001)

        # Increment counter specified number of times.
        for i in range(count):
            GPIO.output(self.DA_INCREMENT, 1)
            time.sleep(0.001)
            GPIO.output(self.DA_INCREMENT, 0)
            time.sleep(0.001)