from PyQt4.QtCore import QTranslator, QSettings, QFileInfo, QVariant, QLocale
from PyQt4.QtGui import QApplication
from qgis.core import QgsApplication

# For i18n support
userPluginPath = QFileInfo( QgsApplication.qgisUserDbFilePath() ).path() + "/python/plugins/multiqml"
systemPluginPath = QgsApplication.prefixPath() + "/python/plugins/multiqml"

overrideLocale = QSettings().value( "locale/overrideFlag", QVariant( False ) ).toBool()
if not overrideLocale:
  localeFullName = QLocale.system().name()
else:
  localeFullName = QSettings().value( "locale/userLocale", QVariant( "" ) ).toString()

if QFileInfo( userPluginPath ).exists():
  translationPath = userPluginPath + "/i18n/multiqml_" + localeFullName + ".qm"
else:
  translationPath = systemPluginPath + "/i18n/multiqml_" + localeFullName + ".qm"

localePath = translationPath
if QFileInfo( localePath ).exists():
  translator = QTranslator()
  translator.load( localePath )
  QApplication.installTranslator( translator )

mVersion = "0.3.22"
def name():
  return unicode(QApplication.translate("__init__", "MultiQml"))
def description():
  return unicode(QApplication.translate("__init__", "Apply single qml style to multiple raster or vector layers"))
def category():
  return unicode(QApplication.translate("__init__", "Plugins"))
def qgisMinimumVersion():
  return "1.0"
def version():
  return "0.3.22"
def authorName():
  return "NextGIS"
def homepage():
  return QApplication.translate("__init__", "http://gis-lab.info/qa/qgis-multiqml-eng.html")
def icon():
  return "icon.png"
def classFactory( iface ):
  from plugin import MultiQmlPlugin
  return MultiQmlPlugin( iface )

