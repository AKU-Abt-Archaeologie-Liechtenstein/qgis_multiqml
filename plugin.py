# -*- coding: utf-8 -*-

#******************************************************************************
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
#******************************************************************************

import gettext

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from multiqml import MultiQmlDlg

import resources_rc

class MultiQmlPlugin():
  def __init__( self, iface ):
    self.iface = iface
    
    userPluginPath = QFileInfo(
            QgsApplication.qgisUserDbFilePath()).path() + \
            '/python/plugins/multiqml'
    systemPluginPath = QgsApplication.prefixPath() + \
            '/python/plugins/multiqml'

    overrideLocale = QSettings().value('locale/overrideFlag', False,
                                       type=bool)
    if not overrideLocale:
        localeFullName = QLocale.system().name()
    else:
        localeFullName = QSettings().value('locale/userLocale', '')

    if QFileInfo(userPluginPath).exists():
        translationPath = userPluginPath + '/i18n/multiqml_' + \
                          localeFullName + '.qm'
    else:
        translationPath = systemPluginPath + '/i18n/multiqml_' + \
                          localeFullName + '.qm'

    self.localePath = translationPath
    if QFileInfo(self.localePath).exists():
        self.translator = QTranslator()
        self.translator.load(self.localePath)
        QCoreApplication.installTranslator(self.translator)
        
  def initGui( self ):
    self.actionRun = QAction( QIcon( ":/plugins/multiqml/icon.png" ),\
      QApplication.translate("MultiQmlPlugin", "MultiQml" ), self.iface.mainWindow() )
    self.actionRun.setWhatsThis( QApplication.translate("MultiQmlPlugin", "Apply single qml style to multiple raster or vector layers") )
    self.actionAbout = QAction( QApplication.translate("MultiQmlPlugin", "About" ), self.iface.mainWindow() )

    QObject.connect( self.actionRun, SIGNAL( "triggered()" ), self.run )
    QObject.connect( self.actionAbout, SIGNAL( "triggered()" ), self.about )

    self.iface.addToolBarIcon(self.actionRun)
    self.iface.addPluginToMenu( QApplication.translate("MultiQmlPlugin", "&MultiQml" ), self.actionRun )
    self.iface.addPluginToMenu( QApplication.translate("MultiQmlPlugin", "&MultiQml" ), self.actionAbout )

    self.isMultiQmlRun = False

  def unload( self ):
    self.iface.removePluginMenu( QApplication.translate("MultiQmlPlugin", "&MultiQml" ), self.actionRun )
    self.iface.removePluginMenu( QApplication.translate("MultiQmlPlugin", "&MultiQml" ), self.actionAbout )
    self.iface.removeToolBarIcon(self.actionRun)

  def run( self ):
    if not self.isMultiQmlRun:
      self.isMultiQmlRun = True
      dlgMain = MultiQmlDlg( self.iface.mainWindow(), self.iface )
      dlgMain.show()
      dlgMain.exec_()
      self.isMultiQmlRun = False

  def about( self ):
    dlgAbout = QDialog()
    dlgAbout.setWindowTitle( QApplication.translate("MultiQmlPlugin", "About", "Window title") )
    lines = QVBoxLayout( dlgAbout )
    #add version back
    lines.addWidget( QLabel( QApplication.translate("MultiQmlPlugin", "<b>MultiQml (Version %1):</b>" ) ) )
    lines.addWidget( QLabel( QApplication.translate("MultiQmlPlugin", "    This plugin takes single qml style and\napplies it to multiple raster or vector layers" ) ) )
    lines.addWidget( QLabel( QApplication.translate("MultiQmlPlugin", "<b>Developers:</b>" ) ) )
    lines.addWidget( QLabel( "    Lynx (alex-86p@yandex.ru)" ) )
    lines.addWidget( QLabel( "    Maxim Dubinin (sim@gis-lab.info)" ) )
    lines.addWidget( QLabel( "    Alexander Bruy" ) )
    lines.addWidget( QLabel( QApplication.translate("MultiQmlPlugin", "<b>Link:</b>") ) )
    linkPage = QLabel( QApplication.translate("MultiQmlPlugin", "<a href=\"http://gis-lab.info/qa/qgis-multiqml-eng.html\">http://gis-lab.info/qa/qgis-multiqml-eng.html</a>" ) )
    linkPage.setOpenExternalLinks( True )
    lines.addWidget( linkPage )
    linkBugs = QLabel( QApplication.translate("MultiQmlPlugin", "<a href=\"https://github.com/nextgis/MultiQML\">https://github.com/nextgis/MultiQML</a>" ) )
    linkBugs.setOpenExternalLinks( True )
    lines.addWidget( linkBugs )

    pbnClose = QPushButton(QApplication.translate("MultiQmlPlugin", "Close"))
    lines.addWidget(pbnClose)

    QObject.connect(pbnClose, SIGNAL("clicked()"), dlgAbout, SLOT("close()"))

    dlgAbout.exec_()

