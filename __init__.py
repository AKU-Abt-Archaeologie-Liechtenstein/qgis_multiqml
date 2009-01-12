def name():
	return "MultiQml"
def description():
	return "Apply single qml to multiple raster and vector layers"
def qgisMinimumVersion(): 
	return "1.0" 
def version():
	return "Version 0.1.8"
def classFactory( iface ):
	from plugin import MultiQmlPlugin
	return MultiQmlPlugin( iface )

