#!/usr/bin/env python3
"""BattMan Pi main program"""

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
from tkinter import filedialog

from setup import setupDialog
from start import startDialog

from hardware import battman
from function import func

import graph

import settings

class MainApplication(tk.Tk):
    
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        
        self.bm = battman()
        self.func = func(self.parent,self.bm)
        
        self.initialize()
        
    def initialize(self):
        self.appIcon = tk.PhotoImage(data=settings.battmanicon)
        self.call('wm','iconphoto',self._w,self.appIcon)

        self.grid()
        
        self.dischargeIcon=tk.PhotoImage(data=settings.dischargeicon) 
        self.chargeIcon=tk.PhotoImage(data=settings.chargeicon) 
        self.autoCycleIcon=tk.PhotoImage(data=settings.autocycleicon) 
        self.resistanceIcon=tk.PhotoImage(data=settings.resistanceicon) 
        self.monitorIcon=tk.PhotoImage(data=settings.monitoricon) 
        self.setupIcon=tk.PhotoImage(data=settings.setupicon) 
        self.saveIcon=tk.PhotoImage(data=settings.saveicon) 
        self.exitIcon=tk.PhotoImage(data=settings.exiticon)
        self.stopIcon=tk.PhotoImage(data=settings.stopicon)

        self.buttonList=[]

        self.dischargeButton = ttk.Button(self, text="Discharge", underline=0, command=self.discharge, compound=tk.TOP, image=self.dischargeIcon)
        self.dischargeButton.grid(column=1, row=0, sticky=tk.W, padx=6, pady=6)
        self.buttonList.append(self.dischargeButton)
        
        self.chargeButton = ttk.Button(self, text="Charge", underline=0, command=self.charge, compound=tk.TOP, image=self.chargeIcon)
        self.chargeButton.grid(column=1, row=1, sticky=tk.W,padx=6,pady=6)
        self.buttonList.append(self.chargeButton)
        
        self.autoCycleButton = ttk.Button(self, text="Auto Cycle", underline=0, command=self.autoCycle, compound=tk.TOP, image=self.autoCycleIcon)
        self.autoCycleButton.grid(column=1, row=2, sticky=tk.W,padx=6,pady=6)
        self.buttonList.append(self.autoCycleButton)
        
        self.resistanceButton = ttk.Button(self, text="Resistance", underline=0, command=self.resistance, compound=tk.TOP, image=self.resistanceIcon)
        self.resistanceButton.grid(column=1, row=3, sticky=tk.W,padx=6,pady=6)
        self.buttonList.append(self.resistanceButton)
        
        self.monitorButton = ttk.Button(self, text="Monitor", underline=0, command=self.monitor, compound=tk.TOP, image=self.monitorIcon)
        self.monitorButton.grid(column=1, row=4, sticky=tk.W,padx=6,pady=6)
        self.buttonList.append(self.monitorButton)
        
        self.setupButton = ttk.Button(self, text="Setup", underline=3, command=self.setup, compound=tk.TOP, image=self.setupIcon)
        self.setupButton.grid(column=1, row=5, sticky=tk.W, padx=6,pady=26)
        self.buttonList.append(self.setupButton)
        
        self.saveButton = ttk.Button(self, text="Save", underline=0, command=self.save, compound=tk.TOP, image=self.saveIcon)
        self.saveButton.grid(column=1, row=6, sticky=tk.W,padx=6,pady=6)
        self.buttonList.append(self.saveButton)
        
        self.exitButton = ttk.Button(self, text="Exit", underline=1, command=self.exit, compound=tk.TOP, image=self.exitIcon)
        self.exitButton.grid(column=1, row=7, sticky=tk.W,padx=6,pady=6)
        self.buttonList.append(self.exitButton)
        
        self.stopButton = ttk.Button(self, text="Stop", underline=1, command=self.stop, compound=tk.TOP, image=self.stopIcon)
        self.stopButton.grid(column=1, row=0, rowspan=8, sticky=tk.W,padx=6,pady=6)
        self.stopButton.grid_remove()
        
        self.canvas = tk.Canvas(self, bg='black', height=480, width=640, borderwidth=2, relief=tk.SUNKEN)
        self.canvas.grid(column=2, row=0, rowspan=8, sticky=(tk.N, tk.W, tk.E, tk.S), padx=(0,6), pady=6)

        self.func.canvas = self.canvas
        
        self.resizable(False,False)


    def showButtons(self):
        # Show the main buttons (not "Stop")
        for button in self.buttonList:
            button.grid()
        self.stopButton.grid_remove()    


    def hideButtons(self):
        # Hide the main buttons (show only "Stop")
        for button in self.buttonList:
            button.grid_remove()
        self.stopButton.grid()    


    def discharge(self, *args):
        dlg=startDialog(self.parent, title="Discharge Settings", mode='discharge')
        if dlg.result is not None:
            # Start pressed
            settings.stoprequested = False
            self.hideButtons()
            print (dlg.result)
            self.func.PerformDischarge(0, dlg.result)
            self.showButtons()
        else:
            # Cancel pressed
            pass

    
    def charge(self, *args):
        dlg=startDialog(self.parent, title="Charge Settings", mode='charge')
        if dlg.result is not None:
            # Start pressed
            settings.stoprequested = False
            self.hideButtons()
            print (dlg.result)
            self.func.PerformCharge(0, 0, dlg.result)
            self.showButtons()
        else:
            # Cancel pressed
            pass


    def autoCycle(self, *args):
        dlg=startDialog(self.parent, title="Auto Cycle Settings", mode='autocycle')
        if dlg.result is not None:
            # Start pressed
            settings.stoprequested = False
            self.hideButtons()
            print (dlg.result)
            self.func.AutoCycle(dlg.result)
            self.showButtons()
        else:
            # Cancel pressed
            pass


    def resistance(self, *args):
        dlg=startDialog(self.parent, title="Internal Resistance Test Settings", mode='resistance')
        if dlg.result is not None:
            # Start pressed
            settings.stoprequested = False
            self.hideButtons()
            print (dlg.result)
            self.canvas.graph = graph.graph(0,0, self.canvas)
            self.func.CheckImpedance('IMPEDANCE_BOTH', dlg.result)
            del self.canvas.graph
            self.showButtons()
        else:
            # Cancel pressed
            pass
        

    def monitor(self, *args):
        settings.stoprequested = False
        self.hideButtons()
        self.func.MonitorVoltage()
        self.showButtons()
            

    def setup(self, *args):
        dlg=setupDialog(self.parent, title='BattMan Pi Setup Assistant', bm=self.bm)
 

    def stop(self):
        settings.stoprequested = True
        #self.showButtons()


    def save(self, *args):
        fileName = filedialog.asksaveasfilename(title = "Save Graph",
            filetypes = (("Windows Bitmap","*.bmp"),
                         ("Portable Network Graphics","*.png"),
                         ("all files","*.*")))
        if fileName:
            self.canvas.graph.SaveToFile(fileName)


    def exit(self, *args):
        self.bm.Exit()
        self.quit()



if __name__ == "__main__":
    
    app = MainApplication(None)
    app.title('BattMan Pi - Computer Controlled Battery Manager - v0.1')
    app.mainloop()