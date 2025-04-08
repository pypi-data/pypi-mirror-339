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
from matplotlib.backend_bases import MouseEvent

import os, sys
from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar



       
class commands(QtWidgets.QFrame):
    
    signal_plot_data = QtCore.pyqtSignal(np.ndarray)
    signal_quit = QtCore.pyqtSignal()
    
    def __init__(self, model = None, debug = False):
        super().__init__()
        self.model = model
        self.debug = debug
        if self.debug : print('\nopen_file_commands\n')
        
        self.max_width = 400
        
        self.label_Alert_0 = QtWidgets.QLabel(self)
        self.label_Alert_0.setText('1) FIRST: Start "Search TP99"')
        self.label_Alert_0.setStyleSheet("color: red; font-weight: bold")
        #self.label_Alert_0.setStyleSheet("background-color: red; font-weight: bold") #; color: yellow ; font-weight: bold
        
        self.label_Alert_1 = QtWidgets.QLabel(self)
        self.label_Alert_1.setText('2) SECOND: Connect TP99 by USB cable\n')
        self.label_Alert_1.setStyleSheet("color: red")
        
        self.button_list_COM = QtWidgets.QPushButton("Update Port List")
        #self.button_A.clicked.connect(self.model.check_ports)
        
        self.combobox_list_COM_known = QtWidgets.QComboBox()
        
        self.button_Connect = QtWidgets.QPushButton(" Search TP99 ")
        
        self.label_Connect = QtWidgets.QLabel(self)
        self.label_Connect.setText(' ... ')
        
        #self.combobox_list_COM_list = QtWidgets.QComboBox()
        
        self.button_test_TP = QtWidgets.QPushButton("Test Detector (T P)")
        #self.button_C.clicked.connect(self.open_data_File_dat)
        self.button_test_TP.setDisabled(True)
        
        self.button_test_LED = QtWidgets.QPushButton("Test LED: Turn ON")
        #self.button_C.clicked.connect(self.open_data_File_dat)
        self.button_test_LED.setDisabled(True)
        
        self.label_test_TP = QtWidgets.QLabel(self)
        self.label_test_TP.setText(' ... ')
        
        self.button_set_name = QtWidgets.QPushButton("Set Name")
        #self.button_C.clicked.connect(self.open_data_File_dat)
        self.button_set_name.setDisabled(True)
        
        self.entry_set_name = QtWidgets.QLineEdit(self, placeholderText='---')
        self.entry_set_name.setMaxLength(8)
        
        # self.entry_set_name = QtWidgets.QLineEdit(self, placeholderText=f'XIAO',
        # clearButtonEnabled=True)
        
        self.label_set_name = QtWidgets.QLabel(self)
        self.label_set_name.setText('Device name = ---')
        
        # self.label_set_name = QtWidgets.QLabel(self)
        # self.label_set_name.setText('Old Name ')
        
        Widget_A = QtWidgets.QWidget()
        Widget_A.setMaximumWidth(self.max_width)
        Widget_A.setObjectName('Widget_A')
        Widget_A.setStyleSheet("#Widget_A {border: 2px solid green; border-radius: 10px;}")
        
        layout_Open = QtWidgets.QGridLayout(Widget_A)
        

        layout_Open.addWidget(self.label_Alert_0, 0, 0, 1, 2)
        layout_Open.addWidget(self.label_Alert_1, 1, 0, 1, 2)
        layout_Open.addWidget(self.button_Connect, 2, 0)
        layout_Open.addWidget(self.label_Connect, 2, 1)
        layout_Open.addWidget(self.button_test_TP, 3, 0)
        layout_Open.addWidget(self.label_test_TP, 3, 1)
        layout_Open.addWidget(self.button_test_LED, 4, 0, 1, 2)
        layout_Open.addWidget(self.button_list_COM, 5, 0)
        layout_Open.addWidget(self.combobox_list_COM_known, 5, 1)

        # layout_Open.addWidget(self.button_set_name, 3, 0)
        # layout_Open.addWidget(self.entry_set_name, 4, 0)
        # layout_Open.addWidget(self.label_set_name, 4, 1)
        
        
        
        
        self.button_set_time = QtWidgets.QPushButton("Set log time in sec")
        self.button_set_time.setDisabled(True)
        
        # self.entry_set_time = QtWidgets.QLineEdit(self, placeholderText='10',
        # clearButtonEnabled=True)
        
        self.entry_set_time = QtWidgets.QLineEdit(self, placeholderText='---')
        
        # self.label_set_time = QtWidgets.QLabel(self)
        # self.label_set_time.setText('Old Time ')
        
        # self.label_day = QtWidgets.QLabel(self)
        # self.label_day.setText(' day ')
        
        # self.entry_day = QtWidgets.QLineEdit(self, placeholderText=f'{str(self.model.delta_day)}',
        # clearButtonEnabled=False)
        
        # self.label_h = QtWidgets.QLabel(self)
        # self.label_h.setText(' h ')
        
        # self.entry_h = QtWidgets.QLineEdit(self, placeholderText=f'{str(self.model.delta_h)}',
        # clearButtonEnabled=False)
        
        # self.label_min = QtWidgets.QLabel(self)
        # self.label_min.setText(' min')
        
        # self.entry_min = QtWidgets.QLineEdit(self, placeholderText=f'{str(self.model.delta_min)}',
        # clearButtonEnabled=False)
        
        # self.label_sec = QtWidgets.QLabel(self)
        # self.label_sec.setText(' sec ')
        
        # self.entry_sec = QtWidgets.QLineEdit(self, placeholderText=f'{str(self.model.delta_sec)}',
        # clearButtonEnabled=False)
        
        # self.label_max_duration = QtWidgets.QLabel(self)
        # self.label_max_duration.setText('Ma')
        
        self.button_battery_date = QtWidgets.QPushButton("Set battery date")
        self.button_battery_date.setDisabled(True)
        
        
        self.entry_battery_date = QtWidgets.QDateTimeEdit(self, calendarPopup=True)
        self.entry_battery_date.setDisplayFormat("dd/MM/yyyy hh:mm")
        self.entry_battery_date.setDate(datetime.now())
        
        self.label_battery_date = QtWidgets.QLabel(self)
        self.label_battery_date.setText('Battery installed ---')
        
        # self.entry_battery_date = QtWidgets.QLineEdit(self, placeholderText='ddmmyy',
        # clearButtonEnabled=True)
        
        
        # self.label_battery_date = QtWidgets.QLabel(self)
        # self.label_battery_date.setText('070524')
        
        self.label_ETA = QtWidgets.QLabel(self)
        self.label_ETA.setText('--- sec, ETA: ---')
        
        
        Widget_B = QtWidgets.QWidget()
        Widget_B.setMaximumWidth(self.max_width)
        Widget_B.setObjectName('Widget_B')
        Widget_B.setStyleSheet("#Widget_B {border: 2px solid green; border-radius: 10px;}")
        
        layout_Time = QtWidgets.QGridLayout(Widget_B)
        
        layout_Time.addWidget(self.entry_set_name, 0, 0)
        layout_Time.addWidget(self.button_set_name, 0, 1)
        layout_Time.addWidget(self.label_set_name, 1, 0, 1, 2)
        
        #layout_Time.addWidget(self.label_set_name, 1, 1)
        
        
        layout_Time.addWidget(self.entry_set_time, 2, 0)
        layout_Time.addWidget(self.button_set_time, 2, 1)
        
        #layout_Time.addWidget(self.label_set_time, 3, 1)
        # layout_Time.addWidget(self.label_day, 1, 0)
        # layout_Time.addWidget(self.label_h, 1, 2)
        # layout_Time.addWidget(self.label_min, 1, 4)
        # layout_Time.addWidget(self.label_sec, 1, 6)
        
        # layout_Time.addWidget(self.entry_day, 1, 1)
        # layout_Time.addWidget(self.entry_h, 1, 3)
        # layout_Time.addWidget(self.entry_min, 1, 5)
        # layout_Time.addWidget(self.entry_sec, 1, 7)
        
        layout_Time.addWidget(self.label_ETA, 3, 0, 1, 2)
        
        layout_Time.addWidget(self.entry_battery_date, 4, 0)
        layout_Time.addWidget(self.button_battery_date, 4, 1)
        layout_Time.addWidget(self.label_battery_date, 5, 0, 1, 2)
        
        #layout_Time.addWidget(self.label_battery_date, 6, 1)
        
        
        self.button_load_data = QtWidgets.QPushButton("Download Device Memory")
        self.button_load_data.setDisabled(True)
        
        self.pbar_load = QtWidgets.QProgressBar(self)
        self.pbar_load.setValue(100)
        self.pbar_load.setDisabled(True)
        
        self.button_save_data = QtWidgets.QPushButton("Save Data")
        self.button_save_data.setDisabled(True)
        
        self.button_erase_data = QtWidgets.QPushButton("Erase Device Memory")
        self.button_erase_data.setDisabled(True)
        
        Widget_C = QtWidgets.QWidget()
        Widget_C.setMaximumWidth(self.max_width)
        Widget_C.setObjectName('Widget_B')
        Widget_C.setStyleSheet("#Widget_B {border: 2px solid green; border-radius: 10px;}")
        
        layout_Data = QtWidgets.QGridLayout(Widget_C)
        layout_Data.addWidget(self.button_load_data, 0, 0)
        layout_Data.addWidget(self.pbar_load, 1, 0, 1, 2)
        layout_Data.addWidget(self.button_save_data, 0, 1)
        layout_Data.addWidget(self.button_erase_data, 2, 0)
        
        #Final layout
        
        layout_controls = QtWidgets.QVBoxLayout()

        layout_controls.addWidget(Widget_A)
        layout_controls.addWidget(Widget_B)
        layout_controls.addWidget(Widget_C)
        
        layout_controls.setAlignment(QtCore.Qt.AlignTop)
        # layout_controls = QtWidgets.QVBoxLayout()
        
        # layout_controls.addWidget(button_Open_csv)
        # layout_controls.addWidget(button_Open_dat)
        # layout_controls.addWidget(button_Open_custom)
        # #layout_controls.addWidget(self.combo)
        
        # layout_controls.addWidget(button_Accept)
        # layout_controls.addWidget(button_Cancel)
        # layout_controls.setAlignment(QtCore.Qt.AlignTop)
        
        self.setLayout(layout_controls)
        
        # self.setSizePolicy(
        #     QtWidgets.QSizePolicy.Fixed,
        #     QtWidgets.QSizePolicy.Fixed)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("""
                      * {
                          font-size: 15px;
                    }
                      """)

    window = commands()

    window.show()
    sys.exit(app.exec())