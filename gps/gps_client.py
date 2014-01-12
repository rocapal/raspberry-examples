#! /usr/bin/python

# Copyright 2014 (C) Roberto Calvo Palomino
# 
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
# 
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
# 
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see http://www.gnu.org/licenses/. 
# 
#   Based in a work of Dan Mandle http://dan.mandle.me September 2012
#
#   Author : Roberto Calvo Palomino <rocapal at gmail dot com>
#

#
# Before execute this script, be sure run following commands:
#
#   $ sudo killall gpsd
#   $ sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock
#


import os
from gps import *
from time import *
import time
import threading
from sys import stdout 

gpsd = None 
 
os.system('clear') 
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd 
    gpsd = gps(mode=WATCH_ENABLE) 
    self.current_value = None
    self.running = True 
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next()

 
if __name__ == '__main__':
  gpsp = GpsPoller()
  try:
    gpsp.start() 
    

    list = ['|','/','-','\\']
    c = 0

    sleep_data = 5

    while True:

      if (gpsd.fix.mode	== MODE_NO_FIX):
        stdout.write("\rWaiting for FIX: %s" % list[c])
        
        c = c+1
        if (c>2):
          c=0

        stdout.flush()
        time.sleep(2)

      else:

        os.system('clear')

        print
        print ' GPS reading'
        print '----------------------------------------'
        print 'latitude    ' , gpsd.fix.latitude
        print 'longitude   ' , gpsd.fix.longitude
        print 'time utc    ' , gpsd.utc
        print 'altitude (m)' , gpsd.fix.altitude
        print 'speed (m/s) ' , gpsd.fix.speed
        print 'mode        ' , gpsd.fix.mode
        print ' '

	f = open("/tmp/gps.txt", "w")
        f.write("datetime: " + str(gpsd.utc) + "\n")
        f.write("latitude: " + str(gpsd.fix.latitude) + "\n")
        f.write("longitude: " +str(gpsd.fix.longitude) + "\n")
        f.close()

        time.sleep(sleep_data) #set to whatever
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."
