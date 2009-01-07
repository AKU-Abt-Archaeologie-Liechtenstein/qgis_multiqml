import sys
import os
import pdb
#import copy

from PyQt4.QtCore import Qt, QObject, SIGNAL, QString, QStringList, QDir, \
pyqtSignature
from PyQt4.QtGui import QDialog, QAbstractItemView, QHBoxLayout, QPalette, \
QStringListModel, QFileDialog, QMessageBox
from qgis.core import *
from qgis.gui import *
from ui_multiqml import Ui_MultiQmlForm

# create the dialog for mapserver export
class MultiQmlDlg(QDialog, Ui_MultiQmlForm): 
	def __init__(self, parent): 
		QDialog.__init__(self, parent) 
		self.setupUi(self) 

		self.lvRasterLayers.setSelectionMode(QAbstractItemView.MultiSelection)
		self.fileNameStyle = QString()

#		pdb.set_trace(  )
		layout = QHBoxLayout( self.canvasFrame )
		self.mCanvas = QgsMapCanvas( self.canvasFrame, "MultiQml Canvas" )
		palette = QPalette(  )
		palette.setColor( QPalette.Inactive, self.mCanvas.backgroundRole(  ), Qt.white )
		self.mCanvas.setPalette( palette )
		self.mCanvas.setCanvasColor( Qt.white )
		layout.addWidget( self.mCanvas )
		print self.mCanvas.backgroundRole(  )

		self.loadRasterLayers()

	@pyqtSignature( "" )
	def on_pbnLoadStyle_clicked(self):
#		pdb.set_trace(  )
		self.fileNameStyle = QFileDialog.getOpenFileName(self, self.tr("Open style"), QDir.currentPath(), self.tr("QGIS Layer Style File (*.qml)"))
		if not self.fileNameStyle.isEmpty():
			selected = self.lvRasterLayers.selectedIndexes()
			for i in selected:
				layer = self.mCanvas.layer(i.row())
				myMessage = layer.loadNamedStyle(self.fileNameStyle)
				layer.triggerRepaint()
		else:
			QMessageBox.critical(self, self.tr("Error!"), self.tr("Style not loaded")); 

	@pyqtSignature( "" )
	def on_pbnDefaultStyle_clicked(self):
#		pdb.set_trace(  )
		selected = self.lvRasterLayers.selectedIndexes()
		for i in selected:
			layer = self.mCanvas.layer(i.row())
			myMessage = layer.loadDefaultStyle()
			layer.triggerRepaint()
	
	@pyqtSignature( "" )
	def on_pbnLoadColormapFromBand_clicked(self):
		QMessageBox.information(self, self.tr("TRLegend Plugin"), self.tr("Function not implement, yet."))
#		myColorRampList = []
#		selected = self.lvRasterLayers.selectedIndexes()
#		for i in selected:
#			layer = QgsRasterLayer()
#			layer = self.iface.mapCanvas().layer(i.row())
#			myMessage = layer.readColorTable(1, myColorRampList)

	@pyqtSignature( "int" )
	def on_chbxSelectAllLayers_stateChanged(self, state):
		if state == Qt.Checked:
			self.lvRasterLayers.selectAll()
			self.chbxViewLayers.setChecked( False )
		else:
			self.lvRasterLayers.clearSelection()

	@pyqtSignature( "int" )
	def on_chbxViewLayers_stateChanged(self, state):
		if state == Qt.Checked:
			self.chbxSelectAllLayers.setChecked( False )
			self.lvRasterLayers.setSelectionMode(QAbstractItemView.SingleSelection)
			self.lvRasterLayers.setCurrentIndex( self.lvRasterLayers.model().index( 0 ) )
			self.lvRasterLayers.emit( SIGNAL( "clicked(QModelIndex)" ), self.lvRasterLayers.model().index( 0 ) )
	#		self.lvRasterLayers.emit( SIGNAL( "activated(QModelIndex)" ), self.lvRasterLayers.model().index( 0 ) )
		else:
			self.lvRasterLayers.setSelectionMode(QAbstractItemView.MultiSelection)

#	@pyqtSignature( "" )
#	def on_pbnReloadLayers_clicked(self):
#		pdb.set_trace(  )
#		self.modelListView.removeRows(0, self.modelListView.rowCount()) 
#		self.mCanvas.clear(  )
#		self.loadRasterLayers(  )
#		for i in range(self.iface.mapCanvas().layerCount()):
#			layersIds.append(self.iface.mapCanvas().layer(i).name())
#			layer = self.iface.mapCanvas().layer(i)
#			myMessage = layer.saveDefaultStyle()
#		model.setStringList(layersIds)
#		self.lvRasterLayers.setModel(self.modelListView)
#		self.lvRasterLayers.reset()
#		self.lvRasterLayers.setSelectionMode(QAbstractItemView.MultiSelection)

	def loadRasterLayers( self ):
#		pdb.set_trace(  )
		layersIds = QStringList()
		self.mapLayers = dict( QgsMapLayerRegistry.instance(  ).mapLayers(  ) )
		layers = []
		for k in self.mapLayers.keys(  ):
			layersIds.append( self.mapLayers[k].name(  ) )
			myMessage = self.mapLayers[k].saveDefaultStyle()
			layers.append( QgsMapCanvasLayer( self.mapLayers[k] ) )

		self.lvRasterLayers.setModel( QStringListModel( layersIds, self ) )
		self.lvRasterLayers.setSelectionMode(QAbstractItemView.MultiSelection)
		self.lvRasterLayers.setEditTriggers( QAbstractItemView.NoEditTriggers )
		self.lvRasterLayers.selectAll()

		if layers != []: self.mCanvas.setLayerSet( layers )
		self.mCanvas.freeze( False )
		self.mCanvas.refresh(  )
		
	@pyqtSignature( "" )
	def on_pbnClose_clicked(self):
		self.close()

	def closeEvent( self, event ):
		for k in self.mapLayers.keys(  ):
			src = str( self.mapLayers[k].source() )
			layerQmlSrc = os.path.splitext( src )[0] + '.qml'
			if os.path.exists( layerQmlSrc ):
				os.remove(layerQmlSrc)
		event.accept()

	@pyqtSignature( "QModelIndex" )
	def on_lvRasterLayers_clicked( self, index ):
#	def on_lvRasterLayers_activated( self, index ):
		if self.chbxViewLayers.checkState() == Qt.Checked:
			layer = self.mCanvas.layer( index.row() )
			if layer:
				indexTransp = QStringList()
				for i in range( 16 ):
					indexTransp.append( str( i ) )
				self.lvTransparency.setModel( QStringListModel( indexTransp, self ) )
				self.lvTransparency.setEditTriggers( QAbstractItemView.NoEditTriggers )

				self.mCanvas.clear()
				self.mCanvas.setCurrentLayer( layer )
				self.mCanvas.refresh()
				self.mCanvas.setExtent( layer.extent() )
				layer.triggerRepaint()

	@pyqtSignature( "QModelIndex" )
	def on_lvTransparency_clicked( self, index ):
#	def on_lvTransparency_activated( self, index ):
		if self.chbxViewLayers.checkState() == Qt.Checked:
			currentLayer = self.mCanvas.currentLayer()
			if currentLayer:
				myTransparentSingleValuePixelList = currentLayer.rasterTransparency().transparentSingleValuePixelList()
				for transparentPixel in myTransparentSingleValuePixelList:
					if transparentPixel.pixelValue == index.row():	
						myTransparentSingleValuePixelList[myTransparentSingleValuePixelList.index( transparentPixel )].percentTransparent = \
							( self.vslValueTransparency.value() / 255 ) * 100
				else:
					myTransparentPixel = QgsRasterTransparency.TransparentSingleValuePixel()
					myTransparentPixel.pixelValue = index.row()
					myTransparentPixel.percentTransparent = ( self.vslValueTransparency.value() / 255 ) * 100
					myTransparentSingleValuePixelList.append( myTransparentPixel )
				currentLayer.rasterTransparency().setTransparentSingleValuePixelList( myTransparentSingleValuePixelList )
				self.mCanvas.refresh()
				currentLayer.triggerRepaint()

	def on_vslValueTransparency_valueChanged( self, val ):
		self.lbTransparencyValuePercant.setText( self.tr( "%1%" ).arg( int( ( val / 255.0 ) * 100 ) ) )
		if self.chbxTransparentLayer.checkState() == Qt.Checked:
			self.mCanvas.currentLayer().setTransparency( val )
			self.mCanvas.currentLayer().triggerRepaint()

	def on_chbxTransparentLayer_stateChanged( self, state ):
		if state == Qt.Checked:
			self.vslValueTransparency.emit( SIGNAL( "valueChanged( int )" ), self.vslValueTransparency.value() )
