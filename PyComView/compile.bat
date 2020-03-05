@echo off

SET CurrentPath=%~dp0

@echo compilation du script avec : %~dp0setup.py

c:\python27\python.exe %~dp0setup.py %py2exe

@echo copying config.txt and iCom_iView.dll in dist folder
COPY /Y %~dp0config.txt %~dp0dist\config.txt
COPY /Y %~dp0iCom_iView\src\iCom_iView.dll %~dp0dist\iCom_iView.dll

@echo copying other dll in dist folder if present in current folder
COPY /Y %~dp0XISL.dll %~dp0dist\XISL.dll
COPY /Y %~dp0iCOMClient.dll %~dp0dist\iCOMClient.dll
COPY /Y %~dp0libgcc_s_dw2-1.dll %~dp0dist\libgcc_s_dw2-1.dll
COPY /Y %~dp0libstdc++-6.dll %~dp0dist\libstdc++-6.dll


