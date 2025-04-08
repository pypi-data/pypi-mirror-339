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

import configparser as cp
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import os, sys
from datetime import datetime
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets, QtCore
from time import sleep

if __name__ == '__main__':
    script = os.path.abspath(__file__)
    script_dir = os.path.dirname(script)
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


class my_Serial():
    
    work_requested = QtCore.pyqtSignal()
    
    def __init__(self, debug = False):
        self.debug = debug
        #serial connection
        
        self.serial_connected = None #Serial object
        # self.serial_connected.port return port name 
        # https://pyserial.readthedocs.io/en/latest/pyserial_api.html
        
        self.serial_error = ""
        #Specific Init / Open Serial
        
        self.ports_list = [] #names
        self.ports = {} #details
        self.devices_list = []
        self.devices = {}
        self.status = {}
        self.known_found_ports = []
        self.methods = ['description',
        'device',
        'hwid',
        'interface',
        'location',
        'manufacturer',
        'pid',
        'product',
        'serial_number',
        'usb_description',
        'usb_info',
        'vid']
        self.known_devices = ['XIAO' , '10374', '32815']

        self.found_XIAO = False
        self.COM_XIAO = None
        
        #FRAM Info
        self.FRAM_memory_size = 4 #2 / 4 megabits #262144 2 megabits 524288 4 megabits
        self.log_bytes = 8 #1 log use 8 bytes: 4 seconds, 2 temperature, 2 pressure
        self.packet = int(4096) #Serial data packet size x transmission
        self.loop = int(131072*self.FRAM_memory_size/self.packet) #262144 2 megabits 524288 4 megabits #Serial data packet loops x transmission
        self.reserved_bytes = 16 #check same in c++ microcontroller #Last bytes reserved for data in FRAM
        self.logs_number = (131072*self.FRAM_memory_size - self.reserved_bytes)//self.log_bytes #total number of logs
        
        #Loaded Data
        self.All_bin = np.zeros((self.packet,self.loop))
        self.temperature = None
        self.seconds = None
        self.pressure = None
        self.logger_loop_wait_time = None
        self.battery_timestamp = None
        
    # def error_box(self, error, title = "Script Error"):
    #     msgBox = QtWidgets.QMessageBox(self)
    #     msgBox.setIcon(QtWidgets.QMessageBox.Critical)
    #     msgBox.setWindowTitle(title)
    #     msgBox.setText(str(error))
    #     msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    #     msgBox.exec()
    
    #Specific methods TP99
    
    def set_FRAM_memory_size(self, size : int):
        self.FRAM_memory_size = size
        self.loop = int(131072*self.FRAM_memory_size/self.packet) #262144 2 megabits 524288 4 megabits #Serial data packet loops x transmission
        self.logs_number = (131072*self.FRAM_memory_size - self.reserved_bytes)//self.log_bytes #total number of logs
        
    def get_log_time(self):
        command = 'd'.encode() #//d  //Get logger loop wait time
        self.serial_connected.write(command)

        _ = self.serial_connected.read_until(b'\r\n')
        if self.debug: print(str(_))
        self.logger_loop_wait_time = int(_[28:]) #Serial.print("Get logger loop wait time = ");
        
    def set_log_time(self, time : int):
        command = f'{time}D'.encode() #//nD //Set logger loop wait time
        self.serial_connected.write(command)
        _ = self.serial_connected.read_until(b'\r\n')
        if self.debug: print(str(_))
        self.logger_loop_wait_time = int(_[28:])  #Serial.print("Set logger loop wait time = ");
    
    def set_name1(self, value : int):
        command = f'{value}M'.encode() #//nD //Set logger loop wait time
        self.serial_connected.write(command)
        _ = self.serial_connected.read_until(b'\r\n')
        if self.debug: print(str(_))
        #self. = int(_[19:]) #Serial.print("Set device name1 = ");
    
    def set_name2(self, value : int):
        command = f'{value}N'.encode() #//nD //Set logger loop wait time
        self.serial_connected.write(command)
        _ = self.serial_connected.read_until(b'\r\n')
        if self.debug: print(str(_))
        #self. = int(_[19:]) #Serial.print("Set device name1 = ");
    
    def get_name1(self):
        command = 'm'.encode() #//a //Get battery timestamp
        self.serial_connected.write(command)

        _ = self.serial_connected.read_until(b'\r\n')
        if self.debug: print(str(_))
        #self. = int(_[19:]) #Serial.print("Get timestamp = ");
        return int(_[19:])
    
    def get_name2(self):
        command = 'n'.encode() #//a //Get battery timestamp
        self.serial_connected.write(command)

        _ = self.serial_connected.read_until(b'\r\n')
        if self.debug: print(str(_))
        #self. = int(_[19:]) #Serial.print("Get timestamp = ");
        return int(_[19:])
    
    def get_battery_timestamp(self):
        command = 'a'.encode() #//a //Get battery timestamp
        self.serial_connected.write(command)

        _ = self.serial_connected.read_until(b'\r\n')
        if self.debug: print(str(_))
        self.battery_timestamp = int(_[16:]) #Serial.print("Get timestamp = ");
        return int(_[16:])

    
    def set_battery_timestamp(self, timestamp : int):
        command = f'{timestamp}A'.encode() #//nA //Set battery timestamp
        self.serial_connected.write(command)
        _ = self.serial_connected.read_until(b'\r\n')
        if self.debug: print(str(_))
        self.battery_timestamp = int(_[16:])  #Serial.print("Set timestamp = ");
        
        
    def test_connection(self):
        command = 'T'.encode()
        self.serial_connected.write(command)
        _ = self.serial_connected.read_until(b'\r\n')
        if self.debug: print(str(_))
        
        return _.strip().decode( "utf-8" )
        
    def set_LED_ON(self):
        command = '1L'.encode() #//nL //Turn LED n (1 = ON, else = OFF)
        self.serial_connected.write(command)
        _ = self.serial_connected.read_until(b'\r\n')
        if self.debug: print(str(_))
      
    def set_LED_OFF(self):
        command = '0L'.encode() #//nL //Turn LED n (1 = ON, else = OFF)
        self.serial_connected.write(command)
        _ = self.serial_connected.read_until(b'\r\n')
        if self.debug: print(str(_))
    
    def get_version(self):
        command = 'I'.encode() #//nL //Turn LED n (1 = ON, else = OFF)
        self.serial_connected.write(command)
        _ = self.serial_connected.read_until(b'\r\n')
        if self.debug: print(str(_))
        
        return _.strip().decode( "utf-8" )
    
    # def decode(self):
        
    #     cut = self.FRAM_memory_size*131072//self.log_bytes
    #     last_measure = cut*self.log_bytes
        
    #     test = self.All_bin.flatten('F')
    #     test = test[0:last_measure]
        
    #     bytes_test = test.astype(np.uint8)
    #     bytes_test_reshape = bytes_test[:cut*self.log_bytes].reshape((cut,self.log_bytes))
        
    #     #4 bytes 0:4 => dtype= int
    #     rtc_byte_array_C  = bytes_test_reshape[:,0:4].copy(order='C')
    #     rtc_seconds = np.frombuffer(rtc_byte_array_C, dtype= np.uintc)
        
    #     #4 bytes 0:4 => dtype= int
    #     # millis_byte_array_C  = bytes_test_reshape[:,4:8].copy(order='C')
    #     # millis_seconds = np.frombuffer(millis_byte_array_C, dtype= np.uintc)/1e3
        
    #     #2 bytes 5:6 => dtype= np.int16
    #     temps_byte_array_C = bytes_test_reshape[:,4:6].copy(order='C')
    #     temperature = np.frombuffer(temps_byte_array_C, dtype= np.int16)/100
        
    #     #2 bytes 7:8 => dtype= np.int16
    #     pressure_byte_array_C = bytes_test_reshape[:,6:8].copy(order='C')
    #     pressure = np.frombuffer(pressure_byte_array_C, dtype= np.int16)/10
        
    #     rtc_seconds = rtc_seconds.astype(float)
    #     rtc_seconds = rtc_seconds - rtc_seconds[0]
        
    #     #Non_Zero
    #     mask = temperature != 0 
    #     self.rtc_seconds_NZ = rtc_seconds[mask]
    #     self.temperature_NZ = temperature[mask]
    #     self.pressure_NZ = pressure[mask]
        
    #Specific methods / Open Serial
    
    def check_ports(self):
        '''
        Check COM ports
        
        Update:
            
            self.ports_list
            self.ports    :dict with ports self.methods
            self.devices_list
            self.devices  :dict with devices self.methods
        
        Returns:
        
            self.ports_list

        '''
        self.ports_list = []
        self.ports = {}
        self.devices_list = []
        self.devices = {}

        for port in serial.tools.list_ports.comports():
            self.ports_list.append(port.name)

            # info= {method : getattr(port, method) for method in methods if method is not None}
            # ports[port.name] = info
            _ = {}
            for method in self.methods:
                __ = getattr(port, method)
                if callable(__):
                    _[method] = getattr(port, method)()
                else:
                    _[method] = getattr(port, method)
            self.ports[port.name] = _
            
            if port.vid is not None and port.pid is not None:
                self.devices_list.append(port.name)

                # info= {method : getattr(port, method) for method in methods}
                # devices[port.name] = info
                _ = {}
                for method in self.methods:
                    __ = getattr(port, method)
                    if callable(__):
                        _[method] = getattr(port, method)()
                    else:
                        _[method] = getattr(port, method)
                    
                self.devices[port.name] = _
                
        return self.ports_list #, self.ports, self.devices_list, self.devices
    
    def search_sn(self, sn):
        self.check_ports()
            
        name = 'Not  Found'
        for key, value in self.ports.items():

            if self.ports[key]['serial_number'] == sn:

                name = key
                
        return name
    
    def check_open(self):
        self.status = {}
        self.check_ports()
        
        if isinstance(self.ports, str):
            _ = [self.ports]
        else:
            _ = self.ports
        self.check_ports()
        if self.debug: print(_)
        for i in _:
            if i not in self.ports:
                self.status[i] = 'Not Found'
            else:
                try:
                    ser = serial.Serial(i, 2000000, timeout=.1)
                    ser.close()
                    self.status[i] = 'Available'
                except:
                    self.status[i] = 'Busy'
        return self.status
    
    def search_vid_pid(self, vid, pid):
        self.check_ports()
        found = {}
        for key, value in self.ports.items():
            try:
                if (self.ports[key]['vid'] == vid) and (self.ports[key]['pid'] == pid) :
                    found[key] = self.ports[key]['serial_number']
            except:
                pass
        return found
    
    def search_known(self):
        '''
        
        Search for known device by PID VID registered in KnownDevice.csv
        
        call self.check_ports()
        
        update self.known_found_ports = []
        
        '''
        self.known_found_list = []
        self.known_found_ports = []
        self.check_ports()
        if self.known_devices is not None:
            # _ = 0 
            # for i in range(self.known_devices[1:,0]):
            #     VID = self.known_devices[i+1,1]
            #     PID = self.known_devices[i+1,2]
            #     for key, value in self.ports.items():
            #         try:
            #             if (self.ports[key]['vid'] == int(VID)) and (self.ports[key]['pid'] == int(PID)) :
            #                 self.known_found_list.append(self.ports_list[_] + ': ' + self.known_devices[i+1,0])
            #                 self.known_found_ports.append(self.ports_list[_])
            #                 _+= 1
            #             else:
            #                 self.known_found_list.append(self.ports_list[_] + ': unk')
            #                 _+= 1
            #         except:
            #             print('error')
            #             pass
            #     return self.known_found_list

            VID = self.known_devices[1]
            PID = self.known_devices[2]
            _ = 0 
            for key, value in self.ports.items():
                try:
                    if (self.ports[key]['vid'] == int(VID)) and (self.ports[key]['pid'] == int(PID)) :
                        self.known_found_list.append(self.ports_list[_] + ': ' + self.known_devices[0])
                        self.known_found_ports.append(self.ports_list[_])
                        _+= 1
                    else:
                        self.known_found_list.append(self.ports_list[_] + ': unk')
                        _+= 1
                except:
                    print('error')
                    pass
            return self.known_found_list
        else:
            print('No known devices')
    
    def connect_port(self, port, baudrate=9600, timeout=None):
        '''
        timeout = None: wait forever / until requested number of bytes are received
        timeout = 0: non-blocking mode, return immediately in any case, returning zero or more, up to the requested number of bytes
        timeout = x: set timeout to x seconds (float allowed) returns immediately when the requested number of bytes are available, otherwise wait until the timeout expires and return all bytes that were received until then.

        '''
        
        try:
            self.serial_connected = serial.Serial(port, baudrate, timeout)
            _ = self.serial_connected.read_all()
            print(_)
        except serial.SerialException as e:
            if self.debug: print('Debug: Serial error: ' + str(e))
            error = str(e)
            if 'The system cannot find the file specified' in error:
                message = 'COM not found, error details: \n\n' + error 
            elif 'Access is denied.' in error:
                if self.serial_connected is None:
                    message = 'COM busy (check others programs), error details:\n\n' + error
                else:
                    message = self.serial_connected.port + ' already connected, error details:\n\n' + error
            self.serial_error = message
    
    def close_port(self):
        self.serial_connected.close()
        self.serial_connected = None


class my_Serial_Thread_Reset(QtCore.QObject):
    #Thread C Delete data in TP99 FRAM (write to 0)

    def __init__(self, my_Serial : my_Serial):
        super().__init__()
        self.my_Serial = my_Serial
        
    erasing = QtCore.pyqtSignal(float)
    
    
    @QtCore.pyqtSlot()
    def start(self):
        #Thread_2C) Create Thread Start method
        if self.my_Serial.debug: 
            print('Start my_Serial_Thread_Reset')
        
        # Reset Data
        max_iter = int((131072*self.my_Serial.FRAM_memory_size - self.my_Serial.reserved_bytes)/2048)
        command = 'Z'.encode() #//Z //set all value in mem to 0
        self.my_Serial.serial_connected.write(command)
        while True:
            _ = self.my_Serial.serial_connected.read_until(b'\r\n')
            if self.my_Serial.debug: print(_)
            if _ == b'Done\r\n': break
        
            self.erasing.emit( int(_)*100 / max_iter) #Thread_2C) Emit Thread Status Signal

        
class my_Serial_Thread_Read(QtCore.QObject):
    #Thread B Read data from TP99 FRAM

    def __init__(self, my_Serial : my_Serial):
        super().__init__()
        self.my_Serial = my_Serial
        
    reading = QtCore.pyqtSignal(float)
    
    
    @QtCore.pyqtSlot()
    def start(self):
        #Thread_2B) Create Thread Start method
        if self.my_Serial.debug: 
            print('Start my_Serial_Thread_Read')
        
        
        command = 'R'.encode() #//R //reset read n bytes loop, must be used before //nr
        self.my_Serial.serial_connected.write(command)
        
        # Read All Fram
        
        command = f'{self.my_Serial.packet}r'.encode() #//nr //read n bytes
        for i in range(self.my_Serial.loop):
            try:
                self.my_Serial.serial_connected.write(command)
                self.my_Serial.All_bin[:,i] = np.frombuffer(self.my_Serial.serial_connected.read(self.my_Serial.packet), dtype=np.uint8)
                if self.my_Serial.debug: 
                    print(i + 1, self.my_Serial.loop)
                # if np.all(All_bin[:,i] == 0) :
                #     print("Empty")
                #     break
                if i < self.my_Serial.loop - 2:
                    #Avoid race condition, memorize data before emitting 100
                    self.reading.emit( (i + 1)*100 / self.my_Serial.loop) #Thread_2B) Emit Thread Status Signal
            except Exception as error:
                print(f'Error reading packet {i} :', error)
        
        All = self.my_Serial.All_bin.flatten('F')
        
        cut = (self.my_Serial.FRAM_memory_size*131072 - self.my_Serial.reserved_bytes)//self.my_Serial.log_bytes
        log_bytes = self.my_Serial.log_bytes
        
        bytes_All = All.astype(np.uint8)
        bytes_All_reshape = bytes_All[:cut*log_bytes].reshape((cut,log_bytes))
        
        #2 bytes 4:6 => dtype= np.int16
        temp_byte_array_C = bytes_All_reshape[:,4:6].copy(order='C')
        temperature= np.frombuffer(temp_byte_array_C, dtype= np.int16).astype(np.float64)/100 - 10
        
        #4 bytes 0:4 => dtype= int
        sec_byte_array_C  = bytes_All_reshape[:,0:4].copy(order='C')
        seconds = np.frombuffer(sec_byte_array_C, dtype= np.uintc).astype(np.float64)
        
        #2 bytes 4:6 => dtype= np.int16
        pressure_byte_array_C = bytes_All_reshape[:,6:8].copy(order='C')
        pressure = np.frombuffer(pressure_byte_array_C, dtype= np.int16).astype(np.float64) * 1500000  / 65535
    
    
        # #Reserved bits = 8, last data not a measure
        # temperature = temperature[:-1]
        # seconds = seconds[:-1]
        # pressure = pressure[:-1]
        
        mask = temperature>-9
        masked_seconds = seconds[mask] #- T0 = 946684800
        masked_temperature = temperature[mask]
        masked_pressure = pressure[mask]
        
        self.my_Serial.seconds = masked_seconds
        self.my_Serial.temperature = masked_temperature
        self.my_Serial.pressure = masked_pressure/1000
        
        self.reading.emit(100) #Thread_2B) Emit Thread Status Signal
        # test.seconds = seconds
        # test.temperature = temperature
        # test.pressure = pressure
        
        
        
class my_Serial_Thread_Open(QtCore.QObject):
    #Thread A Search TP99 COM port and connect

    def __init__(self, my_Serial : my_Serial):
        super().__init__()
        self.my_Serial = my_Serial
        
    searching = QtCore.pyqtSignal(bool)
    #searching = QtCore.pyqtSignal(np.ndarray)
    
    @QtCore.pyqtSlot()
    def start(self):
        #Thread_3A) Create Thread Start method

        if self.my_Serial.debug: 
            print('Start my_Serial_Thread_Open')
            print(self.my_Serial.found_XIAO)
        
        while self.my_Serial.found_XIAO == False :
            
            sleep(0.25)
            self.my_Serial.check_ports()
            if self.my_Serial.known_devices is not None:

                VID = self.my_Serial.known_devices[1]
                PID = self.my_Serial.known_devices[2]
                for key, value in self.my_Serial.ports.items():
                    if (self.my_Serial.ports[key]['vid'] == int(VID)) and (self.my_Serial.ports[key]['pid'] == int(PID)) :
                        COM_XIAO = self.my_Serial.ports[key]['device']
                        
                        self.my_Serial.connect_port(COM_XIAO, 2000000, timeout=5)
                        
                        self.my_Serial.found_XIAO = True
                        
                        if self.my_Serial.serial_connected is not None:
                            self.my_Serial.serial_connected.set_buffer_size(rx_size = 2147483647, tx_size = 12800)
                            command = 'I'.encode()  #//I //Info
                            self.my_Serial.serial_connected.write(command)
                            Info = self.my_Serial.serial_connected.read_until(b'\r\n')
                            self.my_Serial.COM_XIAO = COM_XIAO
                            self.my_Serial.Info = Info.decode('utf-8')
                            
                            self.my_Serial.get_log_time() 
                            
                        
                        break
            
            
            self.searching.emit(self.my_Serial.found_XIAO) #Thread_2A) Emit Thread Status Signal
            print(datetime.now().strftime("%y%m%d_%H%M%S.%f"))
                        
                        
            
                        
                        

    
if __name__ == '__main__':
    test = my_Serial(True)
    test.check_open()
    
    search = True
    
    while(search):        
        sleep(1)
        test.check_ports()
        if test.known_devices is not None:

            VID = test.known_devices[1]
            PID = test.known_devices[2]
            for key, value in test.ports.items():
                if (test.ports[key]['vid'] == int(VID)) and (test.ports[key]['pid'] == int(PID)) :
                    print('Found', test.ports[key]['device'] )
                    COM_XIAO = test.ports[key]['device']
                    test.connect_port(COM_XIAO, 2000000, timeout=5)
                    
                    #Code inside my_Serial_Worker
                    test.serial_connected.set_buffer_size(rx_size = 2147483647, tx_size = 12800)
                    command = 'I'.encode() #//I //Info
                    test.serial_connected.write(command)
                    Info = test.serial_connected.read_until(b'\r\n')
                    test.COM_XIAO = COM_XIAO
                    test.Info = Info.decode('utf-8')
                    test.found_XIAO = True
                    search = False
                else:
                    print('Searching ...') 


    def reset():
        command = 'Z'.encode() #//Z //set all value in mem to 0
        test.serial_connected.write(command)
        while True:
            _ = test.serial_connected.read_until(b'\r\n')
            if test.debug: print(_)
            if _ == b'Done\r\n': break
    


    #%% Read Data
    
    def read_data():
        command = f'{test.packet}r'.encode() #//nr //read n bytes
        for i in range(test.loop):
            try:
                test.serial_connected.write(command)
                test.All_bin[:,i] = np.frombuffer(test.serial_connected.read(test.packet), dtype=np.uint8)
                print(i + 1, test.loop)
                # if np.all(All_bin[:,i] == 0) :
                #     print("Empty")
                #     break
            except Exception as error:
                print(f'Error reading packet {i} :', error)
        
        All = test.All_bin.flatten('F')
        
        cut = (test.FRAM_memory_size*131072 - test.reserved_bytes)//test.log_bytes
        log_bytes = test.log_bytes
        
        bytes_All = All.astype(np.uint8)
        bytes_All_reshape = bytes_All[:cut*log_bytes].reshape((cut,log_bytes))
        
        #2 bytes 4:6 => dtype= np.int16
        temp_byte_array_C = bytes_All_reshape[:,4:6].copy(order='C')
        temperature= np.frombuffer(temp_byte_array_C, dtype= np.int16).astype(np.float64)/100 - 10
        
        #4 bytes 0:4 => dtype= int
        sec_byte_array_C  = bytes_All_reshape[:,0:4].copy(order='C')
        seconds = np.frombuffer(sec_byte_array_C, dtype= np.uintc).astype(np.float64)
        
        #2 bytes 4:6 => dtype= np.int16
        pressure_byte_array_C = bytes_All_reshape[:,6:8].copy(order='C')
        pressure = np.frombuffer(pressure_byte_array_C, dtype= np.int16).astype(np.float64) * 1500000  / 65535
    
    
        # #Reserved bits = 8, last data not a measure
        # temperature = temperature[:-1]
        # seconds = seconds[:-1]
        # pressure = pressure[:-1]
        
        mask = temperature>-9
        we_sec = seconds[mask] #- T0 = 946684800
        we_m = we_sec/60
        we_h = we_sec/3600
        we_t = temperature[mask]
        we_P = pressure[mask]
        
        test.seconds = seconds
        test.temperature = temperature
        test.pressure = pressure

    
# Manually close the port used in test
# test.close_port()


  