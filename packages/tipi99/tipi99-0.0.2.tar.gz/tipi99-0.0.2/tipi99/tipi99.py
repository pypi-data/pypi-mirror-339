# -*- coding: utf-8 -*-
"""

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

import configparser as cp
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import os, sys
from datetime import datetime, timezone
from PyQt5 import QtWidgets, QtCore, QtGui
import traceback
from time import sleep

#https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
import os, sys
script = os.path.abspath(__file__)
script_dir = os.path.dirname(script)
sys.path.append(script_dir)

from TP_view.about_250225 import about
from TP_view.Calendar_Elapsed_250401 import calendar_start_stop
from TP_view.commands_250401 import commands
from TP_view.pop_up_241029 import pop_up, pop_up_error
from TP_view.table_250401 import Data_Table
from TP_view.commands_plot_250402 import commands as commands_plot
from TP_view.Frame_1_graph_241118 import Frame_1_graph
from TP_view.Frame_1_graph_2_axis_250402 import Frame_1_graph_2_ax

from TP_model.TP_model_core_250225 import my_model as model

debug = False

if debug:
    script_name = os.path.basename(script)
    now = datetime.now()
    date = now.isoformat(sep = ' ', timespec = 'seconds')
    date_short = date[2:].replace('-','').replace(' ','_').replace(':','') #example = '240327_141721'
    print("File folder = " + script_dir)
    print("File name = " + script_name)
    print("Current working directory (AKA Called from ...) = " + os.getcwd())
    print("Python version = " + sys.version)
    print("Python folder = " + sys.executable)
    print()
    print("Started @ " + date +' AKA ' + date_short)

 
        
class TiPi99(QtWidgets.QMainWindow):
    
    my_Serial_Thread_Open_start = QtCore.pyqtSignal()
    my_Serial_Thread_Read_start = QtCore.pyqtSignal()
    my_Serial_Thread_Reset_start = QtCore.pyqtSignal()
    
    def __init__(self, debug = False):
        super().__init__()
        self.__version__ = '0.0.1' 
        self.__release__ = '250407'
        
        self.about = about('TiPi99', self.__version__, self.__release__)
        self.font_size = 15
        self.plot_font_big_size = 17
        self.use_plot_size = False
        
        self.update_font_size()
        
        self.built_in_styles = QtWidgets.QStyleFactory.keys()
        self.window_Title = 'TiPi99'
        self.setWindowTitle(self.window_Title)
        #self.resize(500, 500)
        self.debug = debug
        self.model = model(self.debug)
        self.model.mySerial.set_FRAM_memory_size(4)  #2 = 2 Mega, 4 = 4 Mega
        
        show_tabs = True
        
        if self.use_plot_size:
            label_big = self.plot_font_big_size
            label_medium = label_big - 2
            label_small = label_medium - 2
            
            plt.rcParams["font.size"] = label_big
            
            plt.rc('font', size=label_small)          # controls default text sizes
            plt.rc('axes', labelsize=label_medium)    # fontsize of the x and y labels
            plt.rc('xtick', labelsize=label_small)    # fontsize of the tick labels
            plt.rc('ytick', labelsize=label_small)    # fontsize of the tick labels
            plt.rc('legend', fontsize=label_small)    # legend fontsize
            plt.rc('figure', titlesize=label_big)     # fontsize of the figure title

        
        # self.Tab_Neon_Data =  Tab_2(Data_Commands, Data_Table)
        # self.Tab_Single =  Tab_2(Fig_Commands, Frame_1_graph)
        # self.Tab_Double =  Tab_2(Fig_2_Commands, Frame_2_graph_h)
        
        #self.Tab_Neon_Data =  Tab_Neon_Data(self.model)
        #self.Tab_Fine =  Tab_Fine_Calib(self.model)
        #self.Tab_Double =  Tab_Double(self.model)
        
        
        self.commands_serial = commands(self.model)
        #self.commands_2 = commands(self.model)
        self.data_PT = Data_Table(self.model, self.debug)
        self.figure_T = Frame_1_graph(self.model, self.debug)
        self.figure_P = Frame_1_graph(self.model, self.debug)
        self.figure_TP = Frame_1_graph_2_ax(self.model, self.debug)
        
        self.calendar_start_stop = calendar_start_stop(logs_number = self.model.mySerial.logs_number)
        
        self.figure_T.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.figure_P.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.figure_TP.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        self.commands_figure_T = commands_plot()
        self.set_axis_labels()
        
        self.layout_plot_T = QtWidgets.QHBoxLayout ()
        
        a = QtWidgets.QVBoxLayout()
        a.addWidget(self.commands_figure_T)
        a.setAlignment(QtCore.Qt.AlignTop)
        
        b = QtWidgets.QVBoxLayout()
        b.addWidget(self.figure_T)
        b.setAlignment(QtCore.Qt.AlignTop) 
        
        self.layout_plot_T.addLayout(a)
        self.layout_plot_T.addLayout(b)
        
        self.widget_plot_T = QtWidgets.QWidget()
        self.widget_plot_T.setLayout(self.layout_plot_T)
        
        if show_tabs:
            tabs = QtWidgets.QTabWidget()
            #tabs.setTabPosition(QtWidgets.QTabWidget.West) ToDo Orientation
            
            self.tab_1 = tabs.addTab(self.commands_serial, "Serial")
            self.tab_2 = tabs.addTab(self.calendar_start_stop, "Calc")
            self.tab_3 = tabs.addTab(self.data_PT, "Data")
            self.tab_4 = tabs.addTab(self.widget_plot_T, "Plot T")
            self.tab_5 = tabs.addTab(self.figure_P, "Plot P")
            self.tab_6 = tabs.addTab(self.figure_TP, "Plot TP")
            #tabs.setTabEnabled(2, False)

        #Buttons Connection
        
        self.commands_serial.button_list_COM.clicked.connect(self.list_COM)
        #self.commands_serial.button_erase_data.clicked.connect(self.erase_data)
        #self.commands_serial.button_load_data.clicked.connect(self.load_data)
        #self.commands_serial.combobox_list_COM.view().pressed.connect(self.COM_info)
        self.commands_serial.combobox_list_COM_known.activated.connect(self.COM_info)
        self.commands_serial.button_test_TP.clicked.connect(self.test_connection)
        self.commands_serial.button_test_LED.clicked.connect(self.test_LED)
        self.commands_serial.button_save_data.clicked.connect(self.save_data)
        
        self.commands_serial.button_set_time.clicked.connect(self.set_log_time)
        self.commands_serial.button_battery_date.clicked.connect(self.set_battery_date)
        self.commands_serial.button_set_name.clicked.connect(self.set_device_name)
        #Thread Section
        
            #Button_Thread_A) Connect main launcher (i.e. start button) to Main Start method 
        self.commands_serial.button_Connect.clicked.connect(self.start_my_Serial_Thread_Open)
        
            #Button_Thread_B) Connect main launcher (i.e. start button) to Main Start method 
        self.commands_serial.button_load_data.clicked.connect(self.start_my_Serial_Thread_Read)
        
            #Button_Thread_C) Connect main launcher (i.e. start button) to Main Start method 
        self.commands_serial.button_erase_data.clicked.connect(self.start_my_Serial_Thread_Reset)

        #Thread A Search TP99 COM port and connect
        
        self.my_Serial_Thread_Open = self.model.my_Serial_Thread_Open                   #Thread_1A) Create Thread
        self.my_Serial_Thread_Open.searching.connect(self.my_Serial_Thread_Open_status) #Thread_2A) Connect Thread Status Signal to action in main (i.e. update status bar)
        self.my_Serial_Thread_Open_start.connect(self.my_Serial_Thread_Open.start)      #Thread_3A) Connect main launcher signal (i.e. in start button) to Thread Start process 
        
        #Thread B Read data from TP99 FRAM
        
        self.my_Serial_Thread_Read = self.model.my_Serial_Thread_Read                   #Thread_1B) Create Thread
        self.my_Serial_Thread_Read.reading.connect(self.my_Serial_Thread_Read_status)   #Thread_2B) Connect Thread Status Signal to action in main (i.e. update status bar)
        self.my_Serial_Thread_Read_start.connect(self.my_Serial_Thread_Read.start)      #Thread_3B) Connect main launcher signal (i.e. in start button) to Thread Start process 
        
        #Thread C Delete data in TP99 FRAM (write to 0)
        
        self.my_Serial_Thread_Reset = self.model.my_Serial_Thread_Reset                   #Thread_1C) Create Thread
        self.my_Serial_Thread_Reset.erasing.connect(self.my_Serial_Thread_Reset_status)   #Thread_2C) Connect Thread Status Signal to action in main (i.e. update status bar)
        self.my_Serial_Thread_Reset_start.connect(self.my_Serial_Thread_Reset.start)      #Thread_3C) Connect main launcher signal (i.e. in start button) to Thread Start process 
        
        
        #Thread move to main
        self.main_thread = QtCore.QThread()                                            #Thread_4) Create main Thread, only 1 Time 
        
        self.my_Serial_Thread_Open.moveToThread(self.main_thread)                      #Thread_5A) Move every Thread to Main Thread
        self.my_Serial_Thread_Read.moveToThread(self.main_thread)                      #Thread_5B) Move every Thread to Main Thread
        self.my_Serial_Thread_Reset.moveToThread(self.main_thread)                     #Thread_5C) Move every Thread to Main Thread
        
        self.main_thread.start()                                                       #Thread_6) Start Main Thread, only 1 Time
        
        self.commands_figure_T.combo_X_scale_type.currentTextChanged.connect(self.update_all_graphs)
        
        
        #self.commands_figure_T.combo_X_scale_type.currentIndexChanged.connect(self.return_to_elapsed)
        
        #Signal Slot Connection
        
        # self.open_file = of.open_file(self.model)
        # self.open_file.commands.signal_selected_data.connect(self.open_file_commands)
        # self.open_file.commands.signal_selected_data.connect(self.Tab_Single.Right.plot_data)
        # self.open_file.commands.signal_selected_data.connect(self.Tab_Double.Right.Fig_B.plot_data)
        # self.open_file.commands.signal_selected_data.connect(self.data_to_model) #Data from Open File to Model
        # self.open_file.commands.signal_selected_data.connect(self.onclick_button_RESET)
        
        self.commands_figure_T.button_set_new_t0.clicked.connect(self.update_timestamp)

        #self.commands_figure_T.signal_plot_absolute.connect(self.update_all_graphs_abs)
        
        #self.commands_figure_T.combo_X_scale_type.currentTextChanged.connect()
        
            
        if show_tabs:
            self.setCentralWidget(tabs)
        else:
            self.setCentralWidget(self.commands_serial)
        self.init_Actions()
        self.init_Menu()
        self.init_Statusbar()
        self.model.statusbar_message(f'Init {__file__}')
        
        self._counter_1 = 0
    
    def set_device_name(self):
        string_name = self.commands_serial.entry_set_name.text()
        string_name = string_name.ljust(8)
        
        if self.debug: print('Name: |' + string_name + '|')
        
        x1 = sum(ord(string_name[0:4][byte])<<8*(3-byte) for byte in range(4))
        x2 = sum(ord(string_name[4:8][byte])<<8*(3-byte) for byte in range(4))  

        self.model.mySerial.set_name1(x1)

        self.model.mySerial.set_name2(x2)
        
        # #timestamp = int(self.commands_serial.entry_battery_date.dateTime().toUTC().toPyDateTime().replace(tzinfo=timezone.utc).timestamp())
        # timestamp = int(self.commands_serial.entry_battery_date.dateTime().toPyDateTime().replace(tzinfo=timezone.utc).timestamp())
        # self.model.mySerial.set_battery_timestamp(timestamp)

        self.get_device_name()
    
    def get_device_name(self):
        
        x1 = self.model.mySerial.get_name1()
        x2 = self.model.mySerial.get_name2()
        
        string_1 = ''.join(chr((x1>>8*(3-byte)) & 0xFF) for byte in range(4))
        string_2 = ''.join(chr((x2>>8*(3-byte)) & 0xFF) for byte in range(4))
        string = 'Device name = ' + string_1 + string_2
        self.device_name = string_1 + string_2
        self.commands_serial.label_set_name.setText(string)

    def set_battery_date(self):
        
        #timestamp = int(self.commands_serial.entry_battery_date.dateTime().toUTC().toPyDateTime().replace(tzinfo=timezone.utc).timestamp())
        timestamp = int(self.commands_serial.entry_battery_date.dateTime().toPyDateTime().replace(tzinfo=timezone.utc).timestamp())
        self.model.mySerial.set_battery_timestamp(timestamp)
        self.get_battery_date()
    
    def get_battery_date(self):
        timestamp = self.model.mySerial.get_battery_timestamp()
        date = datetime.fromtimestamp(timestamp, timezone.utc)
        self.commands_serial.label_battery_date.setText('Battery installed ' + date.strftime("%d/%m/%Y %H:%M"))
        self.commands_serial.entry_battery_date.setDate(date)
        
    # def return_to_elapsed(self):
    #     scale_type = self.commands_figure_T.combo_X_scale_type.currentText() 
        
    #     if scale_type == 'Elapsed':
    #         self.update_all_graphs()
        
    def update_timestamp(self):
        if self.debug: print(self.commands_figure_T.timestamp_t0)
        self.model.statusbar_message('Starting Date Update')
        sleep(.5)
        self.data_PT.timestamp_t0 = self.commands_figure_T.timestamp_t0
        self.data_PT.update_timestamp(int(self.data_PT.timestamp_t0))                   #MEMO: int ot numpy.int32 gives conversion error
        sleep(.5)
        self.update_all_graphs()
        
        self.model.statusbar_message('Date Update Done')
        
    def set_log_time(self):
        
        entry = self.commands_serial.entry_set_time.text()
        try :
            value = int(entry)
            self.model.mySerial.set_log_time(value)
            if self.debug:
                print(self.model.mySerial.logger_loop_wait_time)
        except:
            pop_up_error("Invalid input, must be integer", 'Entry Error')
            
        actual_log_time = str(self.model.mySerial.logger_loop_wait_time)
        self.commands_serial.entry_set_time.setText(actual_log_time)
        ETA = self.model.time.TM_s_string( self.model.mySerial.logs_number * self.model.mySerial.logger_loop_wait_time )
        self.commands_serial.label_ETA.setText(actual_log_time + ' sec, Total duration ' + ETA)
            
    def save_data(self):
        if self.debug:
            print('save data')
            
        seconds = self.model.mySerial.seconds
        if seconds is not None:
            temperature = self.model.mySerial.temperature
            pressure = self.model.mySerial.pressure
            timestamp = self.data_PT.timestamp
            date = self.data_PT.date
            
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Select File")
            if filename != '':
                f = Path(filename)
                self.filename = f
                
                if self.debug:
                    print(self.filename)
                    
                    
                    
                np.savetxt(f.with_suffix('.txt'), np.transpose([seconds, temperature, pressure, timestamp, date]), fmt='%s')
                #np.savetxt(f'{filename}_full.txt', np.transpose([seconds, temperature, pressure, np_time]), fmt='%s', delimiter = ";")
                np.savetxt(f.with_suffix('.csv'), np.transpose([seconds, temperature, pressure, timestamp, date]), fmt='%s', delimiter = ",", header = 'seconds, temperature, pressure, timestamp, date')
                np.save(f.with_suffix('.npy'), np.transpose([seconds, temperature, pressure, timestamp, date]))
                # with open(f.with_suffix('.npy'), 'wb') as f:
                #     np.save(f, seconds)
                #     np.save(f, temperature)
                #     np.save(f, pressure)
                self.model.statusbar_message('Data Saved')
            else:
                self.model.statusbar_message(f'Data Save Cancelled')
        else:
            pop_up_error("No data loaded", 'SaveError')
            self.model.statusbar_message(f'Save Error')
        
    def my_Serial_Thread_Reset_status(self, status):
        #Thread_2C) Connect Thread Status Signal to action in main (i.e. update status bar)
        if self.debug: print(f'Reset : {status:.1f}')
        self.model.statusbar_message(f'Deleting {status:.1f} %')
        self.commands_serial.pbar_load.setValue(int(status))
    
    def set_axis_labels(self):
        _temp = 'Temperature (°C)'
        _time = 'Elapsed Time (sec)'
        _pres = 'Pressure (bar)'
        
        scale = self.commands_figure_T.combo_X_scale_type.currentText() 
        #'Elapsed (sec)', 'Elapsed (min)', 'Elapsed (hours)', 'Elapsed (days)', 'Date'
        
        if scale[:7] == 'Elapsed':
            
            #scale = self.commands_figure_T.combo_X_scale_value.currentText() #['seconds', 'minutes', 'hours', 'days']
            if scale[8:] == '(sec)':
                _time = 'Elapsed Time (sec)'
            elif scale[8:] == '(min)':
                _time = 'Elapsed Time (min)'
            elif scale[8:] == '(hours)':
                _time = 'Elapsed Time (h)'
            elif scale[8:] == '(days)':
                _time = 'Elapsed Time (day)'
        else:
            _time = 'Time (date)'
            
        self.figure_T.ax.set_xlabel(_time)
        self.figure_T.ax.set_ylabel(_temp)
        self.figure_T.fig.tight_layout()
        self.figure_T.canvas.draw()
        
        self.figure_P.ax.set_xlabel(_time)
        self.figure_P.ax.set_ylabel(_pres)
        self.figure_P.fig.tight_layout()
        self.figure_P.canvas.draw()
        
        self.figure_TP.ax1.set_xlabel(_time)
        self.figure_TP.ax1.set_ylabel(_temp, color = self.figure_TP.ax1_color)
        self.figure_TP.ax2.set_ylabel(_pres, color = self.figure_TP.ax2_color)
        self.figure_TP.ax2.yaxis.set_label_position("right")
        self.figure_TP.fig.tight_layout()
        self.figure_TP.canvas.draw()
        
        
        if self.debug:
            print(f'Set axis labels, x = {_time}')
        
    def update_all_graphs_abs(self, status):
        if self.debug: print(status)
        # scale = self.commands_figure_T.combo_X_scale_value.currentText() #['seconds', 'minutes', 'hours', 'days']
        # # rel_abs = self.commands_figure_T.button_rel_abs.text() 
        # if rel_abs == "Absolute":
        #     self.data_PT.set_timestamp(0,0)
        #     x_scale = self.data_PT.date
        # else:

        #     if scale == 'seconds':
        #         x_scale = self.data_PT.data_2D[:,0]
        #     elif scale == 'minutes':
        #         x_scale = self.data_PT.data_2D[:,0]/60
        #     elif scale == 'hours':
        #         x_scale = self.data_PT.data_2D[:,0]/60/60
        #     elif scale == 'days':
        #         x_scale = self.data_PT.data_2D[:,0]/60/60/24
        
        self.data_PT.set_timestamp_date(0,0) #Create Timestamp and Date column

        x_scale = self.data_PT.date
        self.figure_T.ax.xaxis.set_tick_params(rotation=40)
        self.figure_P.ax.xaxis.set_tick_params(rotation=40)
        self.figure_TP.ax1.xaxis.set_tick_params(rotation=40)

        self.figure_T.plot_data(x_scale, self.data_PT.data_2D[:,1])
        self.figure_P.plot_data(x_scale, self.data_PT.data_2D[:,2])
        self.figure_TP.plot_data_ax1(x_scale, self.data_PT.data_2D[:,1])
        self.figure_TP.plot_data_ax2(x_scale, self.data_PT.data_2D[:,2])
        self.set_axis_labels()
    
    def update_all_graphs(self):
        try:
            if self.debug: print('update_all_graphs')
            scale = self.commands_figure_T.combo_X_scale_type.currentText() 
            #'Elapsed (sec)', 'Elapsed (min)', 'Elapsed (hours)', 'Elapsed (days)', 'Date'
            if scale[:7] == 'Elapsed':
                

                self.figure_T.ax.xaxis.set_tick_params(rotation=0)
                self.figure_P.ax.xaxis.set_tick_params(rotation=0)
                self.figure_TP.ax1.xaxis.set_tick_params(rotation=0)
                
                
                
                if scale[8:] == '(sec)':
                    x_scale = self.data_PT.data_2D[:,0]
                elif scale[8:] == '(min)':
                    x_scale = self.data_PT.data_2D[:,0]/60
                elif scale[8:] == '(hours)':
                    x_scale = self.data_PT.data_2D[:,0]/60/60
                elif scale[8:] == '(days)':
                    x_scale = self.data_PT.data_2D[:,0]/60/60/24
            else:
                x_scale = self.data_PT.date
                
                self.figure_T.ax.xaxis.set_tick_params(rotation=40)
                self.figure_P.ax.xaxis.set_tick_params(rotation=40)
                self.figure_TP.ax1.xaxis.set_tick_params(rotation=40)
        
            if self.debug: print('x : ', x_scale)
            
            self.figure_T.plot_data(x_scale, self.data_PT.data_2D[:,1])
            self.figure_P.plot_data(x_scale, self.data_PT.data_2D[:,2])
            self.figure_TP.plot_data_ax1(x_scale, self.data_PT.data_2D[:,1])
            self.figure_TP.plot_data_ax2(x_scale, self.data_PT.data_2D[:,2])
            self.set_axis_labels()
            
        except Exception as e:
            pop_up_error(traceback.format_exc(), 'Pythony Error')
        
        
    def my_Serial_Thread_Read_status(self, status):
        #Thread_2B) Connect Thread Status Signal to action in main (i.e. update status bar)
        if self.debug: print(f'Read : {status:.1f}')
        self.model.statusbar_message(f'Reading {status:.1f} %')
        self.commands_serial.pbar_load.setValue(int(status))
        if int(status) == 100:
            self.model.statusbar_message('Reading loading, uploading table and graph ...')
            
            if self.debug: print('Reading loading, uploading table and graph ...')
            seconds = self.model.mySerial.seconds
            temperature = self.model.mySerial.temperature
            pressure = self.model.mySerial.pressure
            
            #Set Table data
            
            data = np.transpose([seconds, temperature, pressure])
            self.data_PT.set_numpy_2D(data)
            
            self.data_PT.set_timestamp_date(0,0) #Create Timestamp and Date column
            self.commands_figure_T.update_default_date_epoch(0) #Update value in plot buttons
            
            self.data_PT.set_col_names(['Elapsed (sec)', 'Temp (°C)', 'Press (bar)', 'Timestamp (sec)', 'Date (GTM)'])
            
            self.update_all_graphs()
            self.model.statusbar_message('Reading done')
        
    def my_Serial_Thread_Open_status(self, status):
        #Thread_2A) Connect Thread Signal to action in main (i.e. update status bar)
        if status == False:
            if self._counter_1 == 8: self._counter_1 = 0
            self.commands_serial.label_Connect.setText('-'*self._counter_1)
            self._counter_1 += 1 
        else:
            if self.model.mySerial.serial_connected is None:
                #Xiao Found but not Available
                pop_up_error(self.model.mySerial.serial_error, 'SerialError')
            
            else:
                
                #XIAO Found and Available
                
                version = self.model.mySerial.get_version()
                
                
                self.commands_serial.button_Connect.setText('Found TP99 @')
                COM = self.model.mySerial.COM_XIAO
                if self.debug: print(version)
                self.model.statusbar_message(f'{COM} : {version}')
                self.commands_serial.label_Connect.setText(COM)
                
                self.commands_serial.button_test_TP.setDisabled(False)
                self.commands_serial.button_test_LED.setDisabled(False)
                self.commands_serial.button_erase_data.setDisabled(False)
                self.commands_serial.button_save_data.setDisabled(False)
                self.commands_serial.button_load_data.setDisabled(False)
                self.commands_serial.button_set_time.setDisabled(False)
                self.commands_serial.button_battery_date.setDisabled(False)
                self.commands_serial.button_set_name.setDisabled(False)
                
                
                actual_log_time = str(self.model.mySerial.logger_loop_wait_time)
                self.commands_serial.entry_set_time.setText(actual_log_time)
                ETA = self.model.time.TM_s_string( self.model.mySerial.logs_number * self.model.mySerial.logger_loop_wait_time )
                self.commands_serial.label_ETA.setText(actual_log_time + ' sec, Total duration ' + ETA)
                self.get_battery_date()
                self.get_device_name()
                self.commands_serial.entry_set_name.setText(self.device_name)
            
            if self.debug:
                print(type(self.model.mySerial.COM_XIAO))
                print(self.model.mySerial.COM_XIAO)
            
        if self.debug: print('my_Serial_Thread_Open_status ', status)
    
    def start_my_Serial_Thread_Open(self):
        #Thread_3A) Connect main launcher signal (i.e. in start button) to Thread Start process 
        if self.debug: print('Start Worker')
        self.model.mySerial.found_XIAO = False #restart serial if error already connected
        self.my_Serial_Thread_Open_start.emit()
    

    
    
    def start_my_Serial_Thread_Reset(self):
        #Thread_3C) Connect main launcher signal (i.e. in start button) to Thread Start process 
        self.commands_serial.pbar_load.setValue(0)          #Init status bar
        self.commands_serial.pbar_load.setDisabled(False)   #Init status bar
        # #Init status bar 
        # self.commands_serial.setStyleSheet("QProgressBar::chunk "
        #                   "{"
        #                   "background-color: green;"
        #                   "}")
        # lightblue
        # self.commands_serial.setStyleSheet("QProgressBar"
        #                   "{"
        #                   "background-color : red;"
        #                   "border : 1px"
        #                   "}") 
        self.my_Serial_Thread_Reset_start.emit()
    
    def start_my_Serial_Thread_Read(self):
        #Thread_3B) Connect main launcher signal (i.e. in start button) to Thread Start process 
        self.commands_serial.pbar_load.setValue(0)          #Init status bar
        self.commands_serial.pbar_load.setDisabled(False)   #Init status bar
        # #Init status bar 
        # self.commands_serial.setStyleSheet("QProgressBar::chunk "
        #                   "{"
        #                   "background-color: green;"
        #                   "}")
        # self.commands_serial.setStyleSheet("QProgressBar"
        #                   "{"
        #                   "background-color : green;"
        #                   "border : 1px"
        #                   "}") 
        self.my_Serial_Thread_Read_start.emit()
        
    
    def test_LED(self):
        
        status = self.commands_serial.button_test_LED.text()
        
        if status == "Test LED: Turn ON":
            self.model.mySerial.set_LED_ON()
            self.commands_serial.button_test_LED.setText("Test LED: Turn OFF")
        else:
            self.model.mySerial.set_LED_OFF()
            self.commands_serial.button_test_LED.setText("Test LED: Turn ON")
        
        
    def test_connection(self):
        text = self.model.mySerial.test_connection()
        self.commands_serial.label_test_TP.setText(text)
        self.model.statusbar_message(f'Test port {self.model.mySerial.serial_connected.port} : ' + text)
        
    
        
    def connect_port(self):
        selected_i = self.commands_serial.combobox_list_COM_list.currentIndex()
        if selected_i>=0:
            selected_port = self.commands_serial.combobox_list_COM_list.currentText()
            if self.debug : print('Debug : ' + selected_port)
            error = self.model.mySerial.connect_port(selected_port, baudrate=2000000, timeout=5)
            
            if self.model.mySerial.serial_connected:
                # Connected, enable Test, buttons
                self.commands_serial.button_test.setDisabled(False)
                self.commands_serial.button_erase_data.setDisabled(False)
                self.commands_serial.button_load_data.setDisabled(False)
                
                self.model.statusbar_message(f'Connected Port {self.model.mySerial.serial_connected.port}')
            else:
                
                self.model.statusbar_message(f'Connection Error Port {selected_port}')

        
    def COM_info(self):
        selected_i = self.commands_serial.combobox_list_COM_known.currentIndex()
        selected_name = self.model.mySerial.ports_list[selected_i]
        details = self.model.mySerial.ports[selected_name]
        self.pop_up = pop_up(details, selected_name)
        self.pop_up.show()
        if self.debug : print('COM_info', selected_i, selected_name)
        self.model.statusbar_message(f'Port {selected_name} Info')
        
    def list_COM(self):
        if self.debug: 
            print(self.model.mySerial.search_known())
        else:
            self.model.mySerial.search_known()
        self.model.statusbar_message('Updated Ports')
        self.commands_serial.combobox_list_COM_known.clear()
        self.commands_serial.combobox_list_COM_known.addItems(self.model.mySerial.known_found_list)
        
        # self.commands_serial.combobox_list_COM_list.clear()
        # self.commands_serial.combobox_list_COM_list.addItems(self.model.mySerial.known_found_ports)
        
        if self.debug : 
            print('list_COM', self.model.mySerial.ports_list)
            print('list_COM', self.model.mySerial.known_found_list)
            
    def open_file_commands(self, data, i_x, i_y):
        data_x = data[:,i_x]
        data_y = data[:,i_y]
        self.Tab_Double.onclick_button_RESET()
        self.Tab_Fine.Right.plot_data(data_x, data_y)
        self.Tab_Double.Right.Fig_B.plot_data(data_x, data_y)
        
        #Data from Open File to Model
        self.model.peaks_data_x = data_x
        self.model.peaks_data_y = data_y
        
        
    # def data_to_model(self, data):
    #     #Data from Open File to Model
    #     self.model.peaks_data_x = data[:,0]
    #     self.model.peaks_data_y = data[:,1]
        
    def init_Actions(self):
        
        #Menu Files Action Open

        self.action_Open_file = QtWidgets.QAction()
        self.action_Open_file.setText('Open File')
        self.action_Open_file.setShortcut('Ctrl+O')
        self.action_Open_file.triggered.connect(self.open_file)
        
        
        self.action_Font_Size = QtWidgets.QAction()
        self.action_Font_Size.setText(f'Font Size {int(self.font_size)}')
        #self.action_Open_image.setShortcut('Ctrl+O')
        self.action_Font_Size.triggered.connect(self.get_font_size)
        
        self.action_Style_File = QtWidgets.QAction()
        self.action_Style_File.setText("File Style 'None'")
        #https://qss-stock.devsecstudio.com/templates.php
        #self.action_Open_image.setShortcut('Ctrl+O')
        self.action_Style_File.triggered.connect(self.get_set_Style_File)
        
        self.action_Quit = QtWidgets.QAction()
        self.action_Quit.setText('Quit')
        self.action_Quit.setShortcut('Ctrl+Q')
        self.action_Quit.triggered.connect(self.quit_main)
        
        self.action_About = QtWidgets.QAction()
        self.action_About.setText('About TiPi99')
        self.action_About.setShortcut('Ctrl+H')
        self.action_About.triggered.connect(self.open_about)

    
    def init_Menu(self):
        menu_Bar = QtWidgets.QMenuBar()
        
        menu_File = QtWidgets.QMenu("&File", menu_Bar)
        menu_File.addAction(self.action_Open_file)
        menu_File.addAction(self.action_Quit)
        
        menu_Edit = QtWidgets.QMenu('&Edit', menu_Bar)
        menu_Edit.addAction(self.action_Font_Size)
        #menu_Edit.addAction(self.action_Style_File)

        
        menu_Help = QtWidgets.QMenu('&Help', menu_Bar)
        menu_Help.addAction(self.action_About)
        
        menu_Bar.addMenu(menu_File)
        menu_Bar.addMenu(menu_Edit)
        menu_Bar.addMenu(menu_Help)
        self.setMenuBar(menu_Bar)
    
    def init_Statusbar(self):
        self.statusbar = QtWidgets.QStatusBar()
        #self.statusbar.addPermanentWidget(QtWidgets.QLabel("Welcome !"))
        #self.statusbar.addWidget(QtWidgets.QLineEdit())
        self.setStatusBar(self.statusbar)
        #self.statusbar.showMessage('Init 2')
        self.model.statusbar_message_add(self.statusbar.showMessage)
    
    def open_about(self):
        self.about.show()
        
    def get_set_Style_File(self):
        self.model.statusbar_message('Select QSS Style File')
        #filename =  r'D:\Yiuri\Python\Qt5\menta\OpenSerial2\241104_we.txt'
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Select .qss File", '', "QSS files (*.qss)")
        if self.debug: print(filename)
        self.action_Style_File.setText(f"File Style '{Path(filename).stem}'")
        if filename != '':
            style = Path(filename).read_text()
            style = style + """
                          * {
                              font-size: """ + str(int(self.font_size)) + """px;
                        }
                          """
            if self.debug: print(style)
            QtWidgets.qApp.setStyleSheet(style)
            
    def get_font_size(self):
        size, ok = QtWidgets.QInputDialog.getInt(self, 'Font Size', 'Enter size (min 10):', self.font_size, 10)
        if self.debug: print(size)
        if ok:
            
            self.font_size = size
            self.action_Font_Size.setText(f'Font Size {int(self.font_size)}')
            self.update_font_size()
    
    def update_font_size(self):
        
        QtWidgets.qApp.setStyleSheet("""
                      * {
                          font-size: """ + str(int(self.font_size)) + """px;
                    }
                      """)
                      
    def open_file(self):
        self.model.statusbar_message('Opening file, please wait ...')
        #filename =  r'D:\Yiuri\Python\Qt5\menta\OpenSerial2\241104_we.txt'
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Select File")
        if filename != '':
            try:
                self.data_PT.fast_reset()
                self.data_PT.reset()
                    
                f = Path(filename)
                self.filename = f
                
                if self.debug:
                    print(self.filename)
                    
                if f.suffix == '.txt':
                    
                    col_0 = np.genfromtxt(f,usecols=(0))
                    col_1 = np.genfromtxt(f,usecols=(1))
                    col_2 = np.genfromtxt(f,usecols=(2))
                    col_3 = np.genfromtxt(f,usecols=(3))
                    
                elif f.suffix == '.csv': 
                    
                    col_0 = np.genfromtxt(f,usecols=(0), delimiter = ",")
                    col_1 = np.genfromtxt(f,usecols=(1), delimiter = ",")
                    col_2 = np.genfromtxt(f,usecols=(2), delimiter = ",")
                    col_3 = np.genfromtxt(f,usecols=(3), delimiter = ",")
                    
                elif f.suffix == '.npy':
                    data = np.load(f.with_suffix('.npy'), allow_pickle = True)
                    col_0 = data[:,0]
                    col_1 = data[:,1]
                    col_2 = data[:,2]
                    col_3 = data[:,3]
                
                seconds = col_0.astype(int)
                temperature = col_1
                pressure = col_2
                timestamp = col_3.astype(int)
                
                #self.commands_figure_T.timestamp_t0 = timestamp[0]
                self.commands_figure_T.update_default_date_epoch(timestamp[0] - seconds[0])  #Update value in plot buttons

                # #only for .npy
                # if f.suffix == '.npy': 
                #     with open(f, 'rb') as f:
                #         seconds = np.load(f)
                #         temperature = np.load(f)
                #         pressure = np.load(f)
                        
                

                self.model.mySerial.seconds = seconds 
                self.model.mySerial.temperature = temperature
                self.model.mySerial.pressure = pressure 
                
                data = np.transpose([seconds, temperature, pressure, timestamp])
                if self.debug:
                    print('data shape ',data.shape)
                    
                self.data_PT.set_numpy_2D(data)
                self.data_PT.timestamp = timestamp
                
                self.data_PT.set_date(3)
                self.data_PT.set_col_names(['Elapsed (sec)', 'Temp (°C)', 'Press (bar)', 'Timestamp (sec)', 'Date'])
                self.update_timestamp()
                
                #self.update_all_graphs() is included in self.update_timestamp()
                
                self.commands_serial.button_save_data.setDisabled(False)
                
            except Exception as e:
                pop_up_error(traceback.format_exc(), 'Pythony Error')
                
            
            
            self.model.statusbar_message('File opened')
        else:
            self.model.statusbar_message(f'Open File Cancelled')
            
    def quit_main(self):
        self.close() #intercepted by closeEvent
        
    def closeEvent(self, event):
        choice = QtWidgets.QMessageBox.question(self, "Quit", f"Do you want to Quit {self.window_Title} ?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        QtWidgets.QMessageBox()
        if choice == QtWidgets.QMessageBox.Yes:
            if self.model.mySerial.serial_connected:
                if self.debug: print(self.model.mySerial.serial_connected)
                self.model.mySerial.close_port()
            
            self.about.close()
            self.main_thread.quit() #Thread_7) Close Main Thread at the end
            event.accept()
        else:
            event.ignore()
            
     
def main():
    #QtGui.QStyleFactory.create(text)
    app = QtWidgets.QApplication(sys.argv)
    #app.setStyleSheet(Path('stylesheet_Dioptas.qss').read_text()) #StyleSheet #Adaptic #stylesheet_Dioptas #Diffnes
    window = TiPi99() 
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()