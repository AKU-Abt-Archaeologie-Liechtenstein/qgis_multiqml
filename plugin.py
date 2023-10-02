# -*- coding: utf-8 -*-

# ******************************************************************************
#
# MultiQML
# ---------------------------------------------------------
# Apply uniform style from QML file to multiple raster or vector layers
#
# Copyright (C) 2008-2014 NextGIS (info@nextgis.org)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/licenses/>. You can also obtain it by writing
# to the Free Software Foundation, 51 Franklin Street, Suite 500 Boston,
# MA 02110-1335 USA.
#
# ******************************************************************************
from configparser import ConfigParser

import os

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import (QAction,
                                 QApplication,
                                 QLabel,
                                 QDialog,
                                 QVBoxLayout,
                                 QPushButton,
                                 )

from .multiqml import MultiQmlDlg
from . import about_dialog

from . import resources


class MultiQmlPlugin():
    def __init__(self, iface):
        self.iface = iface

        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        self.localePath = os.path.join(
            self.plugin_dir,
            'i18n',
            'multiqml_{}.qm'.format(locale))

        if QFileInfo(self.localePath).exists():
            self.translator = QTranslator()
            self.translator.load(self.localePath)
            QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        self.actionRun = QAction(QIcon(":/plugins/multiqml/icon.png"), \
                                 QApplication.translate("MultiQmlPlugin", "MultiQml"), self.iface.mainWindow())
        self.actionRun.setWhatsThis(
            QApplication.translate("MultiQmlPlugin", "Apply single qml style to multiple raster or vector layers"))
        self.actionAbout = QAction(QApplication.translate("MultiQmlPlugin", "About"), self.iface.mainWindow())

        self.actionRun.triggered.connect(self.run)
        self.actionAbout.triggered.connect(self.about)

        self.iface.addToolBarIcon(self.actionRun)
        self.iface.addPluginToMenu(QApplication.translate("MultiQmlPlugin", "&MultiQml"), self.actionRun)
        self.iface.addPluginToMenu(QApplication.translate("MultiQmlPlugin", "&MultiQml"), self.actionAbout)

        self.isMultiQmlRun = False

    def unload(self):
        self.iface.removePluginMenu(QApplication.translate("MultiQmlPlugin", "&MultiQml"), self.actionRun)
        self.iface.removePluginMenu(QApplication.translate("MultiQmlPlugin", "&MultiQml"), self.actionAbout)
        self.iface.removeToolBarIcon(self.actionRun)

    def run(self):
        if not self.isMultiQmlRun:
            self.isMultiQmlRun = True
            dlgMain = MultiQmlDlg(self.iface.mainWindow(), self.iface)
            dlgMain.show()
            dlgMain.exec_()
            self.isMultiQmlRun = False

    def about(self):
        dlg = about_dialog.AboutDialog(os.path.basename(self.plugin_dir))
        dlg.exec_()

    def get_version(self):
        try:
            CURR_PATH = os.path.dirname(__file__)
            cp = ConfigParser()
            cp.readfp(open(os.path.join(CURR_PATH, 'metadata.txt')))
            return cp.get('general', 'version')
        except:
            return '?'
