# BattManPi
A project to redesign Stefan Vorkoetter's BattMan II for Raspberry Pi:  
http://www.stefanv.com/electronics/battman2.html

BattMan II is a computer-controlled battery manager which can be used
to charge and discharge common types of rechargeable batteries.

The original project used a Borland C++ program under Windows to drive
the hardware through the PC LPT port.  These days LPT ports are rare, and
no-one has updated the software to use another interface method such as
a USB GPIO module.

There are three aspects to this project.  First, redesign the circuit to
operate with the Raspberry Pi 3.3V GPIO levels.  Second, lay out a new
PCB for the new circuit.  Third, translate the Borland C++ code to
something that will run on the Pi.

The first phase is addressed by the schematic found in the project files
here.  The schematic was drawn using KiCAD, which was then used to do
the PCB artwork for the second phase.  For the third phase, the original
C++ code has been converted to Python with a TKinter GUI.  Permission has
been granted to release the new code under the GPL.  This does not
affect the license of the original code.

At the time of writing the schematic, PCB artwork, and software are ready
for testing.  The PCB has not been fabricated, so the circuit and the
software have not been tested.  I hope to have time to do this in April
or May 2017.

The original design is copyright Stefan Vorkoetter 2007.
