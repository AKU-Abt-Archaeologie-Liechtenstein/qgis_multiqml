def name():
	return "MultiQml"
def description(  ):
	return ""
def qgisMinimumVersion(): 
	return "1.0" 
def version(  ):
	return "Version 0.1.3"
def classFactory( iface ):
	from plugin import MultiQmlPlugin
	return MultiQmlPlugin( iface )

