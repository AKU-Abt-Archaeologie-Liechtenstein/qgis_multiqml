mkdir multiqml
mkdir multiqml\i18n
xcopy *.py multiqml
xcopy *.png multiqml
xcopy README.md multiqml
xcopy LICENSE multiqml
xcopy metadata.txt multiqml
xcopy /F i18n\*.qm multiqml\i18n
zip -r multiqml.zip multiqml
del /Q multiqml
rd multiqml