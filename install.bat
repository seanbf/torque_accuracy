@ECHO off
cls
:start
SET ThisScriptsDirectory=%~dp0
SET PowerShellScriptPath=%ThisScriptsDirectory%/program/install/ps_script.ps1
ECHO.
ECHO ###################################
ECHO [     Torque Accuracy Install     ]
ECHO ###################################
ECHO. 
ECHO    [1] Install Python 3.7.4, Paths, Dependancies and Launch Torque Accuracy Tool [Powershell]
ECHO. 
ECHO    [2] Install Dependancies and Launch Torque Accuracy Tool
ECHO. 

set choice=
set /p choice=Type the [number] of the option you want to use.
ECHO. 

if not '%choice%'=='' set choice=%choice:~0,1%
if '%choice%'=='1' goto install_full
if '%choice%'=='2' goto install_dep

ECHO "%choice%" is not valid, try again
ECHO.
goto start

:install_full
ECHO Installing Python 3.7.4, Paths, Dependancies and Launching Torque Accuracy Tool
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File ""%PowerShellScriptPath%""' -Verb RunAs}"

ECHO Generating Desktop Shortcut and Icon
set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\Torque Accuracy Tool.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath ="%comspec%" >> %SCRIPT%
echo oLink.Arguments = " /c ""%ThisScriptsDirectory%torque_accuracy_tool.bat""" >> %SCRIPT%
echo oLink.IconLocation = "%ThisScriptsDirectory%\icon\accuracy.ico" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
cscript /nologo %SCRIPT%
del %SCRIPT%

goto end

:install_dep
ECHO Installing Dependancies and Launching Torque Accuracy Tool

ECHO Generating Desktop Shortcut and Icon
set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\Torque Accuracy Tool.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath ="%comspec%" >> %SCRIPT%
echo oLink.Arguments = " /c ""%ThisScriptsDirectory%torque_accuracy_tool.bat""" >> %SCRIPT%
echo oLink.IconLocation = "%ThisScriptsDirectory%\icon\accuracy.ico" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
cscript /nologo %SCRIPT%
del %SCRIPT%

py -3.7 -m pip install -r %ThisScriptsDirectory%\program\install\requirements.txt
py -3.7 -m streamlit run %ThisScriptsDirectory%\program\torque_accuracy_tool.py
goto end

echo off

:end
pause