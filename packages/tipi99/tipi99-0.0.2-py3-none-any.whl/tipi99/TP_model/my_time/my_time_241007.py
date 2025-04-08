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

def reset():
    import sys
    
    if hasattr(sys, 'ps1'):
        
        #clean Console and Memory
        from IPython import get_ipython
        get_ipython().run_line_magic('clear','/')
        get_ipython().run_line_magic('reset','-sf')
        print("Running interactively")
        print()
    else:
        print("Running in terminal")
        print()


if __name__ == '__main__':
    reset()


from datetime import datetime


class my_Time():
    def __init__(self, debug = False):
        self.debug = debug
                
    def TM_s_string(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        years, days = divmod(days, 365)
        _ = ''
        labels = ['y', 'd', 'h', 'min', 'sec']
        for i, val in enumerate([years, days, hours, minutes, seconds]):
            if val != 0:
                
                _+=  f'{val} {labels[i]} '
        return _
    
    def TM_print_time(self, event = None, Message = 'Now = '):
        now = datetime.now()
        current_time = now.strftime("%A %d %B %Y %H:%M:%S")
        print(Message + current_time)
    
if __name__ == '__main__':
    test = my_Time()
    print(test.TM_s_string(154545))