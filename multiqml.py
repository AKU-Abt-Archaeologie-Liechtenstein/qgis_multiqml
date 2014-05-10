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

import os
import sys
import tempfile
import gettext

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from ui_multiqml import Ui_MultiQmlForm

# create the dialog
class MultiQmlDlg(QDialog, Ui_MultiQmlForm):
  def __init__(self, parent, iface):
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
  
    QDialog.__init__(self, parent)
    self.setupUi(self)

    self.tmpQmlSrcList = []
    
    self.qgsVersion = unicode(QGis.QGIS_VERSION_INT)
    self.mapLayers = self.iface.legendInterface().layers()
    self.fileNameStyle = ""

    QObject.connect( self.lvMapLayers, SIGNAL( "clicked( const QModelIndex & )" ), self.doApplyStyleButtonEnabled )
    QObject.connect( self.rbnRasterLayers, SIGNAL( "toggled( bool )" ), self.doApplyStyleButtonEnabled )
    QObject.connect( self.rbnVectorLayers, SIGNAL( "toggled( bool )" ), self.doApplyStyleButtonEnabled )
    QObject.connect( self.checkMakeDefault, SIGNAL( "stateChanged( int )" ), self.showWarning )

    self.loadMapLayers()
    self.readSettings()

  def showWarning( self ):
    #if self.checkMakeDefault.checkState() == Qt.Checked:
    # res = QMessageBox.warning( self, self.tr( "MultiQML" ),
    #                    self.tr( "Enabling this option will cause overwriting of any existing QML files. Are you sure?" ),
    #                    QMessageBox.Yes | QMessageBox.No )
    # if res != QMessageBox.Yes:
    #   self.checkMakeDefault.setCheckState( Qt.Unchecked )
    return

  @pyqtSignature( "" )
  def on_pbnApplyStyle_clicked(self):
    def isRasterQml():
      qmlFile = open( self.fileNameStyle, "rb" )
      line = qmlFile.readline()
      result = False
      while line != "":
        if "<rasterproperties>" in line:
          result = True
          break
        line = qmlFile.readline()
      qmlFile.close()
      return result

    myLastUsedDir = self.settings.value( "lastStyleDir" )
    self.fileNameStyle = QFileDialog.getOpenFileName(self, QCoreApplication.translate("MultiQmlDlg", "Open style"), myLastUsedDir, QCoreApplication.translate("MultiQmlDlg", "QGIS apply style file (*.qml)"))
    
    if self.fileNameStyle != "":
      selected = self.lvMapLayers.selectedIndexes()
      layer = None
      for i in selected:
        layer = self.mapLayers[i.row()]

        if ( layer.type() == QgsMapLayer.VectorLayer ) and isRasterQml():
          self.myPluginMessage( QCoreApplication.translate("MultiQmlDlg", "Unable to apply raster qml style \"%1\" to vector layer \"%2\".")\
            .arg(self.fileNameStyle).arg(layer.name()), "critical" )
          continue
        elif ( layer.type() == QgsMapLayer.RasterLayer ) and not isRasterQml():
          self.myPluginMessage( QCoreApplication.translate("MultiQmlDlg", "Unable to apply vector qml style \"%1\" to raster layer \"%2\".")\
            .arg(self.fileNameStyle).arg(layer.name()), "critical" )
          continue

        message, isLoaded = layer.loadNamedStyle(self.fileNameStyle)

        if not isLoaded:
          self.myPluginMessage( QCoreApplication.translate("MultiQmlDlg", "Unable to apply qml style \"%1\" to layer \"%2\"\n%3.")\
            .arg(self.fileNameStyle).arg(layer.name()).arg(message), "critical" )

        if self.checkMakeDefault.isChecked():
          msg, res = layer.saveDefaultStyle()

        self.iface.legendInterface().refreshLayerSymbology( layer )

      self.iface.mapCanvas().refresh()
      self.settings.setValue( "lastStyleDir", os.path.dirname( unicode( self.fileNameStyle ) ) )
    else:
      self.myPluginMessage( QCoreApplication.translate("MultiQmlDlg", "A style was not applied." ), "information" )

  @pyqtSignature( "" )
  def on_pbnRestoreDefaultStyle_clicked(self):
    selected = self.lvMapLayers.selectedIndexes()
    for i in selected:
      layer = self.mapLayers[i.row()]
      
      message, isLoaded = layer.loadNamedStyle(self.tmpQmlSrcList[i.row()])
      if not isLoaded: self.myPluginMessage( QCoreApplication.translate("MultiQmlDlg",  "Unable to restory an initial style for layer \"%1\"\n%2.")\
        .arg(layer.name()).arg(message), "critical" )
      if self.checkMakeDefault.isChecked():
        msg, res = layer.saveDefaultStyle()
      self.iface.legendInterface().refreshLayerSymbology( layer )
      self.iface.mapCanvas().refresh()

  @pyqtSignature( "" )
  def on_pbnSelectAllLayers_clicked(self):
    self.lvMapLayers.selectAll()
    self.pbnSelectAllLayers.setEnabled( True )
    self.pbnApplyStyle.setEnabled( True )

  def loadMapLayers( self ):
    layersNameList = []
    for i in range( len( self.mapLayers ) ):
      layersNameList.append( self.mapLayers[i].name() )
      self.tmpQmlSrcList.append( tempfile.mktemp( '.qml' ) )
      message, isSaved = self.mapLayers[i].saveNamedStyle(self.tmpQmlSrcList[i])

    self.lvMapLayers.setModel( QStringListModel( layersNameList, self ) )
    self.lvMapLayers.setSelectionMode(QAbstractItemView.ExtendedSelection)
    self.lvMapLayers.setEditTriggers( QAbstractItemView.NoEditTriggers )

    if self.lvMapLayers.model().rowCount() == 0:
      self.pbnSelectAllLayers.setEnabled( False )

  @pyqtSignature( "" )
  def on_pbnClose_clicked(self):
    self.writeSettings()
    self.close()

  def closeEvent( self, event ):
    for i in range( len( self.mapLayers ) ):
      os.remove( self.tmpQmlSrcList[i] )
    event.accept()

  def doApplyStyleButtonEnabled( self ):
    if len( self.lvMapLayers.selectedIndexes() ) == 0:
      self.pbnApplyStyle.setEnabled( False )
    else:
      self.pbnApplyStyle.setEnabled( True )

  def on_rbnRasterLayers_toggled( self, checked ):
    for i in range( len( self.mapLayers ) ):
        idx = self.lvMapLayers.model().index( i, 0 )
        layerName = self.lvMapLayers.model().data( idx, 0 )
        for j in range( len( self.mapLayers ) ):
          if self.mapLayers[j].name() == layerName:
            break
        if checked and ( self.mapLayers[i].type() != QgsMapLayer.VectorLayer ):
          self.lvMapLayers.setRowHidden( i, False )
        elif not checked and ( self.mapLayers[i].type() == QgsMapLayer.RasterLayer ):
          self.lvMapLayers.setRowHidden( i, True )
        else:
          self.lvMapLayers.setRowHidden( i, True )

        if checked and ( self.mapLayers[i].type() != QgsMapLayer.VectorLayer ):
          self.lvMapLayers.setRowHidden( i, False )
        elif not checked and ( self.mapLayers[i].type() == QgsMapLayer.RasterLayer ):
          self.lvMapLayers.setRowHidden( i, True )
        else:
          self.lvMapLayers.setRowHidden( i, True )

  def on_rbnVectorLayers_toggled( self, checked ):
    for i in range( len( self.mapLayers ) ):
        idx = self.lvMapLayers.model().index( i, 0 )
        layerName = self.lvMapLayers.model().data( idx, 0 )
        for j in range( len( self.mapLayers ) ):
          if self.mapLayers[j].name() == layerName:
            break
        if checked and ( self.mapLayers[i].type() != QgsMapLayer.RasterLayer ):
          self.lvMapLayers.setRowHidden( i, False )
        elif not checked and ( self.mapLayers[i].type() == QgsMapLayer.VectorLayer ):
          self.lvMapLayers.setRowHidden( i, True )
        else:
          self.lvMapLayers.setRowHidden( i, True )

        if checked and ( self.mapLayers[i].type() != QgsMapLayer.RasterLayer ):
          self.lvMapLayers.setRowHidden( i, False )
        elif not checked and ( self.mapLayers[i].type() == QgsMapLayer.VectorLayer ):
          self.lvMapLayers.setRowHidden( i, True )
        else:
          self.lvMapLayers.setRowHidden( i, True )

  def readSettings(self):
    self.settings = QSettings( "NextGIS", "MultiQml" )
    self.resize( self.settings.value( "size", QSize( 330, 230 ) ) )
    self.move( self.settings.value( "pos", QPoint( 0, 0 ) ) )
    self.rbnRasterLayers.setChecked( self.settings.value( "isRasterChecked", True, type=bool ) )
    self.rbnVectorLayers.setChecked( self.settings.value( "isVectorChecked", False, type=bool ) )
    self.checkMakeDefault.setCheckState( self.settings.value( "saveDefault", 0 ) )

  def writeSettings(self):
    self.settings = QSettings( "NextGIS", "MultiQml" )
    self.settings.setValue( "size", self.size() )
    self.settings.setValue( "pos", self.pos() )
    self.settings.setValue( "isRasterChecked", self.rbnRasterLayers.isChecked())
    self.settings.setValue( "isVectorChecked", self.rbnVectorLayers.isChecked())
    self.settings.setValue( "saveDefault", self.checkMakeDefault.checkState() )

  def myPluginMessage( self, msg, type ):
    if type == "information":
      QMessageBox.information(self, QCoreApplication.translate("MultiQmlDlg", "Information"), msg )
    elif type == "critical":
      QMessageBox.critical(self, QCoreApplication.translate("MultiQmlDlg", "Error"), msg )
