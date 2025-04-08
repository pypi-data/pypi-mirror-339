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

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from pathlib import Path 
import os
 
class about(QtWidgets.QWidget):
    def __init__(self, name = 'Default', version = '0.0.1', relese = '700101'):
        
        super().__init__()
        self.name = name
        self.version = version
        self.release = relese
        
        self.setWindowTitle('About ' + self.name)
        
        self.url_github = 'https://github.com/CelluleProjet/TiPi99'
        self.url_github_TP99 = 'https://github.com/CelluleProjet/TiPi99#about-the-project'
        self.url_impmc = 'https://impmc.sorbonne-universite.fr/fr/index.html'
        self.url_CP = 'https://impmc.sorbonne-universite.fr/fr/plateformes-et-equipements/cellule-projet.html'
        
        
        self.licese = f''' 
<html>
<body>
<h1><br>{self.name}</h1>
<table><tr><td style="padding-left: 1.5em;">
<h3><br>
Copyright (C) 2024-2025 Yiuri GARINO
</h3></td></tr></table>
<br>
<h3>
GNU General Public License Version 3 (GPLv3)
<br>
<br>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
<br><br>
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
<br><br>
You should have received a copy of the GNU General Public License
along with this program.  If not, see <a href="https://www.gnu.org/licenses/">https://www.gnu.org/licenses/</a>
<br>
</h3>
</body>
</html>
        '''
#<https://www.gnu.org/licenses/>.
        self.overview = f'''<!DOCTYPE html>
<html>
<body>

<h1><br>{self.name}</h1>
<table><tr><td style="padding-left: 1.5em;">
<h3><br>Graphical user interface to configure the <a href="{self.url_github_TP99}">Autonomous Temperature Pressure Sensor TP99</a> and download the registered data.
</h3></td></tr></table>
<h3>Version {self.version} Release {self.release}
<br>
<table><tr><td style="padding-left: 1.5em;">
<a href="{self.url_github}">Manual and Download</a> 
</h3></td></tr></table>

<h2>Author: Yiuri GARINO</h2>
<table><tr><td style="padding-left: 1.5em;">
<h3><br>Contact: <a href="mailto:yiuri.garino@cnrs.fr">yiuri.garino@cnrs.fr</a>
<br><br>
</h3>
</td></tr></table>


</body>
</html>'''
        self.text_link_Cp = f'''<!DOCTYPE html>
<html>
<body>
<h3>
<br>
<a href="{self.url_CP}">Cellule Projet</a>
<br>
</h3>
</body>
</html>'''
        self.text_link_IMPMC = f'''<!DOCTYPE html>
<html>
<body>
<h3>
<br>
<a href="{self.url_impmc}">IMPMC</a>
<br>
</h3>
</body>
</html>'''
        tabs = QtWidgets.QTabWidget()
        script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        pixmap_1_path = str(script_dir / 'logo_CP_Scaled.png')
        pixmap_2_path = str(script_dir / 'logo_IMPMC_Scaled.png')
        pixmap_1 = QtGui.QPixmap(pixmap_1_path) #.scaledToWidth(128) #scaledToHeight(64)
        pixmap_2 = QtGui.QPixmap(pixmap_2_path) #.scaledToWidth(128) #scaledToHeight(64)
        
        layout_overwiew = QtWidgets.QGridLayout()
        layout_license = QtWidgets.QVBoxLayout()
        layout_logo = QtWidgets.QVBoxLayout()
        
        self.label_1 = QtWidgets.QLabel()
        self.label_1.setPixmap(pixmap_1)
        self.label_1.resize(pixmap_1.width(),
                          pixmap_1.height())
        
        self.label_2 = QtWidgets.QLabel()
        self.label_2.setPixmap(pixmap_2)
        self.label_2.resize(pixmap_2.width(),
                          pixmap_1.height())
        
        self.label_1_link = QtWidgets.QLabel()
        self.label_1_link.setText(self.text_link_Cp)
        self.label_1_link.setTextFormat(QtCore.Qt.RichText)
        self.label_1_link.setWordWrap(True)
        self.label_1_link.setAlignment(QtCore.Qt.AlignTop)
        self.label_1_link.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.label_1_link.setOpenExternalLinks(True)
        
        self.label_2_link = QtWidgets.QLabel()
        self.label_2_link.setText(self.text_link_IMPMC)
        self.label_2_link.setTextFormat(QtCore.Qt.RichText)
        self.label_2_link.setWordWrap(True)
        self.label_2_link.setAlignment(QtCore.Qt.AlignTop)
        self.label_2_link.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.label_2_link.setOpenExternalLinks(True)
        
        self.label_license = QtWidgets.QLabel()
        self.label_license.setText(self.licese)
        self.label_license.setTextFormat(QtCore.Qt.RichText)
        self.label_license.setWordWrap(True)
        self.label_license.setAlignment(QtCore.Qt.AlignTop)
        self.label_license.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.label_license.setOpenExternalLinks(True)
        
        self.label_overview = QtWidgets.QLabel()   #QTextEdit
        self.label_overview.setText(self.overview)
        self.label_overview.setTextFormat(QtCore.Qt.RichText)
        self.label_overview.setWordWrap(True)
        self.label_overview.setAlignment(QtCore.Qt.AlignTop)
        self.label_overview.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.label_overview.setOpenExternalLinks(True)
        
        
        layout_logo.addWidget(self.label_1, alignment=QtCore.Qt.AlignCenter)
        layout_logo.addWidget(self.label_1_link, alignment=QtCore.Qt.AlignCenter)
        layout_logo.addWidget(self.label_2, alignment=QtCore.Qt.AlignCenter)
        layout_logo.addWidget(self.label_2_link, alignment=QtCore.Qt.AlignCenter)
        layout_logo.addStretch()
        #layout_logo.setAlignment(QtCore.Qt.AlignCenter)
        
        layout_license.addWidget(self.label_license)
        layout_overwiew.addWidget(self.label_overview)

        widget_1 = QtWidgets.QWidget()
        widget_1.setLayout(layout_overwiew)
        
        widget_2 = QtWidgets.QWidget()
        widget_2.setLayout(layout_license)
        
        self.tab_1 = tabs.addTab(widget_1, "Overwiew")
        self.tab_2 = tabs.addTab(widget_2, "Legal")
        
        layout = QtWidgets.QGridLayout()
        layout.addLayout(layout_logo, 0, 0)
        layout.addWidget(tabs, 0, 1)
        
        
        self.setLayout(layout)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("""
                      * {
                          font-size: 15px;
                    }
                      
                      """)

    window = about()
    window.show()
    
    sys.exit(app.exec())