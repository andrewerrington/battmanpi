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


    def writeToLog(oper, cycle, rate, capacity, energy, resistance):

        newFile = False
        try:
            fp = open(LOG_FILE, "r")
        except FileNotFoundError:
            newFile = True

        fp = open(LOG_FILE,"a")
        
        #if( fp != NULL ) { FIXME: Check file was opened successfully
        if newFile:
            fp.write('"Date/Time","Mode","Cycle","Of","Type","Rated","Cells","mA","mAh","mWh","Ohms","V/Cell"\n')

        # FIXME: get StartForm variables from somewhere
        fp.write('"%s","%s",%d,%d,"%s",%d,%d,%1.1f,%1.1f,%1.1f,%1.4f,%1.4f\n'%
                (time.strftime("%Y-%m-%d %H:%M:%S"), oper, StartForm.maximumCycles if cycle else 0,
                StartForm.cellType, StartForm.capacity, StartForm.numberOfCells, rate*1000,
                capacity, energy, resistance, 0.0 if capacity==0 else energy/(capacity*StartForm.numberOfCells)))
        fp.close()


    def waitSeconds(self, seconds, startup=False):

        #if( graph == NULL )
        #    allocateGraph(0,0);

        if startup:
            self.waitSecondsStart = time.time()
            self.waitSecondsRunning = True
            self.waitSecondsNormalExit = False

        # Wait loop here
        self.waitSecondsRemaining = self.waitSecondsStart + seconds - time.time()

        if (remaining < 0):
            # Time passed successfully
            #break;
            self.waitSecondsRunning = False
            self.waitSecondsNormalExit = True

        else:
            # Still counting down
            self.canvas.graph.WriteBottomLine("Waiting... %d"%self.waitSecondsRemaining)
            if not settings.stoprequested:
                self.canvas.after(1000, lambda: self.waitSeconds(self, seconds))
            else:
                self.waitSecondsRunning = False


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
                "Charge: %1.4f Ohms (at %1.0f mA)  Discharge: %1.4f Ohms (at %1.0f mA)  Average: %1.4f Ohms"%
                (resC, settings.chargeRates[formSettings['chargeRateCode']]*1000,
                resD, settings.dischargeRates[formSettings['dischargeRateCode']]*1000,
                (resC+resD)/2))
            self.canvas.graph.WriteBottomLine(" ");
        
        return (resD if which == 'IMPEDANCE_DISCHARGE' else resC)


    def MonitorVoltage(self, startup=False):

        if startup:

            v = self.takeReading(True)
            self.allocateGraph(v-0.05, v+0.05)

            self.canvas.graph.WriteTopLine("Monitor")

            self.start = time.time()

        # This is an infinite loop and it will call itself until a flag on the
        # main form indicates it should stop.

        now = time.time()
        elapsed = now - self.start

        v = self.takeReading()

        self.canvas.graph.WriteBottomLine("Time: %d:%02d:%02d  Voltage: %1.2fV"\
            %(elapsed/3600, (elapsed%3600)/60, elapsed%60, v))

        self.canvas.graph.AddPoint(elapsed, v)

        self.canvas.update()
        
        if not settings.stoprequested:
            self.canvas.after(1000, self.MonitorVoltage)
    
    
    def SaveGraphToFile(self, fileName):
        self.canvas.graph.SaveToFile(fileName)
    
'''
time_t PerformDischarge( int cycle )
{
    double vMin = 0.0;
    if( StartForm->cellType == "NiCd" )
        vMin = Settings.niCdVMin * StartForm->numberOfCells;
    else if( StartForm->cellType == "NiMH" )
        vMin = Settings.niMHVMin * StartForm->numberOfCells;
    else if( StartForm->cellType == "LiPo" )
        vMin = Settings.liPoVMin * StartForm->numberOfCells;
    else if( StartForm->cellType == "LiNP" )
        vMin = Settings.liNPVMin * StartForm->numberOfCells;
    else if( StartForm->cellType == "PbAcid" )
        vMin = Settings.pbAcidVMin * StartForm->numberOfCells;
    else {
        MessageDlg(AnsiString("Unrecognized cell type: ") + StartForm->cellType,
                   mtError,TMsgDlgButtons() << mbOK,0);
        return( -1 );
    }

    double dischargeRate =
        Settings.dischargeRates[StartForm->dischargeRateCode];

    if( graph == NULL )
        allocateGraph(0,0);
    double dischargeImpedance = CheckImpedance(IMPEDANCE_DISCHARGE,graph);

    /* Measured cut-off voltage is minimum no-load voltage minus the drop we
       get due to impedance. */
    double vCutOff = vMin - dischargeImpedance * dischargeRate;

    /* Take an initial reading to know where to start the graph. */
    double v = takeReading(true);
    allocateGraph(v > vCutOff ? vCutOff : v-0.05, v+0.05);

    /* Write discharge information on top line. */
    char buf[200];
    strcpy(buf,"Discharge");
    if( cycle )
        sprintf(buf+strlen(buf)," %d of %d",cycle,StartForm->maximumCycles);
    sprintf(buf+strlen(buf),"  Battery: %d %s",
            StartForm->numberOfCells,StartForm->cellType.c_str());
    sprintf(buf+strlen(buf),"  Rate: %1.0fmA",dischargeRate*1000);
    sprintf(buf+strlen(buf),"  VMin: %1.2fV",vCutOff);
    sprintf(buf+strlen(buf),"  Resistance: %1.4f Ohms",dischargeImpedance);
    graph->WriteTopLine(buf);

    double energy = 0.0; // Watt-seconds
    double capacityDischarged = 0.0; // Amp-seconds

    time_t start = time(NULL), lastTime = start, elapsed;
    DischargeMode(StartForm->dischargeRateCode);

    for( bool done = false; !done; ) {
        time_t now = time(NULL);
        elapsed = now - start;
        v = takeReading();

        if( now > lastTime ) {
            capacityDischarged += dischargeRate;
            energy += dischargeRate * v;
            lastTime = now;
        }

        if( v < vCutOff )
            done = true;

        sprintf(buf,
            "Time: %d:%02d:%02d  Voltage: %1.2fV  Discharge: %1.0fmAh (%1.0fmWh)",
                elapsed/3600,(elapsed%3600)/60,elapsed%60,
                v,capacityDischarged/3.6,energy/3.6);
        graph->WriteBottomLine(buf);
        graph->AddPoint(elapsed,v);

        Application->ProcessMessages();
        if( MainForm->StopRequested() ) {
            StopAndDisconnect();
            return( -1 );
        }
    }

    StopAndDisconnect();
    writeToLog("DIS",cycle,dischargeRate,capacityDischarged/3.6,energy/3.6,
           dischargeImpedance);

    return( elapsed );
}

time_t PerformCharge( int cycle, time_t startAt )
{
    double deltaV = 1.0, vMax = 100.0;
    if( StartForm->cellType == "NiCd" )
        deltaV = Settings.niCdDeltaV;
    else if( StartForm->cellType == "NiMH" )
        deltaV = Settings.niMHDeltaV;
    else if( StartForm->cellType == "LiPo" )
        vMax = Settings.liPoVMax * StartForm->numberOfCells;
    else if( StartForm->cellType == "LiNP" )
        vMax = Settings.liNPVMax * StartForm->numberOfCells;
    else if( StartForm->cellType == "PbAcid" )
        vMax = Settings.pbAcidVMax * StartForm->numberOfCells;
    else {
        MessageDlg(AnsiString("Unrecognized cell type: ") + StartForm->cellType,
                   mtError,TMsgDlgButtons() << mbOK,0);
        return( -1 );
    }

    int chargeRateCode = StartForm->chargeRateCode;
    double chargeRate = Settings.chargeRates[chargeRateCode];
    double origChargeRate = chargeRate;
    time_t timeLimit = (time_t) (StartForm->capacity * 3.6 / chargeRate);
    if( deltaV < 1.0 )
        timeLimit *= 1.25;
    else
        timeLimit *= 1.75;

    if( graph == NULL )
        allocateGraph(0,0);
    double chargeImpedance = CheckImpedance(IMPEDANCE_CHARGE,graph);

    double v = takeReading(true);
    if( cycle == 0 )
        allocateGraph(v-0.05,v+0.05);

    char buf[200];
    strcpy(buf,"Charge");
    if( cycle )
        sprintf(buf+strlen(buf)," %d of %d",cycle,StartForm->maximumCycles);
    sprintf(buf+strlen(buf),"  Battery: %d %s",
            StartForm->numberOfCells,StartForm->cellType.c_str());
    sprintf(buf+strlen(buf),"  Rate: %1.0fmA",chargeRate*1000);
    if( deltaV < 1.0 )
        sprintf(buf+strlen(buf),"  Delta: %1.2f%%",deltaV*100);
    if( vMax < 100.0 )
        sprintf(buf+strlen(buf),"  VMax: %1.2fV",vMax);
    sprintf(buf+strlen(buf),"  TLimit: %2d:%02d:%02d",
            timeLimit/3600,(timeLimit%3600)/60,timeLimit%60);
    sprintf(buf+strlen(buf),"  Resistance: %1.4f Ohms",chargeImpedance);
    graph->WriteTopLine(buf);

    char dischargedCapacity[20];
    if( cycle ) {
        sprintf(dischargedCapacity,"/%1.0fmAh",
        startAt*Settings.dischargeRates[StartForm->dischargeRateCode]/3.6);
    }
    else
        *dischargedCapacity = '\0';

    double maxVoltageSeen = 0.0;
    double energy = 0.0; // Watt-seconds
    double capacityCharged = 0.0; // Amp-seconds

    time_t start = time(NULL), lastTime = start, elapsed;
    time_t lastTimeDeltaWasSmall = start;

    ChargeMode(chargeRateCode);

    for( bool done = false; !done; ) {
        time_t now = time(NULL);
        elapsed = now - start;
        v = takeReading();

        if( now > lastTime ) {
            capacityCharged += chargeRate;
            energy += chargeRate * v;
            lastTime = now;
        }

        double delta;
        if( elapsed > timeLimit )
            done = true;
        else if( v > vMax ) {
            NewChargeRate(--chargeRateCode);
            chargeRate = Settings.chargeRates[chargeRateCode];
            if( chargeRateCode == 0 )
                done = true;
            else {
                Sleep(100);
                takeReading(true);
            }
        }
        else if( elapsed > 60 ) {
            if( v > maxVoltageSeen )
                maxVoltageSeen = v;

            if( maxVoltageSeen == 0.0 )
                delta = 0.0;
            else
                delta = (maxVoltageSeen - v) / maxVoltageSeen;
            if( delta < deltaV )
                lastTimeDeltaWasSmall = now;
            if( now - lastTimeDeltaWasSmall > Settings.deltaVDuration )
                done = true;
        }
        else {
            delta = 0;
            lastTimeDeltaWasSmall = now;
        }

        sprintf(buf,
        "Time: %d:%02d:%02d  Voltage: %1.2fV  Charge: %1.0fmAh%s (%1.0fmWh)",
                elapsed/3600,(elapsed%3600)/60,elapsed%60,
                v,capacityCharged/3.6,dischargedCapacity,energy/3.6);
        if( deltaV < 1.0 )
            sprintf(buf+strlen(buf),"  Delta: %1.2f%% (%ds)",
                    delta*100,now-lastTimeDeltaWasSmall);
        graph->WriteBottomLine(buf);
        graph->AddPoint(elapsed+startAt,v);

        Application->ProcessMessages();
        if( MainForm->StopRequested() ) {
            StopAndDisconnect();
            return( -1 );
        }
    }

    StopAndDisconnect();
    writeToLog("CHG",cycle,origChargeRate,capacityCharged/3.6,energy/3.6,
           chargeImpedance);

    return( elapsed );
}

void AutoCycle( )
{
    time_t dischargeT, lastDischargeT = 0;

    for( int i = 1;
         i <= StartForm->maximumCycles && !MainForm->StopRequested(); ++i )
    {
        if( i != 1 && !waitSeconds(Settings.cycleRestTime)
         || (dischargeT = PerformDischarge(i)) == -1
         || !waitSeconds(Settings.cycleRestTime)
         || PerformCharge(i,dischargeT) == -1 )
        {
            break;
        }

    /* Save graph of just completed cycle if requested. */
        if( StartForm->saveGraph && graph != NULL ) {
            char fileName[64];
            time_t now = time(NULL);
            struct tm* tm = localtime(&now);
            sprintf(fileName,"%04d%02d%02d-%02d%02d%02d.bmp",
                    tm->tm_year + 1900, tm->tm_mon + 1, tm->tm_mday,
                    tm->tm_hour, tm->tm_min, tm->tm_sec);
            graph->SaveToFile(fileName);
        }

    /* Stop if capacity has not increased significantly since the previous
       cycle. */
        if( i > 2 && StartForm->stopAfterSmallIncrease
     && dischargeT <= lastDischargeT * Settings.cycleTerminationRatio )
    {
            break;
    }
        lastDischargeT = dischargeT;
    }
}
'''