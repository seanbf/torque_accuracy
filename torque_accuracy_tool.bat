@ECHO off
cls
:start
SET ThisScriptsDirectory=%~dp0
py -3.7 -m streamlit run %ThisScriptsDirectory%\program\torque_accuracy_tool.py