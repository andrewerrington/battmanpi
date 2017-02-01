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

bitWeights=tuple(float(x) for x in filter(None, [x.strip() for x in config.get('voltage','DACbitWeights').splitlines()]))

DAClowMultiplier=config.getfloat('voltage','DAClowMultiplier')
DAChighMultiplier=config.getfloat('voltage','DAChighMultiplier')

dischargeRates=tuple(float(x) for x in filter(None, [x.strip() for x in config.get('current','discharge').splitlines()]))
chargeRates=tuple(float(x) for x in filter(None, [x.strip() for x in config.get('current','charge').splitlines()]))

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