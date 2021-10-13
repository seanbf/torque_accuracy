# Torque Accuracy Tool 🎯

<br>The Torque Accuracy Tool will plot test data, remove transients and provide analysis on the accuracy of **Torque Output** against **Torque Measured**, in each or all operating quadrants, voltages and speeds.
<br>The tool can also be used to achieve the same analysis with **Torque Estimated**
<br>As the tool uses averaging within the analysis, there is an option to remove transients from the data so only steady state data is analysed

## Installation

<br>`install.bat` is a batch file that allows the user to select from 2 installation choices.
- **Option [1]: Install Python 3.7.4, Paths, Dependancies and Launch torque_accuracy_tool**
<br>Using option [1] will launch a powershell script to install Python 3.7.4, all the dependencies required by torque_accuracy_tool and then launch the tool in a web browser
- **Option [2]: Install Dependancies and Launch torque_accuracy_tool**
<br>Using option [2] will bypass the python installation and just install all the dependencies (presuming it is installed and has the correct paths) required by torque_accuracy_tool and then launch the tool in a web browser.
<br>Once installtion is complete the tool will already be launched, and can be relaunched using `torque_accuracy_tool.bat`

## Running

<br>`torque_accuracy_tool.bat` will apply `py - 3.7 -m streamlit run torque_accuracy_tool.py` command to the cmd terminal which will launch a local server and open up the default web browser as the front-end.
