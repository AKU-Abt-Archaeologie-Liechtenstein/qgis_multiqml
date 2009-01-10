#! /usr/bin/python

import sys
#import pdb
from PyQt4.QtCore import QObject, SIGNAL
from PyQt4.QtGui import QMainWindow, QApplication, QAction
from multiqml import MultiQmlDlg

class MultiQmlPlugin():
	def __init__( self, iface ):
		self.iface = iface

	def initGui( self ):
		print "Init Gui"
		self.action = QAction( "MultiQml", self.iface.mainWindow(  ) )
		self.action.setWhatsThis("Apply single qml to multiple layers.")
		QObject.connect( self.action, SIGNAL( "activated(  )" ), self.run )
		self.iface.addPluginToMenu( "&MultiQml", self.action )
		self.iface.addToolBarIcon(self.action)

	def unload( self ):
		self.iface.removePluginMenu( "&MultiQml", self.action )
		self.iface.removeToolBarIcon(self.action)

	def run( self ):
		MultiQmldlg = MultiQmlDlg( self.iface.mainWindow(  ) )
#		MultiQmldlg = MultiQmlDlg( None )
		MultiQmldlg.show()


if __name__ == "__main__":
	app = QApplication( sys.argv )
	pluginWidget = MultiQmlPlugin( None )
	pluginWidget.run(  )
	sys.exit( app.exec_(  ) )
