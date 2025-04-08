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
from matplotlib.backend_bases import MouseEvent

import os, sys
from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar



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


class Frame_1_graph_2_ax(QtWidgets.QFrame):
    
    signal_fig_on_click = QtCore.pyqtSignal(MouseEvent)
    signal_fig_click_no_drag = QtCore.pyqtSignal(MouseEvent)
    signal_fig_click_drag = QtCore.pyqtSignal(MouseEvent)
    
    def __init__(self, model = None, debug = False):
        
        super().__init__()
        self.model = model
        self.debug = debug
        if self.debug: print("\nDebug mode\n")
        #if self.debug: self.setStyleSheet("border: 20px solid red")
        
        layout = QtWidgets.QVBoxLayout()
        
        self.ax1_color = 'tab:red' #https://matplotlib.org/stable/users/explain/colors/colors.html
        self.ax2_color = 'tab:blue'
        
        self.fig_ref_ax1 = [] #List of plot ref
        self.fig_ref_names_ax1 = [] #List of plot names
        self.x_min_all_ax1 = np.inf
        self.x_max_all_ax1 = -np.inf
        self.y_min_all_ax1 = np.inf
        self.y_max_all_ax1 = -np.inf
        self.total_plot_n_ax1 = 0 
        self.x_moving_ref_left_ax1 = 0 #Ref to detect drag
        self.y_moving_ref_left_ax1 = 0 #Ref to detect drag
        
        
        self.fig = plt.figure(figsize=(5, 5))
        self.canvas = FigureCanvas(self.fig)
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('button_release_event', self.off_click)
        
        self.navigationToolbar = NavigationToolbar(self.canvas, self, coordinates=True)
        self.ax1 = self.fig.add_subplot(111)
        self.ax1.tick_params(axis='y', labelcolor=self.ax1_color)
        self.ax1.grid(color=self.ax1_color)
        
        self.ax2 = self.ax1.twinx() 
        self.ax2.tick_params(axis='y', labelcolor=self.ax2_color)
        self.ax2.grid(color=self.ax2_color)
        
        #self.navigationToolbar.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        
        # show canvas
        self.canvas.show()
        
        # create main layout

        layout.addWidget(self.canvas)
        layout.addWidget(self.navigationToolbar)

        self.setLayout(layout)
        
    
    def on_click(self, event):
        if self.debug: print('on_click')
        self.x_moving_ref_left_ax1 = event.xdata
        self.y_moving_ref_left_ax1 = event.ydata
        self.signal_fig_on_click.emit(event)
    
    def off_click(self, event):
        if self.debug: print('off_click')
        _x = event.xdata
        _y = event.ydata
        not_moved = ((self.x_moving_ref_left_ax1 == _x) and (self.y_moving_ref_left_ax1 == _y))
        if not_moved:
            self.signal_fig_click_no_drag.emit(event)
        else:
            self.signal_fig_click_drag.emit(event)
    
    def reset_ax1(self):
        self.ax1.cla()
        self.fig_ref_ax1 = []
        self.fig_ref_names_ax1 = []
        self.total_plot_n_ax1 = 0 
    
    def reset_ax2(self):
        self.ax2.cla()
        self.fig_ref_ax2 = []
        self.fig_ref_names_ax2 = []
        self.total_plot_n_ax2 = 0 
        
    def plot_data_ax1(self, data_x, data_y = None, label = None):
        self.reset_ax1()
        
        if data_y is None:
            data_y = data_x[:,1]
            data_x = data_x[:,0]
            
        
        self.ax1.grid()
        #print(data_x.shape,data_y.shape)
        if label is not None:
            ref, = self.ax1.plot(data_x, data_y, label = label, color=self.ax1_color)
        else:
            ref, = self.ax1.plot(data_x, data_y, color=self.ax1_color)
        self.total_plot_n_ax1+= 1
        self.fig_ref_ax1.append(ref)
        self.fig_ref_names_ax1.append(label)
        if label is not None:
            leg = self.ax1.legend()
            leg.set_draggable(True)
        self.canvas.draw()
    
    def plot_data_ax2(self, data_x, data_y = None, label = None):
        self.reset_ax2()
        
        if data_y is None:
            data_y = data_x[:,1]
            data_x = data_x[:,0]
            
        
        self.ax2.grid()
        #print(data_x.shape,data_y.shape)
        if label is not None:
            ref, = self.ax2.plot(data_x, data_y , label = label, color=self.ax2_color)
        else:
            ref, = self.ax2.plot(data_x, data_y, color=self.ax2_color)
        self.total_plot_n_ax2+= 1
        self.fig_ref_ax2.append(ref)
        self.fig_ref_names_ax2.append(label)
        if label is not None:
            leg = self.ax2.legend()
            leg.set_draggable(True)
        self.canvas.draw()
        
    def delete_plot(self, element):
        if self.debug: print(f'pop {element}')
        _ = self.fig_ref_ax1.pop(element)
        _.remove()
        cancelled = self.fig_ref_names_ax1.pop(element)
        if cancelled is not None:
            leg = self.ax1.legend()
            leg.set_draggable(True)
        self.autoscale_ax1()
        self.canvas.draw()

    def delete_plot(self, element):
        if self.debug: print(f'pop {element}')
        _ = self.fig_ref_ax2.pop(element)
        _.remove()
        cancelled = self.fig_ref_names_ax2.pop(element)
        if cancelled is not None:
            leg = self.ax2.legend()
            leg.set_draggable(True)
        self.autoscale_ax2()
        self.canvas.draw()
        
    def add_plot_ax1(self, data_x, data_y = None, label = None):
        if data_y is None:
            data_y = data_x[:,1]
            data_x = data_x[:,0]
        i = self.total_plot_n_ax1
        #plot_label = f'Plot {i}'
        self.total_plot_n_ax1+= 1
        if label is not None:
            ref, = self.ax1.plot(data_x, data_y, label = label)
        else:
            ref, = self.ax1.plot(data_x, data_y)
        self.fig_ref_ax1.append(ref)
        self.fig_ref_names_ax1.append(label)
        if label is not None:
            leg = self.ax1.legend()
            leg.set_draggable(True) 
        self.autoscale_ax1()
        self.canvas.draw()
    
    def add_plot_ax2(self, data_x, data_y = None, label = None):
        if data_y is None:
            data_y = data_x[:,1]
            data_x = data_x[:,0]
        i = self.total_plot_n_ax2
        #plot_label = f'Plot {i}'
        self.total_plot_n_ax2+= 1
        if label is not None:
            ref, = self.ax2.plot(data_x, data_y, label = label)
        else:
            ref, = self.ax2.plot(data_x, data_y)
        self.fig_ref_ax2.append(ref)
        self.fig_ref_names_ax2.append(label)
        if label is not None:
            leg = self.ax2.legend()
            leg.set_draggable(True) 
        self.autoscale_ax2()
        self.canvas.draw()
        
    def autoscale_ax1(self):
        border = 0.1
        max_x = -np.inf
        max_y = -np.inf
        min_x = np.inf
        min_y = np.inf
        lines = self.ax1.get_lines()
        for line in lines:
            x_data = line.get_xdata()
            y_data = line.get_ydata()
            max_x = max(max_x, x_data.max())
            max_y = max(max_y, y_data.max())
            min_x = min(min_x, x_data.min())
            min_y = min(min_y, y_data.min())
        
        border_x = (max_x - min_x)*border/2
        border_y = (max_y - min_y)*border/2
        self.ax1.set_xlim(min_x-border_x, max_x+border_x)
        self.ax1.set_ylim(min_y-border_y, max_y+border_y)

    def autoscale_ax2(self):
        border = 0.1
        max_x = -np.inf
        max_y = -np.inf
        min_x = np.inf
        min_y = np.inf
        lines = self.ax2.get_lines()
        for line in lines:
            x_data = line.get_xdata()
            y_data = line.get_ydata()
            max_x = max(max_x, x_data.max())
            max_y = max(max_y, y_data.max())
            min_x = min(min_x, x_data.min())
            min_y = min(min_y, y_data.min())
        
        border_x = (max_x - min_x)*border/2
        border_y = (max_y - min_y)*border/2
        self.ax2.set_xlim(min_x-border_x, max_x+border_x)
        self.ax2.set_ylim(min_y-border_y, max_y+border_y)
        
    def rescale_xy_ax1(self, event = None):
        self.rescale_x_ax1()
        self.rescale_y_ax1()
        
    def rescale_x_ax1(self):
        x_min = self.x_min_all_ax1
        x_max = self.x_max_all_ax1
        x_range = (x_max -x_min)*0.05*np.array((-1,1))+np.array((x_min,x_max))
        self.ax1.set_xlim(x_range)
        self.canvas.draw()
        if self.debug: print('Rescale x')
    
    
    def rescale_y_ax1(self):
        y_min = self.y_min_all_ax1
        y_max = self.y_max_all_ax1
        y_range = (y_max -y_min)*0.05*np.array((-1,1))+np.array((y_min,y_max))
        self.ax1.set_ylim(y_range)
        self.canvas.draw()
        if self.debug: print('Rescale y')
        
    def rescale_xy_ax2(self, event = None):
        self.rescale_x_ax2()
        self.rescale_y_ax2()
        
    def rescale_x_ax2(self):
        x_min = self.x_min_all_ax2
        x_max = self.x_max_all_ax2
        x_range = (x_max -x_min)*0.05*np.array((-1,1))+np.array((x_min,x_max))
        self.ax2.set_xlim(x_range)
        self.canvas.draw()
        if self.debug: print('Rescale x')
    
    
    def rescale_y_ax2(self):
        y_min = self.y_min_all_ax2
        y_max = self.y_max_all_ax2
        y_range = (y_max -y_min)*0.05*np.array((-1,1))+np.array((y_min,y_max))
        self.ax2.set_ylim(y_range)
        self.canvas.draw()
        if self.debug: print('Rescale y')

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("""
                      * {
                          font-size: 15px;
                    }
                      """)
 
    window = Frame_1_graph_2_ax(debug = True)
    x = np.linspace(0, 50)
    y = 3 + x*2
    window.plot_data_ax1(x, y)
    window.plot_data_ax2(x + 10, y + 15)
    window.show()
    sys.exit(app.exec())