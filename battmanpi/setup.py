#!/usr/bin/env python3
"""BattMan Pi setup GUI"""

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

class setupDialog(tkSimpleDialog.Dialog):
    
    def body(self, master):

        # The BattMan hardware object
        self.bm = self.kwargs['bm']
        
        # Rate control
        self.rateValue=tk.IntVar()

        rateControlGroup = ttk.LabelFrame(self, text="Rate Control (Bits 0 to 3)")
        rateControlGroup.grid(column=0, row=0, columnspan=2, sticky=(tk.N, tk.W, tk.E, tk.S), padx=(6,0), pady=(6,0))

        ttk.Label(rateControlGroup, text="Rate:", underline=0).grid(column=0, row=0, sticky=tk.E, padx=(4,0), pady=4)
        
        self.rateScale=ttk.Scale(rateControlGroup, command=self.updateRate, variable=self.rateValue, from_=0, to=15, orient=tk.HORIZONTAL)
        self.rateScale.grid(column=1, row=0, padx=4, pady=4)

        self.hexLabel=ttk.Label(rateControlGroup)
        self.hexLabel.grid(column=1, row=1, padx=4, pady=(0,4))

        self.updateRate()

        # Relay control
        self.modeRelay=tk.BooleanVar()
        self.batteryRelay=tk.BooleanVar()

        relayControlGroup = ttk.LabelFrame(self, text="Relay Control (Bits 4 and 5)")
        relayControlGroup.grid(column=0, row=1, columnspan=2, sticky=(tk.N, tk.W, tk.E, tk.S), padx=(6,0), pady=(6,0))

        ttk.Label(relayControlGroup, text="Mode:").grid(column=0, row=0, sticky=tk.E, padx=(4,0), pady=4)
        ttk.Radiobutton(relayControlGroup, text="Charge", underline=0, variable=self.modeRelay, command=self.updateModeRelay, value=1).grid(column=1, row=0, sticky=tk.W, padx=4, pady=4)
        ttk.Radiobutton(relayControlGroup, text="Discharge", underline=0, variable=self.modeRelay, command=self.updateModeRelay, value=0).grid(column=2, row=0, sticky=tk.W, padx=(0,4), pady=4)

        ttk.Label(relayControlGroup, text="Battery:").grid(column=0, row=1, sticky=tk.W)
        ttk.Radiobutton(relayControlGroup, text="Connect", underline=1, variable=self.batteryRelay, command=self.updateBatteryRelay, value=1).grid(column=1, row=1, sticky=tk.W, padx=4, pady=4)
        ttk.Radiobutton(relayControlGroup, text="Disconnect", underline=1, variable=self.batteryRelay, command=self.updateBatteryRelay, value=0).grid(column=2, row=1, sticky=tk.W, padx=(0,4), pady=(0,4))

        self.updateModeRelay()
        self.updateBatteryRelay()

        # D-to-A control
        D2AControlGroup = ttk.LabelFrame(self, text="D-to-A Control (Bits 6 and 7)")
        D2AControlGroup.grid(column=0, row=2, columnspan=2, sticky=(tk.N, tk.W, tk.E, tk.S), padx=(6,0), pady=(6,0))
        ttk.Label(D2AControlGroup, text="Count To:", underline=6).grid(column=0, row=0, sticky=tk.W, padx=4, pady=4)
        self.D2Acontrol=ttk.Combobox(D2AControlGroup, state='readonly', width=5, values=[0,1,2,4,8,16,32,64,128,256,512,1024,2048,4095])
        self.D2Acontrol.grid(column=1, row=0, padx=(0,4), pady=4)
        self.D2Acontrol.current(0)

        ttk.Button(D2AControlGroup, text="Set", underline=1, command=self.updateD2A).grid(column=2, row=0, sticky=tk.W,padx=(0,4),pady=4)
        self.updateD2A()

        # ini file editor
        iniFileGroup = ttk.LabelFrame(self, text="Configuration File (battmanpi.ini):", underline=14)
        iniFileGroup.grid(column=2,row=0, rowspan=4, padx=6, pady=6)
        self.iniFile=tk.Text(iniFileGroup)
        self.iniFile.grid(column=0, row=0, sticky=tk.W, padx=(4,0), pady=4)
        scrollb = tk.Scrollbar(iniFileGroup, command=self.iniFile.yview)
        scrollb.grid(row=0, column=1, sticky=(tk.N, tk.W, tk.E, tk.S), padx=(0,4), pady=4)
        self.iniFile['yscrollcommand'] = scrollb.set

        # Fill the text box with the contents of the .ini file
        with open('battmanpi.ini') as f:
            self.iniFile.insert(1.0,f.read())

        self.iniFile.edit_modified(False)

        self.saveIcon=tk.PhotoImage(data=settings.tickicon)
        self.cancelIcon=tk.PhotoImage(data=settings.exiticon) 

        ttk.Button(self, text="Save", underline=0, command=self.ok, compound=tk.TOP, image=self.saveIcon).grid(column=0, row=3, sticky=tk.W, padx=6, pady=6)
        ttk.Button(self, text="Cancel", underline=5, command=self.cancel, compound=tk.TOP, image=self.cancelIcon).grid(column=1, row=3, sticky=tk.E, padx=(6,0), pady=6)

        self.resizable(False,False)
        
        return self.rateScale


    def cancel(self, *args):
        if self.iniFile.edit_modified():
            result = messagebox.askyesnocancel("BattMan Pi", "'battmanpi.ini' has been modified.\nDo you want to save it?", icon='warning')
            # Yes: True, No: False, Cancel: None 
            if result is not None:
                if result:
                    self.ok()
                else:
                    self.exit()
        else:
            self.exit()


    def updateRate(self, *args):
        # Send rate value to hardware
        rate=self.rateValue.get()
        self.hexLabel['text']="Hex %02X"%rate
        print("Sending %x to rate control hardware."%rate)  # for debug
        self.bm.NewChargeRate(rate)


    def updateModeRelay(self, *args):
        # Set mode relay
        print("Mode relay on" if self.modeRelay.get() else "Mode relay off") # for debug
        self.bm.SetAll(self.rateValue.get(), self.modeRelay.get(), self.batteryRelay.get())


    def updateBatteryRelay(self, *args):
        # Set battery relay
        print("Battery relay on" if self.batteryRelay.get() else "Battery relay off") # for debug
        self.bm.SetAll(self.rateValue.get(), self.modeRelay.get(), self.batteryRelay.get())


    def updateD2A(self, *args):
        # Send D2A value to hardware
        print("Sending %s to D2A"%self.D2Acontrol.get()) # for debug
        self.bm.SetCount(int(self.D2Acontrol.get()))
        
    def exit(self):
        self.bm.StopAndDisconnect()
        self.destroy()
        
    def buttonbox(self):
        # OK/Cancel buttons are handled in body()
        pass
    
    def apply(self):
        if self.iniFile.edit_modified():
            with open("battmanpi.ini", "w") as f:
                f.write(self.iniFile.get(1.0, "end-1c"))
            self.iniFile.edit_modified(False)
