import os
import sys
import tempfile

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from ui_multiqml import Ui_MultiQmlForm

# create the dialog for mapserver export
class MultiQmlDlg(QDialog, Ui_MultiQmlForm): 
	def __init__(self, parent): 
		QDialog.__init__(self, parent) 
		self.setupUi(self) 

		self.tmpQmlSrcList = []
		self.mapLayers = QgsMapLayerRegistry.instance().mapLayers().values()
		self.fileNameStyle = QString()

		QObject.connect( self.lvMapLayers, SIGNAL( "clicked( const QModelIndex & )" ), self.doApplyStyleButtonEnabled )
		QObject.connect( self.rbnRasterLayers, SIGNAL( "toggled( bool )" ), self.doApplyStyleButtonEnabled )
		QObject.connect( self.rbnVectorLayers, SIGNAL( "toggled( bool )" ), self.doApplyStyleButtonEnabled )

		self.loadMapLayers()
		self.readSettings()

	@pyqtSignature( "" )
	def on_pbnApplyStyle_clicked(self):
		def isRasterQml():
			qmlFile = open( self.fileNameStyle, "rb" )
			line = qmlFile.readline()
			result = False
			while line != "":
				if line.find( "<rasterproperties>" ) != -1:
					result = True
					break
				line = qmlFile.readline()
			qmlFile.close()
			return result

		myLastUsedDir = self.settings.value( "multiqmlplugin/lastStyleDir" ).toString()
		self.fileNameStyle = QFileDialog.getOpenFileName(self, self.tr("Open style"), myLastUsedDir, self.tr("QGIS Apply Style File (*.qml)"))

		if not self.fileNameStyle.isEmpty():
			selected = self.lvMapLayers.selectedIndexes()
			print "There are slected layers:", selected
			for i in selected:
				layer = self.mapLayers[i.row()]
				
				if ( layer.type() == QgsMapLayer.VectorLayer ) and isRasterQml():
					self.myPluginMessage( "Unable to apply raster qml \"%s\" to vector layer \"%s\"." % ( self.fileNameStyle,  layer.name()), "critical" )
					continue
				elif ( layer.type() == QgsMapLayer.RasterLayer ) and not isRasterQml():
					self.myPluginMessage( "Unable to apply vector qml \"%s\" to raster layer \"%s\"." % ( self.fileNameStyle,  layer.name()), "critical" )
					continue

				myMessage, isLoaded = layer.loadNamedStyle(self.fileNameStyle)
				if not isLoaded: self.myPluginMessage( "Unable to apply qml style: %s to raster: %s\n%s." % ( self.fileNameStyle, layer.name(), myMessage ), "critical" )

				layer.triggerRepaint()
			self.settings.setValue( "multiqmlplugin/lastStyleDir", QVariant( os.path.dirname( unicode( self.fileNameStyle ) ) ) )
		else:
			self.myPluginMessage( "A style was not applied.", "information" )

	@pyqtSignature( "" )
	def on_pbnRestoreDefaultStyle_clicked(self):
		selected = self.lvMapLayers.selectedIndexes()
		for i in selected:
			layer = self.mapLayers[i.row()]
			myMessage, isLoaded = layer.loadNamedStyle(self.tmpQmlSrcList[i.row()])
			if not isLoaded: self.myPluginMessage( "Unable to restory the initial style for layer \"%s\"\n\"%s\"." % ( layer.name(), myMessage ), "critical" )
			layer.triggerRepaint()
	
	@pyqtSignature( "" )
	def on_pbnSelectAllLayers_clicked(self):
		self.lvMapLayers.selectAll()

	def loadMapLayers( self ):
		layersNameList = QStringList()
		for i in range( len( self.mapLayers ) ):
			layersNameList.append( self.mapLayers[i].name() )
			self.tmpQmlSrcList.append( tempfile.mktemp( '.qml' ) )
			myMessage, isSaved = self.mapLayers[i].saveNamedStyle(self.tmpQmlSrcList[i])
			if not isSaved: self.myPluginMessage( "Unable to save the temp file of qml style \"%s\"\nThe function to\
				\"Restore initial style\" will be unabled for layer \"%s\"\n\"%s\"." % ( self.tmpQmlSrcList[i], layersNameList[i], myMessage ), "critical" )
		print "There are temp qml files:", self.tmpQmlSrcList

		self.lvMapLayers.setModel( QStringListModel( layersNameList, self ) )
		self.lvMapLayers.setSelectionMode(QAbstractItemView.MultiSelection)
		self.lvMapLayers.setEditTriggers( QAbstractItemView.NoEditTriggers )
#		self.lvMapLayers.setCurrentIndex( self.lvMapLayers.model().index( 0 ) )
		
	@pyqtSignature( "" )
	def on_pbnClose_clicked(self):
		self.writeSettings()
		self.close()

	def closeEvent( self, event ):
		for i in range( len( self.mapLayers ) ):
			os.remove( self.tmpQmlSrcList[i] )
			print "The temp qml file:", self.tmpQmlSrcList[i], "removed"
		event.accept()

#	@pyqtSignature( "const QModelIndex&" )
#	def on_lvMapLayers_clicked( self, index ):
	def doApplyStyleButtonEnabled( self ):
		if len( self.lvMapLayers.selectedIndexes() ) == 0:
			self.pbnApplyStyle.setEnabled( False )
		else:
			self.pbnApplyStyle.setEnabled( True )
#			self.lvMapLayers.setCurrentIndex( self.lvMapLayers.model().index( 0 ) )

	def on_rbnRasterLayers_toggled( self, checked ):
		for i in range( len( self.mapLayers ) ):
			if checked and ( self.mapLayers[i].type() != QgsMapLayer.VectorLayer ):
				self.lvMapLayers.setRowHidden( i, False )
			elif not checked and ( self.mapLayers[i].type() == QgsMapLayer.RasterLayer ):
				self.lvMapLayers.setRowHidden( i, True )
			else:
				self.lvMapLayers.setRowHidden( i, True )

	def on_rbnVectorLayers_toggled( self, checked ):
		for i in range( len( self.mapLayers ) ):
			if checked and ( self.mapLayers[i].type() != QgsMapLayer.RasterLayer ):
				self.lvMapLayers.setRowHidden( i, False )
			elif not checked and ( self.mapLayers[i].type() == QgsMapLayer.VectorLayer ):
				self.lvMapLayers.setRowHidden( i, True )
			else:
				self.lvMapLayers.setRowHidden( i, True )

	def readSettings(self):
		self.settings = QSettings( "Gis-Lab", "MultiQml" )
		self.resize( self.settings.value( "multiqmlplugin/size", QVariant( QSize( 330, 230 ) ) ).toSize() )
		self.move( self.settings.value( "multiqmlplugin/pos", QVariant( QPoint( 0, 0 ) ) ).toPoint() )
		self.rbnRasterLayers.setChecked( self.settings.value( "multiqmlplugin/isRasterChecked", QVariant( True ) ).toBool() )
		self.rbnVectorLayers.setChecked( self.settings.value( "multiqmlplugin/isVectorChecked", QVariant( False ) ).toBool() )

	def writeSettings(self):
		self.settings = QSettings( "Gis-Lab", "MultiQml" )
		self.settings.setValue( "multiqmlplugin/size", QVariant( self.size() ) )
		self.settings.setValue( "multiqmlplugin/pos", QVariant( self.pos() ) )
		self.settings.setValue( "multiqmlplugin/isRasterChecked", QVariant( self.rbnRasterLayers.isChecked() ) )
		self.settings.setValue( "multiqmlplugin/isVectorChecked", QVariant( self.rbnVectorLayers.isChecked() ) )

	def myPluginMessage( self, msg, type ):
		if type == "information":
			QMessageBox.information(self, self.tr("Information"), self.tr( msg ))
		elif type == "critical":
			QMessageBox.critical(self, self.tr("Error"), self.tr( msg ))
