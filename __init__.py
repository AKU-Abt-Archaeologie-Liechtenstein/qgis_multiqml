def name():
	return "MultiQml"
def description():
	return "Apply single qml to multiple layers"
def qgisMinimumVersion(): 
	return "1.0" 
def version():
	return "Version 0.1.6"
def classFactory( iface ):
	from plugin import MultiQmlPlugin
	return MultiQmlPlugin( iface )

