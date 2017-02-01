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


    def MonitorVoltage(self, startup=False):

        if startup:

            v = self.takeReading(True)
            self.allocateGraph(v-0.05, v+0.05)

            self.canvas.graph.WriteTopLine("Monitor")

            self.start = time.time()
            
            self.counter = 0

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
    
    