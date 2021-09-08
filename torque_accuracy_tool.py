import streamlit as st
import pandas as pd
from src.layout import test_details, limits, signals
from src.utils import load_dataframe, col_removal, determine_transients, sample_transients, transient_removal, round_speeds, torque_error_calc
from src.plotter import demanded_plot, transient_removal_plot

page_config = st.set_page_config(
                                page_title              ="Torque Accuracy Tool", 
                                page_icon               ="🎯", 
                                #layout                  ='wide', 
                                initial_sidebar_state   ='auto'
                                )


col_left, col_title, col_right = st.columns(3)
col_title.title("Torque Accuracy Tool 🎯")

st.write("The Torque Accuracy Tool will plot test data, remove transients and provide analysis on the accuracy of **Torque Output** against **Torque Measured**, in each or all operating quadrants, voltages and speeds.")
st.write("The tool can also be used to achieve the same analysis with **Estimated Torque**.")
st.write("As the tool uses averaging within the analysis, there is an option to remove transients from the data so only steady state data is analysed.")

#strings used for readability
t_demanded              = "Torque Demanded [Nm]"
t_estimated             = "Torque Estimated [Nm]"
t_measured              = "Torque Measured [Nm]"
speed                   = "Speed [rpm]"
speed_round             = "Speed [rpm] Rounded"
vdc                     = "DC Voltage"
idc                     = "DC Current"
t_demanded_error_nm     = "Torque Demanded Error [Nm]"
t_demanded_error_pc     = "Torque Demanded Error [%]"
t_estimated_error_nm    = "Torque Estimated Error [Nm]"
t_estimated_error_pc    = "Torque Estimated Error [%]"

st.markdown("---")
st.header("Upload file(s)")
#Ask for file upload and read.
st.checkbox("Show first 10 rows of Data", key = "Sample Data")

uploaded_file = st.file_uploader(   
                                        label="",
                                        accept_multiple_files=False,
                                        type=['csv', 'xlsx']
                                        )

if uploaded_file is None:
    st.info("Please upload file(s)")
    st.stop()

elif uploaded_file is not None:
    original_file_name  = uploaded_file.name

    dataframe, columns  = load_dataframe(uploaded_file=uploaded_file)
    if st.session_state["Sample Data"] == True:
        st.write(dataframe.head(10))
    columns             = list(columns)

    columns.insert(0, "Not Selected")




st.markdown("---")
st.header("Test Details - (*Optional*)")
test_dict = test_details()



st.markdown("---")
st.header("Configure Test Limits")
st.radio("Torque Analysis", ["Output & Estimated","Output"], key = "Analysis Mode")
limits(st.session_state["Analysis Mode"])




st.markdown("---")
st.header("Configure Signals")
st.write("All signals must be manually selected if auto-select cannot find them.")
signals(st.session_state["Analysis Mode"], columns,  t_demanded, t_estimated, t_measured, speed, vdc, idc)
if any(value == 'Not Selected' for value in st.session_state.values()) == True:
    st.stop()




selected_data = col_removal(dataframe, list(st.session_state.values()))

st.write(selected_data.head(10))

if st.session_state["Analysis Mode"] == "Output & Estimated":
    selected_data.rename(columns = {        
                                        st.session_state[speed]         :speed,
                                        st.session_state[t_measured]    :t_measured,
                                        st.session_state[t_demanded]    :t_demanded,
                                        st.session_state[t_estimated]   :t_estimated,
                                        st.session_state[vdc]           :vdc,
                                        st.session_state[idc]           :idc
                                    }, inplace = True)
else:
    selected_data.rename(columns = {        
                                        st.session_state[speed]         :speed,
                                        st.session_state[t_measured]    :t_measured,
                                        st.session_state[t_demanded]    :t_demanded,
                                        st.session_state[vdc]           :vdc,
                                        st.session_state[idc]           :idc
                                    }, inplace = True)

st.markdown("---")
st.header("Remove Transients - (*Optional*)")
with st.spinner("Generating transient removal tool"):

    st.write("Make sure the transient removal process is removing the required data; when there is a step change and time taken until steady state is reached.")
    st.markdown("If this is not achieved, adjust the variable `Dwell Period` using the slider below")
    st.markdown("Scan through torque steps using the `Sample` slider to determine if the `Dwell Period` is appropiate for the range of torque steps.")

    dwell_col, sample_col = st.columns(2)
    dwell_col.slider("Dwell Period", min_value=0, max_value=5000, step=1, value= 500, key = "Dwell Period")

    Step_index, Stop_index          = determine_transients(selected_data, t_demanded, st.session_state["Dwell Period"]) 
    sample_col.slider("Sample", min_value=1, max_value=abs(len(Stop_index)-1), step=1, value= round(abs(len(Stop_index)-1)/2), key = "Sample")

    transient_sample                = sample_transients(Step_index, Stop_index, selected_data, st.session_state)    
    transient_removal_sample_plot   = transient_removal_plot(transient_sample, Step_index, Stop_index, selected_data, st.session_state)

    selected_data = selected_data.drop(['Step_Change'], axis = 1)

    st.plotly_chart(transient_removal_sample_plot)

    rem_trans_col1, rem_trans_col2, rem_trans_col3 = st.columns(3)
    
    if rem_trans_col2.checkbox("Remove Transients", key = "Remove Transients") == True: 
        selected_data = transient_removal(selected_data, Step_index, Stop_index)
        st.success(str(len(Stop_index)-1) + " Transients Removed")









st.markdown("---")
st.header("Round Test Point Variables")  
st.subheader("Speed")
st.number_input("Base", min_value=1, max_value=5000, value=50, step=1, key = "Speed Base")
round_spd_col1, round_spd_col2, round_spd_col3 = st.columns(3)
if round_spd_col2   .checkbox("Round Speed", key = "Round Speed") == True:
    selected_data = round_speeds(selected_data, speed, t_demanded, st.session_state["Speed Base"])
    number_of_rounded_speeds = len((selected_data[speed_round]).unique())
    st.success(str(number_of_rounded_speeds) + " Unique Speed Points Found")
else:
    st.stop()







st.markdown("---")  
st.header("Torque Demanded against Speed - (*Optional*)")
if st.checkbox("Plot Test Data", key = "Plot Test Data") == True:
    st.write("Below is a plot of the data representing Torque Demanded and Speed")
    st.write("This is useful to determine if the data uploaded and rounded represent the correct test cases / behaviour")
    with st.spinner("Generating Demanded Test Point Plot"):
        st.plotly_chart(demanded_plot(selected_data,speed_round, t_demanded))

with st.spinner("Calculating errors..."):
    selected_data = torque_error_calc(selected_data, t_demanded, t_estimated, t_measured, t_demanded_error_nm, t_demanded_error_pc, t_estimated_error_nm, t_estimated_error_pc)


st.markdown("---")  
st.header("Torque Output Accuracy")
st.subheader("Newton Meters")
st.write("Limit: " + str(st.session_state["Output Limit [Nm]"]) + "Nm")

st.header("Torque Output Accuracy")
st.subheader("Percentage")
st.write("Limit: " + str(st.session_state["Output Limit [%]"]) + "%")

report_table = pd.DataFrame([test_dict])
report_table = report_table.astype(str)
report_table = report_table.T
