#!/usr/bin/env python3
"""BattMan Pi test configuration GUI"""

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


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import tkSimpleDialog

import settings

class startDialog(tkSimpleDialog.Dialog):

    def body(self, master):
        # Battery
        self.batteryGroup = ttk.LabelFrame(self, text="Battery", underline=0)
        self.batteryGroup.grid(column=0, row=0, columnspan=2, sticky=(tk.N, tk.W, tk.E, tk.S), padx=6, pady=(6,0))

        ttk.Label(self.batteryGroup, text="Cell Type:", underline=5).grid(column=0, row=0, sticky=tk.E, padx=(4,0), pady=4)
        self.batteryCellTypeCombo=ttk.Combobox(self.batteryGroup, state='readonly', width=10, values=["NiCd","NiMH","LiPo","LiNP","PbAcid"])  # FIXME: Get this list from somewhere
        self.batteryCellTypeCombo.grid(column=1, row=0, sticky=tk.W,padx=(4,0), pady=4)
        self.batteryCellTypeCombo.current(1)

        ttk.Label(self.batteryGroup, text="Capacity:", underline=1).grid(column=2, row=0, sticky=tk.E, padx=(4,0), pady=4)
        self.batteryCapacity=ttk.Entry(self.batteryGroup, width=10)
        self.batteryCapacity.grid(column=3, row=0, padx=(4,0), pady=4)

        ttk.Label(self.batteryGroup, text="mAh").grid(column=4, row=0, sticky=tk.W, padx=(4,0), pady=4)

        ttk.Label(self.batteryGroup, text="Number of Cells:", underline=0).grid(column=5, row=0, sticky=tk.E, padx=(4,0), pady=4)

        self.batteryNumberOfCells=tk.Spinbox(self.batteryGroup, width=5, from_=1, to=12)
        self.batteryNumberOfCells.grid(column=6, row=0, padx=4, pady=4)


        # Discharge
        self.dischargeRate = tk.IntVar()

        self.dischargeGroup = ttk.LabelFrame(self, text="Discharge", underline=0)
        self.dischargeGroup.grid(column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S), padx=(6,0), pady=(6,0))

        ttk.Label(self.dischargeGroup, text="Rate:", underline=3).grid(column=0, row=0, sticky=tk.W, padx=(4,0), pady=4)

        dischargeRateScale=ttk.Scale(self.dischargeGroup, command=self.updateDischargeRate,
                                    variable=self.dischargeRate, from_=0, to=settings.numChargeRates-1, orient=tk.HORIZONTAL)
        dischargeRateScale.grid(column=1, row=0, sticky=tk.W, padx=4, pady=4)

        self.dischargeRateLabel=ttk.Label(self.dischargeGroup)
        self.dischargeRateLabel.grid(column=1, row=1, padx=4, pady=(0,4))

        self.updateDischargeRate()
        

        # Charge
        self.chargeRate = tk.IntVar()

        self.chargeGroup = ttk.LabelFrame(self, text="Charge", underline=0)
        self.chargeGroup.grid(column=1, row=1, sticky=(tk.N, tk.W, tk.E, tk.S), padx=6, pady=(6,0))

        ttk.Label(self.chargeGroup, text="Rate:", underline=0).grid(column=0, row=0, sticky=tk.W, padx=(4,0), pady=4)

        chargeRateScale=ttk.Scale(self.chargeGroup, command=self.updateChargeRate,
                                    variable=self.chargeRate, from_=0, to=settings.numChargeRates-1, orient=tk.HORIZONTAL)
        chargeRateScale.grid(column=1, row=0, sticky=tk.W, padx=4, pady=4)

        self.chargeRateLabel=ttk.Label(self.chargeGroup)
        self.chargeRateLabel.grid(column=1, row=1, padx=4, pady=(0,4))
        
        self.updateChargeRate()
        

        # Auto Cycle
        self.stopCheckBox = tk.BooleanVar()
        self.saveGraphCheckBox = tk.BooleanVar()

        self.autoCycleGroup = ttk.LabelFrame(self, text="Auto Cycle", underline=1)
        self.autoCycleGroup.grid(column=0, row=2, columnspan=2, sticky=(tk.N, tk.W, tk.E, tk.S), padx=6, pady=(6,0))

        ttk.Label(self.autoCycleGroup, text="Maximum Number of Cycles:", underline=0).grid(column=0, row=0, sticky=tk.E, padx=(4,0), pady=4)

        self.autoCycleMaxCycles=tk.Spinbox(self.autoCycleGroup, width=5, from_=1, to=99)
        self.autoCycleMaxCycles.grid(column=1, row=0, padx=(4,0), pady=4)

        autoCycleStop=ttk.Checkbutton(self.autoCycleGroup,
                        text="Stop when capacity increases by less than 0.5%", underline=5, variable=self.stopCheckBox)
        autoCycleStop.grid(column=2, row=0, sticky=tk.W, padx=4, pady=4)

        autoCycleSave=ttk.Checkbutton(self.autoCycleGroup,
                        text="Save graph as BMP file after each cycle", underline=9, variable=self.saveGraphCheckBox)
        autoCycleSave.grid(column=2, row=1, sticky=tk.W, padx=4, pady=4)

        self.startIcon=tk.PhotoImage(file="tick.gif")
        self.cancelIcon=tk.PhotoImage(file="exit.gif")

        ttk.Button(self, text="Start", underline=0, compound=tk.TOP, image=self.startIcon, command=self.ok).grid(column=0, row=3, sticky=tk.W, padx=6, pady=6)
        ttk.Button(self, text="Cancel", underline=5, compound=tk.TOP, image=self.cancelIcon, command=self.cancel).grid(column=1, row=3, sticky=tk.E, padx=6, pady=6)

        self.showControls(self.kwargs['mode'])

        return self.batteryCellTypeCombo


    def showControls(self, mode):
        # Show and hide various panels depending on what action we are doing
        if mode=='discharge':
            self.batteryGroup.grid()
            self.dischargeGroup.grid()
            self.chargeGroup.grid_remove()
            self.autoCycleGroup.grid_remove()
        elif mode=='charge':
            self.batteryGroup.grid()
            self.dischargeGroup.grid_remove()
            self.chargeGroup.grid()
            self.autoCycleGroup.grid_remove()
        elif mode=='autocycle':
            self.batteryGroup.grid()
            self.dischargeGroup.grid()
            self.chargeGroup.grid()
            self.autoCycleGroup.grid()
        elif mode=='resistance':
            self.batteryGroup.grid_remove()
            self.dischargeGroup.grid()
            self.chargeGroup.grid()
            self.autoCycleGroup.grid_remove()
        else:
            # Unknown action.  Probably should throw an error
            pass


    def updateDischargeRate(self, *args):
        self.dischargeRateLabel['text']="%4.0f mA"%(settings.dischargeRates[self.dischargeRate.get()]*1000)


    def updateChargeRate(self, *args):
        self.chargeRateLabel['text']="%4.0f mA"%(settings.chargeRates[self.chargeRate.get()]*1000)

        
    def buttonbox(self):
        # OK/Cancel buttons are handled in body()
        pass
    
    
    def validate(self):
        if self.kwargs['mode'] is not 'resistance':
            try:
                batteryCapacity= int(self.batteryCapacity.get())
                if batteryCapacity < 1 or batteryCapacity > settings.MAX_CAPACITY:
                    raise ValueError
                #self.result = first, second
                return 1
            except ValueError:
                messagebox.showwarning("Error", "Please enter a value from 1 to %s for the Capacity"%settings.MAX_CAPACITY)
                return 0
        else:
            return 1
        

    def apply(self):
        # Stash results for caller to see
        self.result={}  # self.result is None if Cancel is pressed
        
        self.result['cellType']=self.batteryCellTypeCombo.get()
        
        try:
            batteryCapacity= int(self.batteryCapacity.get())
            self.result['capacity']=batteryCapacity
        except ValueError:
            self.result['capacity']=0
            
        self.result['numberOfCells']=self.batteryNumberOfCells.get()
        self.result['chargeRateCode']=self.chargeRate.get()
        self.result['dischargeRateCode']=self.dischargeRate.get()
        self.result['maximumCycles']=self.autoCycleMaxCycles.get()
        self.result['stopAfterSmallIncrease']=self.stopCheckBox.get()
        self.result['saveGraph']=self.saveGraphCheckBox.get()