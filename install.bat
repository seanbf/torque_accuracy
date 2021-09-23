@ECHO off
cls
:start
SET ThisScriptsDirectory=%~dp0
SET PowerShellScriptPath=%ThisScriptsDirectory%ps_script.ps1
ECHO.
ECHO ################################
ECHO [ Torque Accuracy Tool Install ]
ECHO ################################
ECHO. 
ECHO    [1] Install Python 3.9.5, Paths, Dependancies and Launch torque_accuracy_tool [Powershell]
ECHO. 
ECHO    [2] Install Dependancies and Launch torque_accuracy_tool
ECHO. 

set choice=
set /p choice=Type the [number] of the option you want to use.

if not '%choice%'=='' set choice=%choice:~0,1%
if '%choice%'=='1' goto install_full
if '%choice%'=='2' goto install_dep

ECHO "%choice%" is not valid, try again
ECHO.
goto start

:install_full
ECHO Installing Python 3.9.5, Paths, Dependancies and Launching torque_accuracy_tool
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File ""%PowerShellScriptPath%""' -Verb RunAs}"
goto end

:install_dep
ECHO Installing Dependancies and Launching torque_accuracy_tool
python -m pip install -r requirements.txt
python -m streamlit run torque_accuracy_tool.py
goto end

:end
pause