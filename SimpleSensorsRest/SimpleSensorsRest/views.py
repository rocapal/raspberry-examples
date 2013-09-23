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

import os
import sys
import datetime
import collections
from django.http import HttpResponse, HttpResponseServerError
from django.utils import simplejson
from parser import *
import jsonpickle

from django.shortcuts import render
import RPi.GPIO as GPIO, time, os
import glob

import subprocess
import StringIO

JSON_MIMETYPE="application/json"


DOOR = 18

def getDoor():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(DOOR, GPIO.IN)
	return str(GPIO.input(DOOR))


def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def getTemp():
	os.system('modprobe w1-gpio')
	os.system('modprobe w1-therm')

	base_dir = '/sys/bus/w1/devices/'
	device_folder = glob.glob(base_dir + '28*')[0]
	device_file = device_folder + '/w1_slave'

    	lines = read_temp_raw(device_file)
    	while lines[0].strip()[-3:] != 'YES':
        	time.sleep(0.2)
        	lines = read_temp_raw()
 	equals_pos = lines[1].find('t=')
    	if equals_pos != -1:
        	temp_string = lines[1][equals_pos+2:]
        	temp_c = float(temp_string) / 1000.0
        	temp_f = temp_c * 9.0 / 5.0 + 32.0
        	return str(temp_c)

def execCommand (command):
	p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderror = p.communicate()
	return StringIO.StringIO(stdout)

def getTempRBP():
	lines = execCommand (["/usr/bin/vcgencmd", "measure_temp"])
	return lines.getvalue().split('=')[1].split('\'')[0]
	

def data(request):

        data = {'version' : '0.1',
		'temp'	  : getTemp(),
		'door'	  : getDoor(),
		'tempRBP' : getTempRBP()}

        return HttpResponse(simplejson.dumps(data), JSON_MIMETYPE)

