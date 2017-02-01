from tkinter import *
from tkinter import ttk


def start(*args):
    pass


def cancel(*args):
    root.quit()


def updateDischargeRate(*args):
    # Send rate value to hardware
    rate=int(dischargeRate.get())
    dischargeRateLabel['text']="%i mA"%rate
    print("Sending %x to discharge rate control hardware."%rate)  # for debug


def updateChargeRate(*args):
    # Send rate value to hardware
    rate=int(chargeRate.get())
    chargeRateLabel['text']="%i mA"%rate
    print("Sending %x to charge rate control hardware."%rate)  # for debug


root = Tk()
root.title("BattMan Pi")

mainframe = ttk.Frame(root, padding="4 4 4 4")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)


# Battery
batteryGroup = ttk.LabelFrame(mainframe, text="Battery")
batteryGroup.grid(column=0, row=0, columnspan=2, sticky=(N, W, E, S))

ttk.Label(batteryGroup, text="Cell Type:").grid(column=0, row=0, sticky=E)
batteryCellTypeCombo=ttk.Combobox(batteryGroup,state='readonly', width=10, values=["NiCd","NiMH","LiPo","LiNP","PbAcid"])  # FIXME: Get this list from somewhere
batteryCellTypeCombo.grid(column=1,row=0,sticky=W)
batteryCellTypeCombo.current(1)

ttk.Label(batteryGroup, text="Capacity:").grid(column=2, row=0, sticky=E)
batteryCapacity=ttk.Entry(batteryGroup,width=10)
batteryCapacity.grid(column=3,row=0)

ttk.Label(batteryGroup, text="mAh").grid(column=4, row=0, sticky=W)

ttk.Label(batteryGroup, text="Number of Cells:").grid(column=5, row=0, sticky=E)

batteryNumberOfCells=Spinbox(batteryGroup, width=5, from_=1, to=12)
batteryNumberOfCells.grid(column=6,row=0)


# Discharge
dischargeRate=DoubleVar()   # IntVar doesn't seem to work

dischargeGroup = ttk.LabelFrame(mainframe, text="Discharge")
dischargeGroup.grid(column=0, row=1, sticky=(N, W, E, S))

ttk.Label(dischargeGroup, text="Rate:").grid(column=0, row=0, sticky=W)

dischargeRateScale=ttk.Scale(dischargeGroup, command=updateDischargeRate,
                             variable=dischargeRate, from_=0, to=15, orient=HORIZONTAL)
dischargeRateScale.grid(column=1,row=0,sticky=W)

dischargeRateLabel=ttk.Label(dischargeGroup)
dischargeRateLabel.grid(column=1, row=1)


# Charge
chargeRate=DoubleVar()   # IntVar doesn't seem to work

chargeGroup = ttk.LabelFrame(mainframe, text="Charge")
chargeGroup.grid(column=1, row=1, sticky=(N, W, E, S))

ttk.Label(chargeGroup, text="Rate:").grid(column=0, row=0, sticky=W)

chargeRateScale=ttk.Scale(chargeGroup, command=updateChargeRate,
                             variable=chargeRate, from_=0, to=15, orient=HORIZONTAL)
chargeRateScale.grid(column=1,row=0,sticky=W)

chargeRateLabel=ttk.Label(chargeGroup)
chargeRateLabel.grid(column=1, row=1)


# Auto Cycle
stopNoIncrease = BooleanVar()
saveGraph = BooleanVar()

autoCycleGroup = ttk.LabelFrame(mainframe, text="Auto Cycle")
autoCycleGroup.grid(column=0, row=2, columnspan=2, sticky=(N, W, E, S))

ttk.Label(autoCycleGroup, text="Maximum Number of Cycles:").grid(column=0, row=0, sticky=E)

autoCycleMaxCycles=Spinbox(autoCycleGroup, width=5, from_=1, to=99)
autoCycleMaxCycles.grid(column=1,row=0)

autoCycleStop=ttk.Checkbutton(autoCycleGroup,
                text="Stop when capacity increases by less than 0.5%", variable=stopNoIncrease)
autoCycleStop.grid(column=2,row=0,sticky=W)

autoCycleSave=ttk.Checkbutton(autoCycleGroup,
                text="Save graph as BMP file after each cycle", variable=saveGraph)
autoCycleSave.grid(column=2,row=1,sticky=W)

startIcon=PhotoImage(file="tick.gif")
cancelIcon=PhotoImage(file="exit.gif")

ttk.Button(mainframe, text="Start", compound=TOP, image=startIcon, command=start).grid(column=0, row=3, sticky=W)
ttk.Button(mainframe, text="Cancel", compound=TOP, image=cancelIcon, command=cancel).grid(column=1, row=3, sticky=E)


root.mainloop()
