from PyQt4.QtCore import QTranslator, QLocale
from PyQt4.QtGui import QApplication

import resources

if QLocale.system().name() == "ru_RU":
#	i18n Russian
	translatorDlg = QTranslator()
	translatorDlg.load(":/translations/multiqml_ru")
	QApplication.installTranslator(translatorDlg)
	
def name():
	return unicode(QApplication.translate("__init__", "MultiQml"))
def description():
	return unicode(QApplication.translate("__init__", "Apply single qml style to multiple raster or vector layers."))
def qgisMinimumVersion():
	return "1.0"
def version():
	return unicode(QApplication.translate("__init__", "Version") + " 0.2.3")
def classFactory( iface ):
	from plugin import MultiQmlPlugin
	return MultiQmlPlugin( iface )

