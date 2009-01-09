# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'multiqml.ui'
#
# Created: Fri Jan  9 23:27:30 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MultiQmlForm(object):
    def setupUi(self, MultiQmlForm):
        MultiQmlForm.setObjectName("MultiQmlForm")
        MultiQmlForm.resize(330, 230)
        self.gridLayout = QtGui.QGridLayout(MultiQmlForm)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(MultiQmlForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lvMapLayers = QtGui.QListView(MultiQmlForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lvMapLayers.sizePolicy().hasHeightForWidth())
        self.lvMapLayers.setSizePolicy(sizePolicy)
        self.lvMapLayers.setMaximumSize(QtCore.QSize(180, 16777215))
        self.lvMapLayers.setObjectName("lvMapLayers")
        self.gridLayout.addWidget(self.lvMapLayers, 1, 0, 5, 1)
        self.pbnApplyStyle = QtGui.QPushButton(MultiQmlForm)
        self.pbnApplyStyle.setObjectName("pbnApplyStyle")
        self.gridLayout.addWidget(self.pbnApplyStyle, 1, 1, 1, 1)
        self.pbnRestoreDefaultStyle = QtGui.QPushButton(MultiQmlForm)
        self.pbnRestoreDefaultStyle.setObjectName("pbnRestoreDefaultStyle")
        self.gridLayout.addWidget(self.pbnRestoreDefaultStyle, 2, 1, 1, 1)
        self.pbnLoadColormapFromBand = QtGui.QPushButton(MultiQmlForm)
        self.pbnLoadColormapFromBand.setObjectName("pbnLoadColormapFromBand")
        self.gridLayout.addWidget(self.pbnLoadColormapFromBand, 3, 1, 1, 1)
        self.pbnSelectAllLayers = QtGui.QPushButton(MultiQmlForm)
        self.pbnSelectAllLayers.setObjectName("pbnSelectAllLayers")
        self.gridLayout.addWidget(self.pbnSelectAllLayers, 4, 1, 1, 1)
        self.pbnClose = QtGui.QPushButton(MultiQmlForm)
        self.pbnClose.setObjectName("pbnClose")
        self.gridLayout.addWidget(self.pbnClose, 5, 1, 1, 1)
        self.label.setBuddy(self.lvMapLayers)

        self.retranslateUi(MultiQmlForm)
        QtCore.QMetaObject.connectSlotsByName(MultiQmlForm)
        MultiQmlForm.setTabOrder(self.pbnApplyStyle, self.lvMapLayers)
        MultiQmlForm.setTabOrder(self.lvMapLayers, self.pbnRestoreDefaultStyle)
        MultiQmlForm.setTabOrder(self.pbnRestoreDefaultStyle, self.pbnClose)

    def retranslateUi(self, MultiQmlForm):
        MultiQmlForm.setWindowTitle(QtGui.QApplication.translate("MultiQmlForm", "Assign style", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MultiQmlForm", "Map layers:", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnApplyStyle.setText(QtGui.QApplication.translate("MultiQmlForm", "Apply style ...", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnRestoreDefaultStyle.setText(QtGui.QApplication.translate("MultiQmlForm", "Restore initial style", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnLoadColormapFromBand.setText(QtGui.QApplication.translate("MultiQmlForm", "Load colormap from band", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnSelectAllLayers.setText(QtGui.QApplication.translate("MultiQmlForm", "Select all layers", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnClose.setText(QtGui.QApplication.translate("MultiQmlForm", "Close", None, QtGui.QApplication.UnicodeUTF8))

