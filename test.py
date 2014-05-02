#!/usr/bin/env python
from pprint import pprint
import pycarrera
from pycarrera.monitor import RaceMonitor
race_monitor = RaceMonitor('/dev/ttyUSB0')
pprint(race_monitor.race_status)

