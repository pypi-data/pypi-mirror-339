# TiPi99
Graphical user interface to configure the ![Autonomous Temperature Pressure Sensor TP99](https://github.com/CelluleProjet/TiPi99#about-the-project) and download the registered data.

## Install

1) Download and install [Miniforge](https://github.com/conda-forge/miniforge)  
   Anaconda and Miniconda work the same way, but Miniconda uses free and openly-licensed packages from the conda-forge project by default. [More info.](https://www.sens.buffalo.edu/software/conda)

2) From miniforge/anaconda prompt (windows) or terminal (Ubuntu & MAC) create a virtual environment with name "my_env":

```bash
conda create -n  my_env pip
```

3) Activate the virtual environment with
```bash
conda activate my_env
```

4) Install TiPi99 with:

```bash

pip install TiPi99
```

5) Launch TiPi99:

```bash

TiPi99
```
## Shortcut

In windows the TiPi99.exe can be found in the virtual environment Scripts folder, usually something like:  
- C:\Users\username\anaconda3\envs\my_env\Scripts
- C:\Users\username\miniconda\envs\my_env\Scripts

To check where the virtual environment has been installed:

```bash

conda env list 
```

# Manual

## 'Serial' Tab: Starting page
> [!Caution]
> The _TP99 device_ once turned on automatically searches for a serial connection for 5 seconds during which the device LED flashes. If the serial connection is not found, the device enters the 'logger' mode and starts recording new data, **overwriting** the old data in memory. For this reason, it is necessary to start the search of the _TP99 device_ **before** connecting it by USB cable.

![Tab_1_Serial_Connect](https://github.com/user-attachments/assets/4ed5ae32-a4a6-447d-84db-d9b1866fce52)


  - **Search TP99**
    - starts the automatic search for the _TP99 device_ and wait for the USB cable connection.  

  - **Update Port List**
    - for debug purpose, it updates and show all the COM ports available in the pc. By clicking on the name of the displayed COM you can see the details.  

## 'Serial' Tab: Device Found

![Tab_1_Serial_Connected](https://github.com/user-attachments/assets/cf0dfd96-a96d-40b7-8f73-bc427c677b1d)


  - **Test Detector**
    - read T and P from the sensor  

  - **Test LED**
    - turn the device LED ON/OFF  

  - **Set Name**
    - shows the name of the connected device (maximum length 8 characters). The name is saved in the device memory and can be changed.  

  - **Set log time in sec**
    - shows the time between each measurement in seconds and the total available duration (depends on device memory).  

  - **Set battery date**
    - shows the date the device battery was installed. Must be updated when changing the battery.  

  - **Download Device Memory**
    - download the data saved in the device memory. The data are showed in the 'Data' Tab and plotted in the 'Plot T', 'Plot P' and 'Plot TP' tabs
   
  - **Save Data**
    - save the data to file using 3 formats: csv, txt and npy ([numpy format](https://numpy.org/doc/stable/reference/generated/numpy.lib.format.html))

  - **Erase Device Memory**
    - Erase the memory of the device, to be used to clear old data from a previous measurement from memory, so that it does not interfere with the data from a more recent measurement.

> [!IMPORTANT]
> Data can also be imported from previously saved files, see the menu.  
> The file containing the test measurement data, performed up to around 300 bar and used for the following figures, is located in the "example" folder.

## 'Calc' Tab
Calculator to estimate the optimal log times to use for a measurement.  

![Tab_2_Calc](https://github.com/user-attachments/assets/4e688418-46c6-4cfb-ae38-6e4a644c24ab)


The "Start" and "Stop" tabs allow you to choose the start and end dates of the measurement on the calendars. The hour, minutes and seconds can be further added in the appropriate input areas.
  - **Calc**
    - estimate the two closest log times

The two log times are displayed with their corresponding end dates next to them.

## 'Data' Tab

Displays loaded data (from device memory or file) in table form.  
The starting date of the Date column can be changed by the [Set new starting date](https://github.com/CelluleProjet/TiPi99#set-or-change-the-initial-measurements-date) in the 'Plot T' Tab.

![Tab_3_Data](https://github.com/user-attachments/assets/7b0d06ce-2799-4370-b7b3-0997ebeb015d)


## 'Plot T' Tab
Displays the temperature and shows the plot commands relative to the time axis.  

![Tab_4_PlotT](https://github.com/user-attachments/assets/a46f90e3-8d87-424f-a6a7-03ef2876ea97)



### X scale available options
  - **Elapsed**: elapsed time in seconds / minutes / hours or days
  - **Date**: dates reported in the Table

  
### Set or change the initial measurements date
  - **Date**: it allows the selection of the measurement start date using a calendar
  - **Epoch**: it allows the selection of the measurement start date using the [Unix epoch time](https://www.epochconverter.com/) (number of seconds elapsed since January 1, 1970).
  - **Set new starting date**: Updates the Date columns in the 'Data' tab and the X axis of all the plots


## 'Plot P' and 'Plot TP' Tabs
- **Plot P**
  - Displays the pressure on the time axis selected in the 'Plot P' Tab.
  
![Tab_5_PlotP](https://github.com/user-attachments/assets/24405ffa-78d9-4175-9da6-20568c38304d)

 
- **Plot TP**
  - Displays the temperature and the pressure on the time axis selected in the 'Plot P' Tab.

![Tab_6_plotTP](https://github.com/user-attachments/assets/8acd711d-a3b2-47c5-ba9f-98ffcd5aa270)




## Menu

**File**  
- Open File Ctrl + O
- Quit  

**Edit**  
- Fonts Size  

**Help**  
- About  

# Author

**Yiuri Garino**  
- Yiuri.Garino@cnrs.fr  

<img src="https://github.com/CelluleProjet/Rubycond/assets/83216683/b728fe64-2752-4ecd-843b-09d335cf4f93" width="100" height="100">
<img src="https://github.com/CelluleProjet/Rubycond/assets/83216683/0a81ce1f-089f-49d8-ae65-d19af8078492" width="100" height="100">

# License
**TiPi99**

Copyright (c) 2022-2024 Yiuri Garino

**TiPi99** is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

# Release notes

Version 0.0.1  

# About the Project

## Title  
- Capteur Autonome Température Pression – TP99

## Description  
- TP99 is an autonomous temperature pressure sensor that can operate up to 3000 m depth in waters between 2 and 50°C. Although several Conductivity Temperature Depth (CTD) sensors are commercially available, the latter have large dimensions making their use
restrictive, with a relatively high maintenance cost, requiring regular intervention from the manufacturer. The development of a deep-sea PT sensor, miniaturized and financially accessible, would undoubtedly find opportunities in many areas of deep oceanography, including the different disciplines (biology, geology...) that are now booming.  

## Funding  
- [Réseau de technologie des hautes pressions (Réseau HP)](https://reseauhp.org/idt-initiatives-de-developpement-de-technologies)

## PI  
- Bruce Shillito  (UMR BOREA - MNHN, CNRS 8067, SU, IRD 207, UA)

## Mechanics  
- Louis Amand: Louis.Amand@sorbonne-universite.fr
   
## Electronics  
- Marc Morand: Marc.Morand@sorbonne-universite.fr

## Software  
- Yiuri Garino: Yiuri.Garino@sorbonne-universite.fr
  
<img src="https://github.com/CelluleProjet/Rubycond/assets/83216683/b728fe64-2752-4ecd-843b-09d335cf4f93" width="100" height="100">
<img src="https://github.com/CelluleProjet/Rubycond/assets/83216683/0a81ce1f-089f-49d8-ae65-d19af8078492" width="100" height="100">

[Cellule Projet](http://impmc.sorbonne-universite.fr/fr/plateformes-et-equipements/cellule-projet.html) @ [IMPMC](http://impmc.sorbonne-universite.fr/en/index.html)

![XiaoBoardTP99_PM](https://github.com/user-attachments/assets/61878889-8bb4-4fe9-a144-9dfef88ade99)
*PCB design: Marc Morand*

![Louis_Amand](https://github.com/user-attachments/assets/901f7da3-6c96-4197-b273-f784045f326f)
*CAD model: Louis Amand*

      




