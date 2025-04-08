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
        terminal = False
    else:
        print("Running in terminal")
        print()
        terminal = True

if __name__ == '__main__':
    reset()

import configparser as cp
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.backend_bases import MouseEvent
from datetime import datetime
import sys 
import os

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
    
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar



class Data_Table(QtWidgets.QTableWidget):
    def __init__(self, model = None, debug = False):
        super().__init__()
        self.model = model 
        self.debug = debug
        if self.debug : print('\nData_Table 2411\n')
        self.table_col = 5
        self.table_row = 5
        self.editable = False
        self.setColumnCount(self.table_col)
        self.setRowCount(self.table_row )
        self.data_2D = None   
        self.timestamp = None #int, memo: elapsed = col 0
        self.timestamp_t0 = None #datetime64
        self.date = None #datetime64
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self)
   
    def fast_reset(self):
        self.table_col = 2
        self.table_row = 2
        self.setColumnCount(2)
        self.setRowCount(2)
        self.clear()
        
    def reset(self):
        tot = self.rowCount()
        self.data_2D = None
        for i in range(tot+1):
            self.removeColumn(i)
        
    def set_numpy_2D(self, data):
        self.setColumnCount(2)
        self.setRowCount(2)
        self.clear()
        row, col = data.shape
        self.data_2D = data
        self.table_row = row
        self.table_col = col
        self.setColumnCount(col)
        self.setRowCount(row)
        if self.debug: print('2D data, row ', self.table_row , ' col ', self.table_col)
        for i_r in range(row):
            for i_c in range(col):
                item = QtWidgets.QTableWidgetItem(f'{data[i_r,i_c]:.2f}')
                if not self.editable: item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.setItem(i_r, i_c, item)
    
    def update_timestamp(self, t0):
        col_elapsed = 0
        self.timestamp = self.data_2D[:,col_elapsed].astype(int) + t0
        # print(t0)
        # print(self.timestamp)
        # print(type(self.timestamp))
        #self.date = np.datetime64(t0, 's') + self.timestamp.astype(int).astype(np.timedelta64)
        # print(self.data_2D[:,col_elapsed])
        _elapsed = self.data_2D[:,col_elapsed].astype(int)
        # print(_elapsed)
        # print(type(_elapsed))
        self.date = np.datetime64(t0, 's') + _elapsed.astype(np.timedelta64)
        
        col_elapsed = 0
        col_timestamp = 3
        col_date = 4
        
        for i_r in range(self.table_row):
            
            timestamp = int(float(self.item(i_r, col_elapsed).text()) + t0)
            item = QtWidgets.QTableWidgetItem(f'{timestamp}')
            if not self.editable: item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.setItem(i_r, col_timestamp, item)
            
            time_string = datetime.utcfromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M:%S")
            item = QtWidgets.QTableWidgetItem(time_string)
            if not self.editable: item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.setItem(i_r, col_date, item)
        
        [self.resizeColumnToContents(i) for i in range(self.table_col)]
        
    def set_timestamp_date(self, col_elapsed, t0 = 0):
        ''' 
        Add 2 columns at the end of the table:
            timestamp = col_elapsed + t0
            date(timestamp)
        '''
        
        self.setColumnCount(self.table_col + 2)
        col_timestamp = self.table_col
        col_date = self.table_col + 1
        self.table_col = self.table_col + 2
        self.timestamp = self.data_2D[:,col_elapsed].astype(int)
        self.date = np.datetime64(t0, 's') + self.timestamp.astype(int).astype(np.timedelta64)
        
        if self.debug: print('set datetime, row ', self.table_row , ' col ', self.table_col)
        
        for i_r in range(self.table_row):
            
            timestamp = int(float(self.item(i_r, col_elapsed).text()) + t0)
            item = QtWidgets.QTableWidgetItem(f'{timestamp}')
            if not self.editable: item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.setItem(i_r, col_timestamp, item)
            
            time_string = datetime.utcfromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M:%S")
            item = QtWidgets.QTableWidgetItem(time_string)
            if not self.editable: item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.setItem(i_r, col_date, item)
        
        [self.resizeColumnToContents(i) for i in range(self.table_col)]
            
    def set_date(self, col_timestamp):
        #Add column Date to last position
        col_date = self.table_col 
        self.setColumnCount(self.table_col + 1)
        self.table_col = self.table_col + 1
        for i_r in range(self.table_row):
            timestamp = int(float(self.item(i_r, col_timestamp).text()))
            time_string = datetime.utcfromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M:%S")
            item = QtWidgets.QTableWidgetItem(time_string)
            if not self.editable: item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.setItem(i_r, col_date, item)
                
    def set_str_2D(self, data):
        self.clear()
        row, col = data.shape
        self.data_2D = data
        self.table_row = row
        self.table_col = col
        self.setColumnCount(col)
        self.setRowCount(row)
        for i_r in range(row):
            for i_c in range(col):
                item = QtWidgets.QTableWidgetItem(data[i_r,i_c])
                if not self.editable: item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.setItem(i_r, i_c, item)
    
    def set_col_names(self, names):
        if self.table_col != len(names):
            print('Wronge names number, columns number = ', self.table_col )
        else:
            self.setHorizontalHeaderLabels(names)
            
        [self.resizeColumnToContents(i) for i in range(self.table_col)]
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("""
                      * {
                          font-size: 15px;
                    }
                      """)

    window = Data_Table()
    
    #test_2D = np.diag(np.linspace(0,9,10),0)
    timestamp = np.arange(0,60*60*24*10,60*60*24)
    
    start_y = 1970 #int(now.strftime("%Y"))
    start_m = '01' #int(now.strftime("%m"))
    start_d = '01' #int(now.strftime("%d"))
    start_h = '00' #int(now.strftime("%H"))
    start_min = '00' #int(now.strftime("%M"))
    
    now = datetime.now()
    
    start_y = now.strftime("%Y")
    start_m = now.strftime("%m")
    start_d = now.strftime("%d")
    start_h = now.strftime("%H")
    start_min = now.strftime("%M")
    
    time_0 = np.datetime64(f'{start_y}-{start_m}-{start_d}T{start_h}:{start_min}:00')

    #time_0 = np.datetime64(now.strftime("%Y-%m-%dT%H:%M:%S"))
    np_time = time_0 + timestamp.astype(np.timedelta64)
    test_2D = np.array([timestamp, timestamp]).T
    
    window.set_numpy_2D(test_2D)
    #np.savetxt('test.txt', window.date)
    window.set_timestamp_date(0, 1731948847)
    #window.set_date(0)
    names = ['Name ' + str(int(i)) for i in np.linspace(0,9,10)]
    window.set_col_names(names)
    window.show()
    sys.exit(app.exec())
    
    plt.plot(window.date, timestamp)
    ax = plt.gca()
    ax.xaxis.set_tick_params(rotation=40)
    plt.show()
    
