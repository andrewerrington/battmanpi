# BattManPi
A project to redesign Stefan Vorkoetter's BattMan II for Raspberry Pi.
http://www.stefanv.com/electronics/battman2.html

The original project used a Borland C++ program under Windows to drive
the hardware through the PC LPT port.  These days LPT ports are rare, and
no-one has updated the software to use another interface method such as
a USB GPIO module.

There are three aspects to this project.  First, redesign the circuit to
operate with the Raspberry Pi 3.3V GPIO levels.  Second, lay out a new
PCB for the new circuit.  Third, translate the Borland C++ code to
something that will run on the Pi.

The first phase is addressed by the schematic found in the project files
here.  The schematic was drawn using KiCAD, which will be used to do
the PCB artwork for the second phase.  For the third phase I propose
to convert the C++ to Python with a simple GUI.

The original design is copyright Stefan Vorkoetter 2007.
