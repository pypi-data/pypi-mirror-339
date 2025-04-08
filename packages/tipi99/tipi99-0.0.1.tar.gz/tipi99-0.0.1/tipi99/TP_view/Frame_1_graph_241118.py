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


class Frame_1_graph(QtWidgets.QFrame):
    
    signal_fig_on_click = QtCore.pyqtSignal(MouseEvent)
    signal_fig_click_no_drag = QtCore.pyqtSignal(MouseEvent)
    signal_fig_click_drag = QtCore.pyqtSignal(MouseEvent)
    
    def __init__(self, model = None, debug = False):
        
        super().__init__()
        self.model = model
        self.debug = debug
        if self.debug: print("\nDebug mode\n")
        
        res_x = int(448/4) # Image in About
        res_y = int(300/4) # Image in About
        
        
        #Logo CP
        
        self.label_CP = QtWidgets.QLabel(self)
        path_CP = Path("logo_CP.jpg")
        _pixmap_CP = QtGui.QPixmap(str(Path(__file__).parent.resolve() / path_CP))
        
        self.pixmap_CP = _pixmap_CP.scaled(res_x, res_y, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        #self.pixmap_CP = _pixmap_CP
        
        self.label_CP.setScaledContents(True)
        self.label_CP.setPixmap(self.pixmap_CP)
        self.label_CP.resize(res_x, res_y)
        
        #Logo IMPMC
        
        self.label_IMPMC = QtWidgets.QLabel(self)
        path_IMPMC = Path("logo_IMPMC.jpg")  
        _pixmap_IMPMC = QtGui.QPixmap(str(Path(__file__).parent.resolve() / path_IMPMC))

        self.pixmap_IMPMC = _pixmap_IMPMC.scaled(res_x, res_y, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        #self.pixmap_IMPMC = _pixmap_IMPMC
        
        self.label_IMPMC.setScaledContents(True)
        self.label_IMPMC.setPixmap(self.pixmap_IMPMC)
        self.label_IMPMC.resize(res_x, res_y)
        
        self.fig_ref = [] #List of plot ref
        self.fig_ref_names = [] #List of plot names
        self.x_min_all = np.inf
        self.x_max_all = -np.inf
        self.y_min_all = np.inf
        self.y_max_all = -np.inf
        self.total_plot_n = 0 
        
        self.fig = plt.figure(figsize=(5, 5))
        self.canvas = FigureCanvas(self.fig)
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('button_release_event', self.off_click)
        
        self.navigationToolbar = NavigationToolbar(self.canvas, self, coordinates=True)
        self.ax = self.fig.add_subplot(111)
        self.ax.grid()
        self.x_moving_ref_left = 0 #Ref to detect drag
        self.y_moving_ref_left = 0 #Ref to detect drag
        #self.navigationToolbar.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        
        # show canvas
        self.canvas.show()
        
        # create main layout
        
        layout_V = QtWidgets.QVBoxLayout()
        
        layout_V.addWidget(self.canvas)
        
        
        layout_H = QtWidgets.QHBoxLayout()
        layout_H.addWidget(self.label_IMPMC)
        layout_H.addWidget(self.label_CP)
        layout_H.addWidget(self.navigationToolbar)
        
        
        layout_V.addLayout(layout_H)
        self.setLayout(layout_V)
        
        self.plot_ref = None
        self.data_x = None
        self.data_y = None
        self.plot_simple_calib_ref = None
        
        self.label_CP.setSizePolicy(QtWidgets .QSizePolicy.Fixed, QtWidgets .QSizePolicy.Fixed) #MinimumExpanding
        self.label_IMPMC.setSizePolicy(QtWidgets .QSizePolicy.Fixed, QtWidgets .QSizePolicy.Fixed) #MinimumExpanding
    
    def on_click(self, event):
        if self.debug: print('on_click')
        self.x_moving_ref_left = event.xdata
        self.y_moving_ref_left = event.ydata
        self.signal_fig_on_click.emit(event)
    
    def off_click(self, event):
        if self.debug: print('off_click')
        _x = event.xdata
        _y = event.ydata
        not_moved = ((self.x_moving_ref_left == _x) and (self.y_moving_ref_left == _y))
        if not_moved:
            self.signal_fig_click_no_drag.emit(event)
        else:
            self.signal_fig_click_drag.emit(event)
    
    def reset(self):
        self.ax.cla()
        self.fig_ref = []
        self.fig_ref_names = []
        self.total_plot_n = 0 
        
    def plot_data(self, data_x, data_y = None, label = None):
        self.reset()
        
        if data_y is None:
            data_y = data_x[:,1]
            data_x = data_x[:,0]
            
        
        self.ax.grid()
        #print(data_x.shape,data_y.shape)
        if label is not None:
            ref, = self.ax.plot(data_x, data_y, '-o', label = label)
        else:
            ref, = self.ax.plot(data_x, data_y, '-o')
        self.total_plot_n+= 1
        self.fig_ref.append(ref)
        self.fig_ref_names.append(label)
        if label is not None:
            leg = self.ax.legend()
            leg.set_draggable(True)
        self.canvas.draw()
    
    def delete_plot(self, element):
        if self.debug: print(f'pop {element}')
        _ = self.fig_ref.pop(element)
        _.remove()
        cancelled = self.fig_ref_names.pop(element)
        if cancelled is not None:
            leg = self.ax.legend()
            leg.set_draggable(True)
        self.autoscale_ax()
        self.canvas.draw()

    def add_plot(self, data_x, data_y = None, label = None):
        if data_y is None:
            data_y = data_x[:,1]
            data_x = data_x[:,0]
        i = self.total_plot_n
        #plot_label = f'Plot {i}'
        self.total_plot_n+= 1
        if label is not None:
            ref, = self.ax.plot(data_x, data_y, '-o', label = label)
        else:
            ref, = self.ax.plot(data_x, data_y, '-o')
        self.fig_ref.append(ref)
        self.fig_ref_names.append(label)
        if label is not None:
            leg = self.ax.legend()
            leg.set_draggable(True) 
        self.autoscale_ax()
        self.canvas.draw()
    
    def autoscale_ax(self):
        border = 0.1
        max_x = -np.inf
        max_y = -np.inf
        min_x = np.inf
        min_y = np.inf
        lines = self.ax.get_lines()
        for line in lines:
            x_data = line.get_xdata()
            y_data = line.get_ydata()
            max_x = max(max_x, x_data.max())
            max_y = max(max_y, y_data.max())
            min_x = min(min_x, x_data.min())
            min_y = min(min_y, y_data.min())
        
        border_x = (max_x - min_x)*border/2
        border_y = (max_y - min_y)*border/2
        self.ax.set_xlim(min_x-border_x, max_x+border_x)
        self.ax.set_ylim(min_y-border_y, max_y+border_y)
    
    def rescale_xy(self, event = None):
        x_min = self.x_min_all
        x_max = self.x_max_all
        x_range = (x_max -x_min)*0.05*np.array((-1,1))+np.array((x_min,x_max))
        self.ax_Spectro.set_xlim(x_range)
        if self.debug: print('Rescale x')
        y_min = self.intensities.min()
        y_max = self.intensities.max()
        y_range = (y_max -y_min)*0.05*np.array((-1,1))+np.array((y_min,y_max))
        self.ax_Spectro.set_ylim(y_range)
        if self.debug: print('Rescale y')
        
    def rescale_x(self):
        x_min = self.x_min_all
        x_max = self.x_max_all
        x_range = (x_max -x_min)*0.05*np.array((-1,1))+np.array((x_min,x_max))
        self.ax_Spectro.set_xlim(x_range)
        if self.debug: print('Rescale x')
    
    
    def rescale_y(self):
        y_min = self.y_min_all
        y_max = self.y_max_all
        y_range = (y_max -y_min)*0.05*np.array((-1,1))+np.array((y_min,y_max))
        self.ax.set_ylim(y_range)
        self.canvas.draw()
        

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("""
                      * {
                          font-size: 15px;
                    }
                      """)
 
    window = Frame_1_graph()


    window.show()
    sys.exit(app.exec())