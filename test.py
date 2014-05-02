#!/usr/bin/env python
import curses
from pprint import pformat
import pycarrera
import time

from pycarrera.monitor import RaceMonitor
race_monitor = RaceMonitor('/dev/ttyUSB0')

stdscr = curses.initscr()

while True:
    try:
        status = pformat(race_monitor.race_status)
        stdscr.addstr(0, 0, status)
        stdscr.refresh()
        time.sleep(0.05)
    except (KeyboardInterrupt, SystemExit):
        curses.endwin()
        exit()


