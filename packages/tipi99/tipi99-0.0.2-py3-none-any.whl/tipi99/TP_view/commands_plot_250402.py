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
from datetime import datetime, timezone, UTC
from time import gmtime, strftime
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import traceback

       
class commands(QtWidgets.QFrame):
    
    # signal_plot_data = QtCore.pyqtSignal(np.ndarray)
    # signal_quit = QtCore.pyqtSignal()
    # signal_plot_absolute = QtCore.pyqtSignal(str)
    
    def __init__(self, model = None, debug = False):
        super().__init__()
        self.model = model
        self.debug = debug
        if self.debug : print('\nTime commands\n')
        
        self.max_width = 400
        self.date_epoch_synch = True #keep synchronisation 
        self.timestamp_t0 = 0
        
        
        #Widget A
        
        self.label_X_scale = QtWidgets.QLabel(self)
        self.label_X_scale.setText(' X Scale')
        
        self.combo_X_scale_type = QtWidgets.QComboBox()
        self.combo_X_scale_type.addItems(['Elapsed (sec)', 'Elapsed (min)', 'Elapsed (hours)', 'Elapsed (days)', 'Date'])
        
        #Widget B
        
        self.combo_edit_scale_type = QtWidgets.QComboBox()
        self.combo_edit_scale_type.addItems(['Date', 'Epoch'])
        
        # self.combo_X_scale_value = QtWidgets.QComboBox()
        # self.combo_X_scale_value.addItems(['seconds', 'minutes', 'hours', 'days'])
        
        
        
        self.time_edit_time0 = QtWidgets.QDateTimeEdit(self, calendarPopup=True)
        self.time_edit_time0.setDisplayFormat("dd/MM/yyyy hh:mm")
        _ = datetime.fromtimestamp(0, UTC)
        #_ = datetime.now()
        self.time_edit_time0.setDate(_)

        
        self.line_edit_epoch0 = QtWidgets.QLineEdit(self, text='0',
        clearButtonEnabled=False)
        self.line_edit_epoch0.hide()
        
        
        self.label_time_conv = QtWidgets.QLabel(self)

        
        self.label_time_conv_value = QtWidgets.QLabel(self)
        self.label_time_conv_value.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        #self.label_time_conv_value.hide()
        
        self.button_set_new_t0 = QtWidgets.QPushButton("Set new starting date")

        
        
        Widget_A = QtWidgets.QWidget()
        Widget_A.setMaximumWidth(self.max_width)
        Widget_A.setObjectName('Widget_A')
        Widget_A.setStyleSheet("#Widget_A {border: 2px solid green; border-radius: 10px;}")
        
        layout_Widget_A = QtWidgets.QGridLayout(Widget_A)
        
        Widget_B = QtWidgets.QWidget()
        Widget_B.setMaximumWidth(self.max_width)
        Widget_B.setObjectName('Widget_B')
        Widget_B.setStyleSheet("#Widget_B {border: 2px solid green; border-radius: 10px;}")
        
        layout_Widget_B = QtWidgets.QGridLayout(Widget_B)
        
        
        
        
        
        #Elapsed
        layout_Widget_A.addWidget(self.label_X_scale, 0, 0)
        layout_Widget_A.addWidget(self.combo_X_scale_type, 0, 1)
        
        #layout_Widget_A.addWidget(self.combo_X_scale_value, 1, 1)
        
        #Abs Widget B

        layout_Widget_B.addWidget(self.combo_edit_scale_type, 0, 0)
        
        layout_Widget_B.addWidget(self.time_edit_time0, 0, 1)
        layout_Widget_B.addWidget(self.line_edit_epoch0, 0, 1)
        
        layout_Widget_B.addWidget(self.label_time_conv, 1, 0)
        layout_Widget_B.addWidget(self.label_time_conv_value, 1, 1)
        
        layout_Widget_B.addWidget(self.button_set_new_t0, 2, 0, 1, 2)
        
        
        
        # group_rel = [self.label_X_scale, self.combo_X_scale_value]
        # group_abs = [self.combo_X_scale_type, self.time_edit_time0, self.line_edit_epoch0, self.label_time_conv, self.label_time_conv_value]
        
        
        
        


        
        #Final layout
        
        layout_controls = QtWidgets.QVBoxLayout()

        layout_controls.addWidget(Widget_A)
        layout_controls.addWidget(Widget_B)

        
        layout_controls.setAlignment(QtCore.Qt.AlignTop)
        layout_controls.addStretch()

        # layout_controls = QtWidgets.QVBoxLayout()
        
        # layout_controls.addWidget(button_Open_csv)
        # layout_controls.addWidget(button_Open_dat)
        # layout_controls.addWidget(button_Open_custom)
        # #layout_controls.addWidget(self.combo)
        
        # layout_controls.addWidget(button_Accept)
        # layout_controls.addWidget(button_Cancel)
        # layout_controls.setAlignment(QtCore.Qt.AlignTop)
        
        self.setLayout(layout_controls)
        
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed)
        
        
        # #self.combo_X_scale_type.view().pressed.connect(self.update_time0)
        self.combo_edit_scale_type.activated[str].connect(self.update_time0)
        # #editingFinished // returnPressed
        

        self.time_edit_time0.dateTimeChanged.connect(self.date_to_epoch)
        self.line_edit_epoch0.textChanged.connect(self.epoch_to_date)
            
        
        
        
        
    
    def update_default_date_epoch(self, timestamp: int):

        self.timestamp_t0 = timestamp
        _ = datetime.fromtimestamp(timestamp, UTC)
        self.time_edit_time0.setDate(_)
        self.line_edit_epoch0.setText(str(timestamp))
        item = self.combo_edit_scale_type.currentText()
        self.update_time0(item)
        
    def date_to_epoch(self):
        try:
            if not self.time_edit_time0.isHidden():
                
                value = self.time_edit_time0.dateTime()
                value_utc = value.toUTC()
                
                value_dt = value.toPyDateTime()
    
                value_utc = int(value_dt.replace(tzinfo=timezone.utc).timestamp())
                self.label_time_conv_value.setText(str(value_utc))
                
                self.timestamp_t0 = value_utc
                
                self.line_edit_epoch0.setText(str(value_utc))
                
        except:
            print(traceback.format_exc())
        
    def epoch_to_date(self):
        try:
            if not self.line_edit_epoch0.isHidden():
                
                value = int(self.line_edit_epoch0.text())
            
                date = datetime.utcfromtimestamp(value) 
                date_str = date.strftime("%d/%m/%Y %H:%M")
                self.label_time_conv_value.setText(date_str)
                
                self.timestamp_t0 = value
                
                self.time_edit_time0.setDate(date)
            
        except:
            print(traceback.format_exc())
            
        
        
    def update_time0(self, item):
        #'Date', 'Epoch'
        if item == 'Date':

            

            self.time_edit_time0.show()
            self.line_edit_epoch0.hide()
            
            self.label_time_conv.setText("Epoch")
            self.label_time_conv.show()
            self.label_time_conv_value.show()
            self.date_to_epoch()
            

            
        elif item == 'Epoch':

            
            #Absolute
            self.line_edit_epoch0.show()
            self.time_edit_time0.hide()
            
            self.label_time_conv.setText("Date")
            self.label_time_conv.show()
            self.label_time_conv_value.show()
            self.epoch_to_date()
            

        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("""
                      * {
                          font-size: 20px;
                    }
                      """)

    window = commands(debug = True)

    window.show()
    sys.exit(app.exec())