#!/usr/bin/env python

#  Copyright (C) Roberto Calvo 2013
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see http://www.gnu.org/licenses/.
#
#  Authors : Roberto Calvo <rocapal at gmail dot com>

import RPi.GPIO as GPIO, time, os

RED = 23
GREEN = 24
BLUE = 25


GPIO.setwarnings(False)


def led (stateR, stateG, stateB):
	GPIO.output(RED,stateR)
	GPIO.output(GREEN,stateG)
	GPIO.output(BLUE,stateB)

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)

led (False, True, True)
time.sleep(1)
led (True, False, True)
time.sleep(1)
led (True, True,False)
time.sleep(1)
led (True, True, True)
time.sleep(1)
