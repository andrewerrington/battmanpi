#!/usr/bin/env python3
"""BattMan Pi functions"""

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
import graph

import settings

NUM_READINGS = 20
LOG_FILE = "battmanpi.csv"

class func:

    def __init__(self, parent, bm):
        self.bm = bm
        self.parent = parent

        
    def allocateGraph(self, yMin, yMax):
        #del(self.canvas.graph)
        
        self.canvas.graph = graph.graph(yMin, yMax, self.canvas)


    def takeReading(self, starting=False):
        
        if starting:
            self.average = 0.0
        else:
            self.average = self.average *((NUM_READINGS - 1.0) / NUM_READINGS)\
                + self.bm.ReadVoltage() /NUM_READINGS
        
        return self.average


    def writeToLog(self, oper, cycle, rate, capacity, energy, resistance, formSettings):

        newFile = False
        try:
            fp = open(LOG_FILE, "r")
        except FileNotFoundError:
            newFile = True

        fp = open(LOG_FILE,"a")
        
        #if( fp != NULL ) { FIXME: Check file was opened successfully
        if newFile:
            fp.write('"Date/Time","Mode","Cycle","Of","Type","Rated","Cells","mA","mAh","mWh","ohms","V/Cell"\n')

        fp.write('"%s","%s",%d,%d,"%s",%d,%d,%1.1f,%1.1f,%1.1f,%1.4f,%1.4f\n'%
                (time.strftime("%Y-%m-%d %H:%M:%S"), oper, cycle,
                formSettings['maximumCycles'] if cycle else 0,
                formSettings['cellType'], formSettings['capacity'],
                formSettings['numberOfCells'], rate*1000,
                capacity, energy, resistance, 0.0 if capacity==0 else
                energy/(capacity*formSettings['numberOfCells'])))
        fp.close()


    def PerformDischarge(self, cycle, formSettings):

        if (formSettings['cellType'] == "NiCd"):
            vMin = settings.niCdVMin * formSettings['numberOfCells']
        elif (formSettings['cellType'] == "NiMH"):
            vMin = settings.niMHVMin * formSettings['numberOfCells']
        elif (formSettings['cellType'] == "LiPo"):
            vMin = settings.liPoVMin * formSettings['numberOfCells']
        elif (formSettings['cellType'] == "LiNP"):
            vMin = settings.liNPVMin * formSettings['numberOfCells']
        elif (formSettings['cellType'] == "PbAcid"):
            vMin = settings.pbAcidVMin * formSettings['numberOfCells']
        else:
            #MessageDlg(AnsiString("Unrecognized cell type: ") + StartForm->cellType,
            #           mtError,TMsgDlgButtons() << mbOK,0);
            return None

        dischargeRate = settings.dischargeRates[formSettings['dischargeRateCode']]
    
        #if( graph == NULL )
        #    allocateGraph(0,0);
        dischargeImpedance = self.CheckImpedance('IMPEDANCE_DISCHARGE', formSettings)

        # Measured cut-off voltage is minimum no-load voltage minus the drop we
        # get due to impedance.
        vCutOff = vMin - dischargeImpedance * dischargeRate

        # Take an initial reading to know where to start the graph.
        v = self.takeReading(True)
        self.allocateGraph(vCutOff if v > vCutOff else v-0.05, v+0.05)

        # Write discharge information on top line.
        buf = "Discharge"
        if (cycle):
            buf +=" %d of %d"%(cycle,formSettings['maximumCycles'])
        buf += "  Battery: %d %s"%\
            (formSettings['numberOfCells'],formSettings['cellType'])
        buf += "  Rate: %1.0f mA"%(dischargeRate*1000)
        buf += "  VMin: %1.2f V"%vCutOff
        buf += "  Resistance: %1.4f ohms"%dischargeImpedance
        self.canvas.graph.WriteTopLine(buf)

        energy = 0.0    # Watt-seconds
        capacityDischarged = 0.0    # Amp-seconds

        start = time.time()
        lastTime = start
    
        self.bm.DischargeMode(formSettings['dischargeRateCode'])

        done = False
    
        while not done:
            now = time.time()
            elapsed = now - start
            v = self.takeReading()

            if (now > lastTime):
                capacityDischarged += dischargeRate
                energy += dischargeRate * v
                lastTime = now
        
            if (v < vCutOff):
                done = True

            self.canvas.graph.WriteBottomLine(
                "Time: %d:%02d:%02d  Voltage: %1.2f V  Discharge: %1.0f mAh (%1.0f mWh)"%
                (elapsed/3600, (elapsed%3600)/60, elapsed%60, v,
                capacityDischarged/3.6,energy/3.6))
            self.canvas.graph.AddPoint(elapsed, v)

            self.canvas.update()

            if settings.stoprequested:
                self.bm.StopAndDisconnect()
                return None
        

        self.bm.StopAndDisconnect()
        self.writeToLog("DIS", cycle, dischargeRate, capacityDischarged/3.6,
            energy/3.6, dischargeImpedance, formSettings)

        return elapsed
    
    
    def PerformCharge(self, cycle, startAt, formSettings):
        
        deltaV = 1.0
        vMax = 100.0

        if (formSettings['cellType'] == "NiCd"):
            deltaV = settings.niCdDeltaV
        elif (formSettings['cellType'] == "NiMH"):
            deltaV = settings.niMHDeltaV
        elif (formSettings['cellType'] == "LiPo"):
            vMax = settings.liPoVMax * formSettings['numberOfCells']
        elif (formSettings['cellType'] == "LiNP"):
            vMax = settings.liNPVMax * formSettings['numberOfCells']
        elif (formSettings['cellType'] == "PbAcid"):
            vMax = settings.pbAcidVMax * formSettings['numberOfCells']
        else:
            #MessageDlg(AnsiString("Unrecognized cell type: ") + StartForm->cellType,
            #           mtError,TMsgDlgButtons() << mbOK,0);
            return None

        chargeRateCode = formSettings['chargeRateCode']
        chargeRate = settings.dischargeRates[chargeRateCode]
        origChargeRate = chargeRate

        timeLimit = (formSettings['capacity'] * 3.6 / chargeRate)

        if (deltaV < 1.0):
            timeLimit *= 1.25
        else:
            timeLimit *= 1.75

        #if( graph == NULL )
        #    allocateGraph(0,0);
        chargeImpedance = self.CheckImpedance('IMPEDANCE_CHARGE', formSettings)

        v = self.takeReading(True)

        if (cycle == 0):
            self.allocateGraph(v-0.05, v+0.05)

        buf = "Charge"
        if (cycle):
            buf +=" %d of %d"%(cycle,formSettings['maximumCycles'])
        buf += "  Battery: %d %s"%\
            (formSettings['numberOfCells'],formSettings['cellType'])
        buf += "  Rate: %1.0f mA"%(chargeRate*1000)
        if (deltaV < 1.0):
            buf += "  Delta: %1.2f%%"%(deltaV*100)
        if (vMax < 100.0):
            buf += "  VMax: %1.2f V"%vMax
            
        buf += "  TLimit: %2d:%02d:%02d"%\
            (timeLimit/3600,(timeLimit%3600)/60,timeLimit%60)
        buf += "  Resistance: %1.4f ohms"%chargeImpedance
        self.canvas.graph.WriteTopLine(buf)

        if (cycle):
            dischargedCapacity = "/%1.0f mAh"%\
                (startAt*settings.dischargeRates[formSettings['dischargeRateCode']]/3.6)
        else:
            dischargedCapacity = ''

        maxVoltageSeen = 0.0
        energy = 0.0    # Watt-seconds
        capacityCharged = 0.0   # Amp-seconds

        start = time.time()
        lastTime = start
        #, elapsed;
        lastTimeDeltaWasSmall = start

        self.bm.ChargeMode(chargeRateCode)

        done = False

        while not done:
            now = time.time()
            elapsed = now - start
            v = self.takeReading()

            if (now > lastTime):
                capacityCharged += chargeRate
                energy += chargeRate * v
                lastTime = now

            #double delta
            if (elapsed > timeLimit):
                done = True

            elif (v > vMax):
                chargeRateCode -= 1
                self.bm.NewChargeRate(chargeRateCode)
                chargeRate = settings.chargeRates[chargeRateCode]
                if (chargeRateCode == 0):
                    done = True
                else:
                    time.sleep(0.1)
                    self.takeReading(True)

            elif (elapsed > 60):
                if (v > maxVoltageSeen):
                    maxVoltageSeen = v

                if (maxVoltageSeen == 0.0):
                    delta = 0.0
                else:
                    delta = (maxVoltageSeen - v) / maxVoltageSeen

                if (delta < deltaV):
                    lastTimeDeltaWasSmall = now

                if (now - lastTimeDeltaWasSmall > Settings.deltaVDuration):
                    done = True

            else:
                delta = 0
                lastTimeDeltaWasSmall = now

            buf = "Time: %d:%02d:%02d  Voltage: %1.2f V  Charge: %1.0f mAh%s (%1.0f mWh)"%\
                (elapsed/3600, (elapsed%3600)/60, elapsed%60, v,
                capacityCharged/3.6, dischargedCapacity, energy/3.6)
            if (deltaV < 1.0):
                buf += "  Delta: %1.2f%% (%d s)"%(delta*100, now-lastTimeDeltaWasSmall)
            
            self.canvas.graph.WriteBottomLine(buf)
            self.canvas.graph.AddPoint(elapsed+startAt, v)

            self.canvas.update()
            
            if settings.stoprequested:
                self.bm.StopAndDisconnect()
                return None
    

        self.bm.StopAndDisconnect()
        self.writeToLog("CHG", cycle, origChargeRate, capacityCharged/3.6,
            energy/3.6, chargeImpedance, formSettings)

        return elapsed


    def waitSeconds(self, seconds):

        #if( graph == NULL )
        #    allocateGraph(0,0);
        start = time.time()
        
        while True:
        
            remaining = start + seconds - time.time()

            if (remaining < 0):
                break

            self.canvas.graph.WriteBottomLine("Waiting... %d"%remaining)

            self.canvas.update()

            if settings.stoprequested:
                return False
            
        return True


    def AutoCycle(self, formSettings):

        dischargeT = lastDischargeT = 0

        for i in range(1, formSettings['maximumCycles']+1):
            
            dischargeT = self.PerformDischarge(i, formSettings)
            print("DischargeT %s"%dischargeT)
            if dischargeT is None:
                break
            
            if not self.waitSeconds(settings.cycleRestTime):
                break
            
            
            if self.PerformCharge(i, dischargeT, formSettings) is None:
                break            
            
            # Save graph of just completed cycle if requested.
            if (formSettings['saveGraph']): #&& graph != NULL ) {
                self.canvas.graph.SaveToFile(time.strftime("%Y%m%d-%H%M%S.bmp"))

            if not self.waitSeconds(settings.cycleRestTime):
                break

            # Stop if capacity has not increased significantly since the
            # previous cycle.
            if( i > 2 and formSettings['stopAfterSmallIncrease']
                and dischargeT <= lastDischargeT * settings.cycleTerminationRatio):
                break
            
            lastDischargeT = dischargeT
            


    def CheckImpedance(self, which, formSettings):
    #double v1, v2, resC, resD;
    
    #define IMPEDANCE_DISCHARGE -1
    #define IMPEDANCE_CHARGE 1
    #define IMPEDANCE_BOTH 0

    #graph->WriteBottomLine("One moment please...");
    
        self.allocateGraph(0,0)
        
        self.canvas.graph.WriteBottomLine("One moment please...")

        self.takeReading(True)

        if (which == 'IMPEDANCE_BOTH'):
            self.canvas.graph.Render(-1)

        if which in ('IMPEDANCE_BOTH', 'IMPEDANCE_DISCHARGE'):
            self.canvas.graph.WriteTopLine("Measuring Discharge Impedance")
            self.bm.DischargeMode(formSettings['dischargeRateCode'])
            v1 = self.takeReading(True)
            self.bm.DischargeMode(0)
            time.sleep(0.1)
            v2 = self.takeReading(True)
            resD = (v2-v1) / settings.dischargeRates[formSettings['dischargeRateCode']]

        if which in ('IMPEDANCE_BOTH', 'IMPEDANCE_CHARGE'):
            self.canvas.graph.WriteTopLine("Measuring Charge Impedance")
            self.bm.ChargeMode(formSettings['chargeRateCode'])
            v1 = self.takeReading(True)
            self.bm.ChargeMode(0)
            time.sleep(0.1)
            v2 = self.takeReading(True)
            resC = (v1-v2) / settings.chargeRates[formSettings['chargeRateCode']]

        if (which == 'IMPEDANCE_BOTH'):
            self.bm.StopAndDisconnect()
            self.canvas.graph.WriteTopLine(
                "Charge: %1.4f ohms (at %1.0f mA)  Discharge: %1.4f ohms (at %1.0f mA)  Average: %1.4f ohms"%
                (resC, settings.chargeRates[formSettings['chargeRateCode']]*1000,
                resD, settings.dischargeRates[formSettings['dischargeRateCode']]*1000,
                (resC+resD)/2))
            self.canvas.graph.WriteBottomLine(" ");
        
        return (resD if which == 'IMPEDANCE_DISCHARGE' else resC)


    def MonitorVoltage(self):

        v = self.takeReading(True)
        self.allocateGraph(v-0.05, v+0.05)

        self.canvas.graph.WriteTopLine("Monitor")

        self.start = time.time()

        done = False
        
        while not done:

            now = time.time()
            elapsed = now - self.start

            v = self.takeReading()

            self.canvas.graph.WriteBottomLine("Time: %d:%02d:%02d  Voltage: %1.2fV"\
                %(elapsed/3600, (elapsed%3600)/60, elapsed%60, v))

            self.canvas.graph.AddPoint(elapsed, v)
            print(elapsed,v)

            self.canvas.update()
            
            time.sleep(1)
            
            if settings.stoprequested:
                done = True

    
    def SaveGraphToFile(self, fileName):
        self.canvas.graph.SaveToFile(fileName)