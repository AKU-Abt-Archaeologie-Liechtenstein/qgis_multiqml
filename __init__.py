from PyQt4.QtCore import QTranslator, QLocale
from PyQt4.QtGui import QApplication

import resources

if QLocale.system().name() == "ru_RU":
#	i18n Russian
	translatorDlg = QTranslator()
	translatorDlg.load(":/plugins/multiqml/translations/multiqml_ru")
	QApplication.installTranslator(translatorDlg)
	
mVersion = "0.2.9"
def name():
	return unicode(QApplication.translate("__init__", "MultiQml"))
def description():
	return unicode(QApplication.translate("__init__", "Apply single qml style to multiple raster or vector layers"))
def qgisMinimumVersion():
	return "1.0"
def version():
	return mVersion
def authorName():
	return "Gis-Lab"
def homepage():
	return QApplication.translate("__init__", "http://gis-lab.info/qa/qgis-multiqml-eng.html")
def classFactory( iface ):
	from plugin import MultiQmlPlugin
	return MultiQmlPlugin( iface )

