#!/usr/bin/env python3
"""BattMan Pi .ini file reader and settings"""

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


import configparser

config = configparser.ConfigParser()

config.read('battmanpi.ini')

bitWeights=tuple(float(x) for x in filter(None,
    [x.strip() for x in config.get('voltage','DACbitWeights').splitlines()]))

DAClowMultiplier=config.getfloat('voltage','DAClowMultiplier')
DAChighMultiplier=config.getfloat('voltage','DAChighMultiplier')

dischargeRates=tuple(float(x) for x in filter(None,
    [x.strip() for x in config.get('current','discharge').splitlines()]))
chargeRates=tuple(float(x) for x in filter(None,
    [x.strip() for x in config.get('current','charge').splitlines()]))

numChargeRates=config.getint('current','numChargeRates')

niCdDeltaV=config.getfloat('chemistry','NiCddV')
niCdVMin=config.getfloat('chemistry','NiCdVmin')

niMHDeltaV=config.getfloat('chemistry','NiMHdV')
niMHVMin=config.getfloat('chemistry','NiMHVmin')

deltaVDuration=config.getfloat('chemistry','NiCdNiMHdVt')

cycleTerminationRatio=config.getfloat('chemistry','autoCycleTerminationRatio')

cycleRestTime=config.getfloat('chemistry','cycleRestTime')

liPoVMax=config.getfloat('chemistry','LiPoVmax')
liPoVMin=config.getfloat('chemistry','LiPoVmin')

liNPVMax=config.getfloat('chemistry','LiNPVmax')
liNPVMin=config.getfloat('chemistry','LiNPVmin')

pbAcidVMax=config.getfloat('chemistry','PbAcidVmax')
pbAcidVMin=config.getfloat('chemistry','PbAcidVmin')


# Application settings and globals
stoprequested = False

MAX_CAPACITY=99999


# Base64 encoded GIF icons
tickicon='''
R0lGODlhEAAQAPEAAACAAAD/AAAAgAAAACH5BAEAAAMALAAAAAAQABAAAAIsnI8YyRcAWnpASAfr
HVTfbn1ZaCzKeJocimQLyAhu5iUyXcc0Kd38JfhthgUAOw==
'''

stopicon='''
R0lGODlhEAAQAPEBAP8AAP///wAAAAAAACH5BAEAAAIALAAAAAAQABAAAAI1lBWpeR0AIwwNyQuo
efhS3nlPkpHmOEbcWWbqhLbubMLT3a4xncqh9PmpDqCOhhg6OhaKRgEAOw==
'''

setupicon='''
R0lGODlhEAAQAPIDAAAAAIsAAP8AAP///wAAAAAAAAAAAAAAACH5BAEAAAQALAAAAAAQABAAAAND
SLoUwQvI6WAceFSrgNMB0BESSYLBIJrsKQSC2on0qWFrbk485zcPC0+yEWZAP0/KkdOdHCnnxAWT
kaSYlHXFGpZ8CQA7
'''

saveicon='''
R0lGODlhEAAQAPIAAAAAAP8AAAAA/5mZmczMzP///wAAAAAAACH5BAEAAAYALAAAAAAQABAAAANK
CLrW/qDIoky410UwKG0D1kQTCTSisa1MSk4TJrMbJQcqDJ8utQ4AgTAgVOgkr1KydFw4n88HBHqS
jgCELKFiVWGx26pVARwAAQkAOw==
'''

resistanceicon='''
R0lGODlhEAAQAPIEAAAAAP8wMJmZmczMzP///wAAAAAAAAAAACH5BAEAAAUALAAAAAAQABAAAANE
CLrcBSQSIakEb8odKYZRwG3fJo7EZ4XCsAllJQTCmj5NvhR87/9ADE/4AMIEhWOS2PsUnUIAEvpc
DqtUn3IrDTa/vgQAOw==
'''

monitoricon='''
R0lGODlhEAAQAPEAAAAAAP8wMAAAAAAAACH5BAEAAAIALAAAAAAQABAAAAInFISpe+sI2nNyqmph
vjL45AUJEIIf8mGZOkXb9Y6xFkf2jbvSLgsFADs=
'''

exiticon='''
R0lGODlhEAAQAPEAAIsAAP8AAJmZmQAAACH5BAEAAAMALAAAAAAQABAAAAIvnI+pGRAMIIinAVHn
RXZ3LF0aqHQTuZioop2LYbpl264qTaqDDo/Z9rOtBoLhogAAOw==
'''

dischargeicon='''
R0lGODlhEAAQAPEAAAAAAP8AAP8wMAAAACH5BAEAAAMALAAAAAAQABAAAAItHDSpu8efABgBvllt
S1kb7hkTF5TWyJSmglpdC2VSSEW0TNewK/X+P0MJWYkCADs=
'''

chargeicon='''
R0lGODlhEAAQAPEAAAAAAP8AAAAAAAAAACH5BAEAAAIALAAAAAAQABAAAAIsFISpGbaPAjhQNVcZ
ovnivnFWQCocWUKUl61ZKLBt/CaA3OLqxPf+wQnaEAUAOw==
'''

battmanicon='''
R0lGODlhIAAgAPIGAAAAAP8AAP//AAAA//8A/8DAwP///wAAACH5BAEAAAcALAAAAAAgACAAAAPO
eLrcBxC6SVcpMYNatdEZ54CAYZpDJDJQIAjReYYiBr2RKxupSkEfUAAykGl+QI0LVjr1AMNNI8a7
vZjNqtWnoJpI2cyV+wDKntnnEsf17pziK1vSdRs18jENDM7raWV8Vn5YQVIHWEKEfwRfdIiJa4sZ
jSiPTItyUXZBLIN+JHBFbRGgIEWOQD0LcX8RqAYElFqsrYmwqQCoZBkBbzuyr7menHdUaCMZv8FE
WoDEum/KYEjFhiQcGbjM1CLKudgrtUVoIOJTF3znFOnPFAkAOw==
'''

autocycleicon='''
R0lGODlhEAAQAPEAAAAAAP8wMAAAAAAAACH5BAEAAAIALAAAAAAQABAAAAIwFISpGbaPAjhQNVcZ
ojD4BFyLuIXdc5CCuq0jRHksyEVZ7VZ4jj7zBAwKJ5gih1IAADs=
'''