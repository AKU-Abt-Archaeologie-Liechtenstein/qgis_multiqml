import sys
import os
import pdb

from osgeo import gdal

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

		self.lvMapLayers.setSelectionMode(QAbstractItemView.MultiSelection)
		self.fileNameStyle = QString()

		self.pbnLoadColormapFromBand.setVisible( False )

#		pdb.set_trace(  )
#		layout = QHBoxLayout( self.canvasFrame )
#		self.mCanvas = QgsMapCanvas( self.canvasFrame, "MultiQml Canvas" )
#		palette = QPalette(  )
#		palette.setColor( QPalette.Inactive, self.mCanvas.backgroundRole(  ), Qt.white )
#		self.mCanvas.setPalette( palette )
#		self.mCanvas.setCanvasColor( Qt.white )
#		layout.addWidget( self.mCanvas )
#		print self.mCanvas.backgroundRole(  )

		self.loadMapLayers()

	@pyqtSignature( "" )
	def on_pbnLoadStyle_clicked(self):
#		pdb.set_trace(  )
		self.fileNameStyle = QFileDialog.getOpenFileName(self, self.tr("Open style"), QDir.currentPath(), self.tr("QGIS Layer Style File (*.qml)"))
		if not self.fileNameStyle.isEmpty():
			selected = self.lvMapLayers.selectedIndexes()
			print selected
			for i in selected:
#				layer = self.mCanvas.layer(i.row())
				layer = self.mapLayers[i.row()]
				myMessage = layer.loadNamedStyle(self.fileNameStyle)
				print myMessage
				layer.triggerRepaint()
		else:
			QMessageBox.critical(self, self.tr("Error"), self.tr("Style not loaded")); 

	@pyqtSignature( "" )
	def on_pbnRestoreDefaultStyle_clicked(self):
#		pdb.set_trace(  )
		selected = self.lvMapLayers.selectedIndexes()
		for i in selected:
			layer = self.mapLayers[i.row()]
			myMessage = layer.loadDefaultStyle()
			print myMessage
			layer.triggerRepaint()
	
	@pyqtSignature( "" )
	def on_pbnLoadColormapFromBand_clicked(self):
		QMessageBox.information(self, self.tr("TRLegend Plugin"), self.tr("Function not implement, yet."))
#		myColorRampList = []
#		selected = self.lvMapLayers.selectedIndexes()
#		for i in selected:
#			layer = QgsRasterLayer()
#			layer = self.iface.mapCanvas().layer(i.row())
#			myMessage = layer.readColorTable(1, myColorRampList)

	@pyqtSignature( "" )
	def on_pbnSelectAllLayers_clicked(self):
#		if state == Qt.Checked:
#			self.chbxViewLayers.setChecked( False )
		self.lvMapLayers.selectAll()
#		else:
#			self.lvMapLayers.clearSelection()

#	@pyqtSignature( "int" )
#	def on_chbxViewLayers_stateChanged(self, state):
#		if state == Qt.Checked:
#			self.lvMapLayers.setSelectionMode(QAbstractItemView.SingleSelection)
#			self.lvMapLayers.setCurrentIndex( self.lvMapLayers.model().index( 0 ) )
#			self.lvMapLayers.emit( SIGNAL( "clicked(QModelIndex)" ), self.lvMapLayers.model().index( 0 ) )
#	#		self.lvMapLayers.emit( SIGNAL( "activated(QModelIndex)" ), self.lvMapLayers.model().index( 0 ) )
#		else:
#			self.lvMapLayers.setSelectionMode(QAbstractItemView.MultiSelection)
##			self.lvMapLayers.selectAll()

	def loadMapLayers( self ):
#		pdb.set_trace(  )
		layersNameList = QStringList()
		self.mapLayers = QgsMapLayerRegistry.instance().mapLayers().values()
#		self.countRasterPixelsList = []
#		layers = []
		for i in range( len( self.mapLayers ) ):
			layersNameList.append( self.mapLayers[i].name() )
			myMessage = self.mapLayers[i].saveDefaultStyle()
##			layers.append( QgsMapCanvasLayer( self.mapLayers[k] ) )
			print myMessage

#			ds = gdal.Open( str( self.mapLayers[k].source() ) )
#			colorTable = ds.GetRasterBand( 1 ).GetRasterColorTable()
#			if colorTable:
#				self.countRasterPixelsList.append( colorTable.GetCount() )
#			else:
#				self.countRasterPixelsList.append( 0 )

		self.lvMapLayers.setModel( QStringListModel( layersNameList, self ) )
		self.lvMapLayers.setSelectionMode(QAbstractItemView.MultiSelection)
		self.lvMapLayers.setEditTriggers( QAbstractItemView.NoEditTriggers )
		self.lvMapLayers.selectAll()

#		if self.layers != []: self.mCanvas.setLayerSet( self.layers )
#		self.mCanvas.freeze( False )
#		self.mCanvas.refresh(  )
		
	@pyqtSignature( "" )
	def on_pbnClose_clicked(self):
		self.close()

	def closeEvent( self, event ):
		for i in range( len( self.mapLayers ) ):
			src = str( self.mapLayers[i].source() )
			layerQmlSrc = os.path.splitext( src )[0] + '.qml'
			if os.path.exists( layerQmlSrc ):
				os.remove(layerQmlSrc)
		event.accept()

#	@pyqtSignature( "QModelIndex" )
#	def on_lvMapLayers_clicked( self, index ):
#	def on_lvMapLayers_activated( self, index ):
#		if self.chbxViewLayers.checkState() == Qt.Checked:
#			layer = self.mCanvas.layer( index.row() )
#			print layer
#			if layer:
#				print self.countRasterPixelsList
#				rasterPixelsList = QStringList()
#				if self.countRasterPixelsList == []:
#					self.lvTransparentClasses.model().removeRows( 0, self.lvTransparentClasses.model().rowCount() )
#				else:
#					for i in range( self.countRasterPixelsList[index.row()] ):
#						rasterPixelsList.append( str( i ) )
#					self.lvTransparentClasses.setModel( QStringListModel( rasterPixelsList, self ) )
#					self.lvTransparentClasses.setEditTriggers( QAbstractItemView.NoEditTriggers )

#				self.mCanvas.clear()
#				self.mCanvas.setCurrentLayer( layer )
#				self.mCanvas.setExtent( layer.extent() )
##				self.mCanvas.refresh()
#				layer.triggerRepaint()

#	@pyqtSignature( "QModelIndex" )
#	def on_lvTransparentClasses_clicked( self, index ):
##	def on_lvTransparentClasses_activated( self, index ):
#		if self.chbxViewLayers.checkState() == Qt.Checked:
#			currentLayer = self.mCanvas.currentLayer()
#			if currentLayer:
#				myTransparentSingleValuePixelList = currentLayer.rasterTransparency().transparentSingleValuePixelList()
#				for transparentPixel in myTransparentSingleValuePixelList:
#					if transparentPixel.pixelValue == index.row():
#						myTransparentSingleValuePixelList[myTransparentSingleValuePixelList.index( transparentPixel )].percentTransparent = \
#							( self.vslValueTransparency.value() / 255 ) * 100
#				else:
#					myTransparentPixel = QgsRasterTransparency.TransparentSingleValuePixel()
#					myTransparentPixel.pixelValue = index.row()
#					myTransparentPixel.percentTransparent = ( self.vslValueTransparency.value() / 255 ) * 100
#					myTransparentSingleValuePixelList.append( myTransparentPixel )
#
#				currentLayer.rasterTransparency().setTransparentSingleValuePixelList( myTransparentSingleValuePixelList )
#				self.mCanvas.refresh()
#				currentLayer.triggerRepaint()

#	def on_vslValueTransparency_valueChanged( self, val ):
#		self.lbTransparencyValuePercant.setText( self.tr( "%1%" ).arg( int( ( val / 255.0 ) * 100 ) ) )
#		if self.chbxTransparentLayer.checkState() == Qt.Checked:
#			self.mCanvas.currentLayer().setTransparency( 255 - val )
#			self.mCanvas.currentLayer().triggerRepaint()

#	def on_chbxTransparentLayer_stateChanged( self, state ):
#		if state == Qt.Checked:
#			self.vslValueTransparency.emit( SIGNAL( "valueChanged( int )" ), self.vslValueTransparency.value() )
