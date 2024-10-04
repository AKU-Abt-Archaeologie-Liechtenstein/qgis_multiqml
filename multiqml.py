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

import os
import tempfile

from qgis.PyQt.QtCore import *
from qgis.core import *
from qgis.PyQt.QtWidgets import (
    QDialog,
    QMessageBox,
    QFileDialog,
    QAbstractItemView,
)

from .multiqml_ui_base import Ui_MultiQmlForm


# create the dialog
class MultiQmlDlg(QDialog, Ui_MultiQmlForm):
    def __init__(self, parent, iface):
        self.iface = iface

        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.tmpQmlSrcList = []

        self.qgsVersion = unicode(Qgis.QGIS_VERSION_INT)
        self.mapLayers = list(QgsProject.instance().mapLayers().values())
        self.fileNameStyle = ""

        self.lvMapLayers.clicked.connect(self.doApplyStyleButtonEnabled)
        self.rbnRasterLayers.toggled.connect(self.doApplyStyleButtonEnabled)
        self.rbnVectorLayers.toggled.connect(self.doApplyStyleButtonEnabled)
        self.checkMakeDefault.stateChanged.connect(self.showWarning)

        self.loadMapLayers()
        self.readSettings()

    def showWarning(self):
        if self.checkMakeDefault.checkState() == Qt.Checked:
            res = QMessageBox.warning(
                self,
                QCoreApplication.translate("MultiQmlDlg", "MultiQML"),
                QCoreApplication.translate(
                    "MultiQmlDlg",
                    "Enabling this option will cause overwriting of any existing QML files. Are you sure?",
                ),
                QMessageBox.Yes | QMessageBox.No,
            )
            if res != QMessageBox.Yes:
                self.checkMakeDefault.setCheckState(Qt.Unchecked)
        return

    @pyqtSlot()
    def on_pbnApplyStyle_clicked(self):
        def isRasterQml():
            qmlFile = open(self.fileNameStyle, "r")
            line = qmlFile.readline()
            result = False
            while line != "":
                if "<rasterproperties>" in line or "<rasterrenderer" in line:
                    result = True
                    break
                line = qmlFile.readline()
            qmlFile.close()
            return result

        myLastUsedDir = self.settings.value("lastStyleDir")
        self.fileNameStyle = QFileDialog.getOpenFileName(
            self,
            QCoreApplication.translate("MultiQmlDlg", "Open style"),
            myLastUsedDir,
            QCoreApplication.translate(
                "MultiQmlDlg", "QGIS apply style file (*.qml)"
            ),
        )[0]

        if self.fileNameStyle != "":
            selected = self.lvMapLayers.selectedIndexes()
            layer = None
            for i in selected:
                layer = self.mapLayers[i.row()]

                if (layer.type() == QgsMapLayer.VectorLayer) and isRasterQml():
                    self.myPluginMessage(
                        QCoreApplication.translate(
                            "MultiQmlDlg",
                            f'Unable to apply raster qml style "{self.fileNameStyle}" to vector layer "{layer.name()}".',
                        ),
                        "critical",
                    )
                    continue
                elif (
                    layer.type() == QgsMapLayer.RasterLayer
                ) and not isRasterQml():
                    self.myPluginMessage(
                        QCoreApplication.translate(
                            "MultiQmlDlg",
                            f'Unable to apply vector qml style "{self.fileNameStyle}" to raster layer "{layer.name()}".',
                        ),
                        "critical",
                    )
                    continue

                message, isLoaded = layer.loadNamedStyle(self.fileNameStyle)

                if not isLoaded:
                    self.myPluginMessage(
                        QCoreApplication.translate(
                            "MultiQmlDlg",
                            f'Unable to apply qml style "{self.fileNameStyle}" to layer "{layer.name()}"\n{message}.',
                        ),
                        "critical",
                    )

                if self.checkMakeDefault.isChecked():
                    msg, res = layer.saveDefaultStyle()

                self.iface.layerTreeView().refreshLayerSymbology(layer.id())
                layer.triggerRepaint()

            # mapCanvas refresh is not working anymore
            # self.iface.mapCanvas().refresh()
            self.settings.setValue(
                "lastStyleDir", os.path.dirname(unicode(self.fileNameStyle))
            )
        else:
            self.myPluginMessage(
                QCoreApplication.translate(
                    "MultiQmlDlg", "A style was not applied."
                ),
                "information",
            )

    @pyqtSlot()
    def on_pbnRestoreDefaultStyle_clicked(self):
        selected = self.lvMapLayers.selectedIndexes()
        for i in selected:
            layer = self.mapLayers[i.row()]

            message, isLoaded = layer.loadNamedStyle(
                self.tmpQmlSrcList[i.row()]
            )
            if not isLoaded:
                self.myPluginMessage(
                    QCoreApplication.translate(
                        "MultiQmlDlg",
                        f'Unable to restory an initial style for layer "{layer.name()}"\n{message}.',
                    ),
                    "critical",
                )
            if self.checkMakeDefault.isChecked():
                msg, res = layer.saveDefaultStyle()
            self.iface.layerTreeView().refreshLayerSymbology(layer.id())
            self.iface.mapCanvas().refresh()

    @pyqtSlot()
    def on_pbnSelectAllLayers_clicked(self):
        self.lvMapLayers.selectAll()
        self.pbnSelectAllLayers.setEnabled(True)
        self.pbnApplyStyle.setEnabled(True)

    def loadMapLayers(self):
        layersNameList = []
        for i, layer in enumerate(self.mapLayers):
            layersNameList.append(layer.name())
            self.tmpQmlSrcList.append(tempfile.mktemp(".qml"))
            message, isSaved = layer.saveNamedStyle(self.tmpQmlSrcList[i])

        self.lvMapLayers.setModel(QStringListModel(layersNameList, self))
        self.lvMapLayers.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.lvMapLayers.setEditTriggers(QAbstractItemView.NoEditTriggers)

        if self.lvMapLayers.model().rowCount() == 0:
            self.pbnSelectAllLayers.setEnabled(False)

    @pyqtSlot()
    def on_pbnClose_clicked(self):
        self.writeSettings()
        self.close()

    def closeEvent(self, event):
        for i in range(len(self.mapLayers)):
            if os.path.isfile(self.tmpQmlSrcList[i]):
                os.remove(self.tmpQmlSrcList[i])
        event.accept()

    def doApplyStyleButtonEnabled(self):
        if len(self.lvMapLayers.selectedIndexes()) == 0:
            self.pbnApplyStyle.setEnabled(False)
        else:
            self.pbnApplyStyle.setEnabled(True)

    def on_rbnRasterLayers_toggled(self, checked):
        for i, layer in enumerate(self.mapLayers):
            idx = self.lvMapLayers.model().index(i, 0)
            layerName = self.lvMapLayers.model().data(idx, 0)
            for lyr in self.mapLayers:
                if lyr.name() == layerName:
                    break
            if checked and (layer.type() != QgsMapLayer.VectorLayer):
                self.lvMapLayers.setRowHidden(i, False)
            elif not checked and (layer.type() == QgsMapLayer.RasterLayer):
                self.lvMapLayers.setRowHidden(i, True)
            else:
                self.lvMapLayers.setRowHidden(i, True)

            if checked and (layer.type() != QgsMapLayer.VectorLayer):
                self.lvMapLayers.setRowHidden(i, False)
            elif not checked and (layer.type() == QgsMapLayer.RasterLayer):
                self.lvMapLayers.setRowHidden(i, True)
            else:
                self.lvMapLayers.setRowHidden(i, True)

    def on_rbnVectorLayers_toggled(self, checked):
        for i, layer in enumerate(self.mapLayers):
            idx = self.lvMapLayers.model().index(i, 0)
            layerName = self.lvMapLayers.model().data(idx, 0)
            for lyr in self.mapLayers:
                if lyr.name() == layerName:
                    break
            if checked and (layer.type() != QgsMapLayer.RasterLayer):
                self.lvMapLayers.setRowHidden(i, False)
            elif not checked and (layer.type() == QgsMapLayer.VectorLayer):
                self.lvMapLayers.setRowHidden(i, True)
            else:
                self.lvMapLayers.setRowHidden(i, True)

            if checked and (layer.type() != QgsMapLayer.RasterLayer):
                self.lvMapLayers.setRowHidden(i, False)
            elif not checked and (layer.type() == QgsMapLayer.VectorLayer):
                self.lvMapLayers.setRowHidden(i, True)
            else:
                self.lvMapLayers.setRowHidden(i, True)

    def readSettings(self):
        self.settings = QSettings("NextGIS", "MultiQml")
        self.resize(self.settings.value("size", QSize(330, 230)))
        # self.move(self.settings.value("pos", QPoint(0, 0)))  # May cause an error on first run
        self.rbnRasterLayers.setChecked(
            self.settings.value("isRasterChecked", True, type=bool)
        )
        self.rbnVectorLayers.setChecked(
            self.settings.value("isVectorChecked", False, type=bool)
        )
        # self.checkMakeDefault.setCheckState( self.settings.value( "saveDefault", 0, type=int ) )

    def writeSettings(self):
        self.settings = QSettings("NextGIS", "MultiQml")
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.settings.setValue(
            "isRasterChecked", self.rbnRasterLayers.isChecked()
        )
        self.settings.setValue(
            "isVectorChecked", self.rbnVectorLayers.isChecked()
        )
        # self.settings.setValue( "saveDefault", self.checkMakeDefault.checkState() )

    def myPluginMessage(self, msg, type):
        if type == "information":
            QMessageBox.information(
                self,
                QCoreApplication.translate("MultiQmlDlg", "Information"),
                msg,
            )
        elif type == "critical":
            QMessageBox.critical(
                self, QCoreApplication.translate("MultiQmlDlg", "Error"), msg
            )
