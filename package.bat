mkdir multiqml
mkdir multiqml\i18n
xcopy *.py multiqml
xcopy *.png multiqml
xcopy about_dialog_base.ui multiqml
xcopy README.md multiqml
xcopy LICENSE multiqml
xcopy metadata.txt multiqml
xcopy /F i18n\*.ts multiqml\i18n
lrelease multiqml\i18n\multiqml_ru.ts
del multiqml\i18n\multiqml_ru.ts
zip -r multiqml.zip multiqml
del /Q multiqml
rmdir /Q /S multiqml