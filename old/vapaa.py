# -*- coding:utf-8 -*-
#!/usr/bin/env python
#
#   Copyright 2018 Eric Yang
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

"""

.. moduleauthor:: eric yang <tomdy@hotmail.com>

vapaa: A Python driver for the Greenhouse environmental control system.

This Python file was changed (committed) at $Date: 2018-12-15 01:29:19 +0200 (Sun, 22 Jun 2018) $,
which was $Revision: 200 $.

"""

__author__   = 'Eric Yang'
__email__    = 'tomdy@hotmail.com'
__url__      = 'https://opengovtw.com/ban/28084557'
__license__  = 'Apache License, Version 2.0'

__version__  = '0.0.1'
__status__   = 'Beta'
__revision__ = '$Rev: 200 $'
__date__     = '$Date: 2018-12-15 01:29:19 +0200 (Sun, 22 Jun 2018) $'

import serial
import minimalmodbus
import time

def chack_flag(flag):
    if flag!=0:
        time.sleep(0.3)
        flag=0
    else:
        time.sleep(0.3)
        flag=1

def calcFromA(max,min,data):
    x=((data-4)*(max-min)/16)+min
    return round(x,1)

def calcFromV(max,min,data):
    return int(((max-min)/10)*data+min)

class conn():
 def __init__(self, com):
  flag=0
  self.conn=minimalmodbus.Instrument(com,1)
  self.conn.serial.baudrate=9600
  self.conn.serial.bytesize=8
  self.conn.serial.parity=serial.PARITY_NONE
  self.conn.serial.stopbits=1
  self.conn.serial.timeout=0.4 # seconds. At least 0.2 seconds required for 2400 bits/s.
  self.conn.mode=minimalmodbus.MODE_ASCII

 def ai(self, id, type):
     id=id-1
     chack_flag(0)
     self.conn.address=97
     try:
         data=self.conn.read_register(id,3,4,signed=False)
         if type=='T':
             return calcFromA(80, -40, data)
         elif type=='RH':
             return calcFromA(100, 0, data)
         elif type=='soil':
             return calcFromA(100, 0, data)
             #return calcFromV(333 self.assertNotIn(needle, haystack, 'message'), 0, data)
         else:
            return data
     except Exception as e:
         print("error:" + str(e))

 def do(self, id, on):
     id=id-1
     chack_flag(1)
     self.conn.address=33
     try:
         self.conn.write_bit(id, on, 15)
     except Exception as e:
         print("error:" + str(e))
