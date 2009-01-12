import sys
#import pdb
from PyQt4.QtCore import QObject, SIGNAL
from PyQt4.QtGui import QMainWindow, QApplication, QAction, QIcon, \
	QDialog, QLabel, QWidget, QVBoxLayout

from multiqml import MultiQmlDlg

import resources

class MultiQmlPlugin(QObject):
	def __init__( self, iface ):
		self.iface = iface

	def initGui( self ):
		myTr = QWidget()
		self.actionRun = QAction( QIcon( ":/plugins/multiqml/icon.png" ),\
			myTr.tr( "MultiQml" ), self.iface.mainWindow() )
		self.actionRun.setWhatsThis( myTr.tr( "Apply single qml to multiple raster and vector layers.") )
		self.actionAbout = QAction( myTr.tr( "About" ), self.iface.mainWindow() )

		QObject.connect( self.actionRun, SIGNAL( "activated()" ), self.run )
		QObject.connect( self.actionAbout, SIGNAL( "activated()" ), self.about )

		self.iface.addToolBarIcon(self.actionRun)
		self.iface.addPluginToMenu( myTr.tr( "&MultiQml" ), self.actionRun )
		self.iface.addPluginToMenu( myTr.tr( "&MultiQml" ), self.actionAbout )

	def unload( self ):
		myTr = QWidget()
		self.iface.removePluginMenu( myTr.tr( "&MultiQml" ), self.actionRun )
		self.iface.removePluginMenu( myTr.tr( "&MultiQml" ), self.actionAbout )
		self.iface.removeToolBarIcon(self.actionRun)

	def run( self ):
		dlgMain = MultiQmlDlg( self.iface.mainWindow(  ) )
#		MultiQmldlg = MultiQmlDlg( None )
		dlgMain.show()

	def about( self ):
		myTr = QWidget()
		dlgAbout = QDialog( self.iface.mainWindow() )
		lines = QVBoxLayout( dlgAbout )
		lines.addWidget( QLabel( myTr.tr( "<p><b>MultiQml:</b></p>\
		<pre>  Apply single qml to multiple raster and vector layers.</pre>\
		<p><b>Developers:</b></p>\
		<pre>  Lynx (lynx21.12.12@gmail.com)</pre>\
		<pre>  Maxim Dubinin (sim@gis-lab.info)</pre>\
		<p><b>Link:</b></p>") ) )
		link = QLabel( "<pre>  <a href=\"http://gis-lab.info/qa/qgis-multiqml-eng.html\">http://gis-lab.info/qa/qgis-multiqml-eng.html</a></pre>" )
		link.setOpenExternalLinks( True )
		lines.addWidget( link )

		dlgAbout.exec_()

if __name__ == "__main__":
	app = QApplication( sys.argv )
	pluginWidget = MultiQmlPlugin( None )
	pluginWidget.run(  )
	sys.exit( app.exec_(  ) )
