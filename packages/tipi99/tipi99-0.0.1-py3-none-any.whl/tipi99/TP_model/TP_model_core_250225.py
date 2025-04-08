# -*- coding: utf-8 -*-
"""
This file is part of

TiPi99:
    Graphical user interface to configure the Autonomous Temperature Pressure Sensor TP99 and download the registered data.

Author:
    Yiuri Garino @ yiuri.garino@cnrs.fr

Copyright (c) 2024-2025 Yiuri Garino

Download:
    https://github.com/CelluleProjet/TiPi99

Version: 0.0.1
Release: 250407

License: GPLv3

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

"""

import configparser as cp
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import os, sys
from datetime import datetime

debug = True


script = os.path.abspath(__file__)
script_dir = os.path.dirname(script)
script_name = os.path.basename(script)


if __name__ == '__main__':
    from my_serial.my_serial_250213 import my_Serial, my_Serial_Thread_Open, my_Serial_Thread_Read, my_Serial_Thread_Reset
    from my_time.my_time_241007 import my_Time
else:
    from .my_serial.my_serial_250213 import my_Serial, my_Serial_Thread_Open, my_Serial_Thread_Read, my_Serial_Thread_Reset
    from .my_time.my_time_241007 import my_Time
    
# from my_serial.my_serial_241018 import my_Serial

class my_model():
    def __init__(self, debug = False):

        self.debug = debug
        self.statusbar_message_ref = [print] #List of messages method (print, label, statusbar, etc)
        
        self.mySerial = my_Serial(self.debug)
        self.my_Serial_Thread_Open = my_Serial_Thread_Open(self.mySerial)
        self.my_Serial_Thread_Read = my_Serial_Thread_Read(self.mySerial)
        self.my_Serial_Thread_Reset = my_Serial_Thread_Reset(self.mySerial)
        
        self.time = my_Time(self.debug)
        
        self.script = script
        self.script_dir = script_dir
        self.script_name = script_name
        self.start_date = datetime.now()
        self.start_name = self.start_date.strftime("%y%m%d_%H%M%S")
        
        
    def statusbar_message_add(self, method):
        #print(method)
        self.statusbar_message_ref.append(method)
        
    def statusbar_message(self, message):
        now = datetime.now()
        text = now.strftime("%H:%M:%S : ") + message
        for method in self.statusbar_message_ref:
            method(text)



if __name__ == '__main__':
    test = my_model(True)
    print(test.time.TM_s_string(154545))




