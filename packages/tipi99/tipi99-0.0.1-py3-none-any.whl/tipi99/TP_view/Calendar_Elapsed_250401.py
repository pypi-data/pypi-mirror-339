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
from datetime import datetime, timedelta
from PyQt5 import QtWidgets, QtCore, QtGui
import math
import traceback

class pop_up_error(QtWidgets.QMessageBox):
    def __init__(self, text, title = '', debug = False):
        super().__init__()
        
        self.setIcon(QtWidgets.QMessageBox.Critical)
        self.setWindowTitle(title)
        self.resize(800, 500)
        

        # try:
        #     text = self.format_dict(text)
        # except:
        #     text = 'Reading Error'

        self.setText(text)
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)
        
        # self.setSizePolicy(
        #     QtWidgets.QSizePolicy.Fixed,
        #     QtWidgets.QSizePolicy.Fixed)
        
        self.exec()
        
    def format_dict(self, text):
        new_text = str()
        for key, value in text.items():
            new_text += str(key)
            new_text +='\n\t'
            new_text += str(value)
            new_text +='\n'
            
        return new_text
    
class calendar_start_stop(QtWidgets.QFrame):
    
    signal_plot_data = QtCore.pyqtSignal(np.ndarray)
    signal_quit = QtCore.pyqtSignal()
    
    def __init__(self, model = None, debug = False, logs_number = None):
        super().__init__()
        self.model = model
        self.debug = debug
        self.time_format = "%d/%m/%Y"
        self.time_format_long = "%d/%m/%Y %H:%M:%S"
        if self.debug : print('\nopen_file_commands\n')
        
        self.max_width = 400
        
        if logs_number is None:
            self.logs_number = 262144 *1 / 8 - 1 # *1 | 2 mega *2 | 4 mega
        else:
            self.logs_number = logs_number
            
        self.calendar_start = QtWidgets.QCalendarWidget(self)
        self.calendar_start.setFixedSize(QtCore.QSize(400, 300))
        #self.calendar_start.setGeometry(10, 10, 400, 600)
        self.calendar_start.clicked.connect(self.set_start_date)
        
        #date = QtCore.QDate(2021, 1, 1)
        date = datetime.now().date()
        self.calendar_start.setSelectedDate(date)
        
        
        self.calendar_stop = QtWidgets.QCalendarWidget(self)
        self.calendar_stop.setFixedSize(QtCore.QSize(400, 300))
        #self.calendar_stop.setGeometry(10, 10, 400, 250)
        self.calendar_stop.clicked.connect(self.set_stop_date)
        #date = QtCore.QDate(2021, 1, 1)
        
        self.calendar_stop.setSelectedDate(date)
        
        
        #py_date = date.toPyDate()
        self.start_time = np.datetime64(date) +  np.timedelta64(0,'s')
        self.stop_time = np.datetime64(date) +  np.timedelta64(0,'s')
        
        
        self.button_Calc = QtWidgets.QPushButton("Calc")
        self.button_Calc.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        self.button_Calc.setFixedWidth(400)
        self.button_Calc.clicked.connect(self.calc_elapsed)

        
        self.label_elapsed = QtWidgets.QLabel(self)
        self.label_elapsed.setText(f'{int(self.logs_number)} logs, Total time in sec = 0')
        
        self.label_starting_date = QtWidgets.QLabel(self)
        start_str = self.start_time.astype(datetime).strftime(self.time_format_long)
        self.label_starting_date.setText(f'Starting date: {start_str}')
        
        self.label_closest_available = QtWidgets.QLabel(self)
        self.label_closest_available.setText('Closest available samplings:')
        
        self.label_closest_available_higher = QtWidgets.QLabel(self)
        self.label_closest_available_higher.setText(' -- ')
        
        self.label_closest_available_lower = QtWidgets.QLabel(self)
        self.label_closest_available_lower.setText(' -- ')
        
        # self.button_B = QtWidgets.QPushButton("Get Date")
        # self.button_B.clicked.connect(self.print_date)
        
        self.entry_start_hh = QtWidgets.QLineEdit(self, text='00',
        clearButtonEnabled=False)
        self.entry_start_hh.setFixedWidth(30)
        
        self.entry_start_mm = QtWidgets.QLineEdit(self, text='00',
        clearButtonEnabled=False)
        self.entry_start_mm.setFixedWidth(30)
        
        self.entry_start_ss = QtWidgets.QLineEdit(self, text='00',
        clearButtonEnabled=False)
        self.entry_start_ss.setFixedWidth(30)
        
        
        self.entry_stop_hh = QtWidgets.QLineEdit(self, text='00',
        clearButtonEnabled=False)
        self.entry_stop_hh.setFixedWidth(30)
        
        self.entry_stop_mm = QtWidgets.QLineEdit(self, text='00',
        clearButtonEnabled=False)
        self.entry_stop_mm.setFixedWidth(30)
        
        self.entry_stop_ss = QtWidgets.QLineEdit(self, text='00',
        clearButtonEnabled=False)
        self.entry_stop_ss.setFixedWidth(30)
        
        #self.button_C = QtWidgets.QPushButton("Button 3")
        #self.button_C.clicked.connect(self.open_data_File_dat)
        
        
        Widget_A = QtWidgets.QWidget()
        #Widget_A.setMaximumWidth(self.max_width)
        Widget_A.setObjectName('Widget_A')
        Widget_A.setStyleSheet("#Widget_A {border: 2px solid green; border-radius: 10px;}")
        width = 400
        height = 300
        # setting  the fixed size of window
        #Widget_A.setFixedSize(width, height)
        
        Widget_A.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        
        self.tabs = QtWidgets.QTabWidget()
        #self.tabs.setTabPosition(QtWidgets.QTabWidget.West)
        self.tab_1 = self.tabs.addTab(self.calendar_start, "Start")
        self.tab_2 = self.tabs.addTab(self.calendar_stop, "Stop")
        #self.tabs.setTabEnabled(1, False)
        
        self.label_dp00= QtWidgets.QLabel(self)
        self.label_dp00.setText('Start')
        
        self.label_dp01= QtWidgets.QLabel(self)
        self.label_dp01.setText(date.strftime("%d/%m/%Y"))
        

        self.label_dp02= QtWidgets.QLabel(self)
        self.label_dp02.setText(':')

        self.label_dp03= QtWidgets.QLabel(self)
        self.label_dp03.setText(':')
        
        self.label_dp10= QtWidgets.QLabel(self)
        self.label_dp10.setText('Stop')
        
        self.label_dp11= QtWidgets.QLabel(self)
        self.label_dp11.setText(date.strftime("%d/%m/%Y"))
        
        self.label_dp12= QtWidgets.QLabel(self)
        self.label_dp12.setText(':')

        self.label_dp13= QtWidgets.QLabel(self)
        self.label_dp13.setText(':')
        
        #layout_controls = QtWidgets.QVBoxLayout(Widget_A)
        
        layout_start_date = QtWidgets.QHBoxLayout()
        layout_start_date.addWidget(self.label_dp00)
        layout_start_date.addWidget(self.label_dp01)
        layout_start_date.addWidget(self.entry_start_hh)
        layout_start_date.addWidget(self.label_dp02)
        layout_start_date.addWidget(self.entry_start_mm)
        layout_start_date.addWidget(self.label_dp03)
        layout_start_date.addWidget(self.entry_start_ss)
        layout_start_date.addStretch()#
        
        layout_stop_date = QtWidgets.QHBoxLayout()
        layout_stop_date.addWidget(self.label_dp10)
        layout_stop_date.addWidget(self.label_dp11)
        layout_stop_date.addWidget(self.entry_stop_hh)
        layout_stop_date.addWidget(self.label_dp12)
        layout_stop_date.addWidget(self.entry_stop_mm)
        layout_stop_date.addWidget(self.label_dp13)
        layout_stop_date.addWidget(self.entry_stop_ss)
        layout_stop_date.addStretch()#

        #layout_start_date.setAlignment(QtCore.Qt.AlignLeft)
        
        layout_Open = QtWidgets.QGridLayout()
        layout_Open.addWidget(self.tabs, 0, 1)
        #layout_Open.addWidget(self.button_C, 1, 1)
        #layout_Open.setColumnStretch(0, 1)
        
        layout_inline = QtWidgets.QVBoxLayout(Widget_A)
        layout_inline.addLayout(layout_Open)
        layout_inline.addLayout(layout_start_date)
        layout_inline.addLayout(layout_stop_date)
        layout_inline.addWidget(self.button_Calc)
        layout_inline.addWidget(self.label_starting_date)
        layout_inline.addWidget(self.label_elapsed)
        layout_inline.addWidget(self.label_closest_available)
        layout_inline.addWidget(self.label_closest_available_lower)
        layout_inline.addWidget(self.label_closest_available_higher)
        layout_inline.setAlignment(QtCore.Qt.AlignLeft)
        layout_inline.addStretch()
        
        # #Final layout
        
        layout_controls = QtWidgets.QVBoxLayout()
        layout_controls.addWidget(Widget_A)

        
        # layout_controls.setAlignment(QtCore.Qt.AlignTop)
        # layout_controls.setAlignment(QtCore.Qt.AlignLeft)
        
        
        
        layout_controls.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(layout_controls)
        
        #self.setLayout(layout_inline)
        
        # self.setSizePolicy(
        #     QtWidgets.QSizePolicy.Fixed,
        #     QtWidgets.QSizePolicy.Fixed)
    
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
    
    def calc_elapsed(self):
        self.set_start_date()
        self.set_stop_date()
        total_seconds = (self.stop_time - self.start_time).astype(dtype='timedelta64[s]').astype('int')
        loop_duration_UP = math.ceil(total_seconds / self.logs_number)
        loop_duration_DOWN = math.floor(total_seconds / self.logs_number)
        self.label_elapsed.setText(f'{int(self.logs_number)} logs, Total duration {self.TM_s_string(total_seconds)}')
        OFF_UP = self.start_time.astype(datetime) + timedelta(seconds=loop_duration_UP*self.logs_number)
        OFF_DOWN = self.start_time.astype(datetime) + timedelta(seconds=loop_duration_DOWN*self.logs_number)
        
        OFF_UP = OFF_UP.strftime(self.time_format_long)
        OFF_DOWN = OFF_DOWN.strftime(self.time_format_long)
        
        start_str = self.start_time.astype(datetime).strftime(self.time_format_long)
        self.label_starting_date.setText(f'Starting date: {start_str}')
        self.label_closest_available_lower.setText(f'log time = {loop_duration_DOWN} sec, End: {OFF_DOWN}')
        self.label_closest_available_higher.setText(f'log time = {loop_duration_UP} sec, End: {OFF_UP}')
        
    def set_start_date(self):
        value = self.calendar_start.selectedDate()
        py_date = value.toPyDate ()
        try:
            ss = np.int32(self.entry_start_ss.text())
            mm = np.int32(self.entry_start_mm.text())
            hh = np.int32(self.entry_start_hh.text())
            self.start_time = np.datetime64(py_date) + ss.astype("timedelta64[s]") + mm.astype("timedelta64[m]") + hh.astype("timedelta64[h]")
            self.label_dp01.setText(py_date.strftime("%d/%m/%Y"))
            _str = self.start_time.astype(datetime).strftime("%H%M%S")
            self.entry_start_hh.setText(_str[0:2])
            self.entry_start_mm.setText(_str[2:4])
            self.entry_start_ss.setText(_str[4:6])
        except:
            pop_up_error("Invalid input, must be integer", 'Entry Error')
        
    
    def set_stop_date(self):
        value = self.calendar_stop.selectedDate()
        py_date = value.toPyDate ()
        try:
            ss = np.int32(self.entry_stop_ss.text())
            mm = np.int32(self.entry_stop_mm.text())
            hh = np.int32(self.entry_stop_hh.text())
            self.stop_time = np.datetime64(py_date) + ss.astype("timedelta64[s]") + mm.astype("timedelta64[m]") + hh.astype("timedelta64[h]")
            self.label_dp11.setText(py_date.strftime("%d/%m/%Y"))
            _str = self.stop_time.astype(datetime).strftime("%H%M%S")
            self.entry_stop_hh.setText(_str[0:2])
            self.entry_stop_mm.setText(_str[2:4])
            self.entry_stop_ss.setText(_str[4:6])
        except:
            pop_up_error("Invalid input, must be integer", 'Entry Error')
        
        
    def print_date(self):
        value = self.calendar_stop.selectedDate()
        py_date = value.toPyDate ()
        py_dt = datetime.combine(py_date, datetime.min.time())
        print(py_date)
        print(py_dt)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("""
                      * {
                          font-size: 15px;
                    }
                      """)
    
    window = calendar_start_stop()

    window.show()
    sys.exit(app.exec())

