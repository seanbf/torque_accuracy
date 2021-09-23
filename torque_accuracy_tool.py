import streamlit as st
import pandas as pd

from src.layout import report_details, limits,  limit_format
from src.utils import load_dataframe, col_removal, determine_transients, sample_transients, transient_removal, round_speeds, torque_error_calc, error_nm_analysis, error_pc_analysis, z_col_or_grid
from src.plotter import demanded_plot, transient_removal_plot, plot_3D, plot_pie, plot_bowtie
from src.colors import sequential_color_dict, diverging_color_dict, plot_color_set
from src.symbols import symbol_auto_select, speed_rpm_symbols, t_demanded_symbols, t_measured_symbols, t_estimated_signals, vdc_symbols,idc_symbols
import plotly.graph_objects as go

page_config = st.set_page_config(
                                page_title              ="Torque Accuracy Tool", 
                                page_icon               ="🎯", 
                                #layout                  ='wide', 
                                initial_sidebar_state   ='auto'
                                )


col_left, col_title, col_right = st.columns(3)
col_title.title("Torque Accuracy Tool 🎯")

st.write("The Torque Accuracy Tool will plot test data, remove transients and provide analysis on the accuracy of **Torque Output** against **Torque Measured**, in each or all operating quadrants, voltages and speeds.")
st.write("The tool can also be used to achieve the same analysis with **Torque Estimated**.")
st.write("As the tool uses averaging within the analysis, there is an option to remove transients from the data so only steady state data is analysed.")

#strings used for readability
t_demanded              = "Torque Demanded [Nm]"
t_estimated             = "Torque Estimated [Nm]"
t_measured              = "Torque Measured [Nm]"
speed                   = "Speed [rpm]"
speed_round             = "Speed [rpm] Rounded"
vdc                     = "DC Voltage [V]"
idc                     = "DC Current [A]"
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
                                        accept_multiple_files=True,
                                        type=['csv', 'xlsx']
                                        )

if uploaded_file == []:
    st.info("Please upload file(s)")
    st.stop()

else:

    dataframe, columns  = load_dataframe(uploaded_files=uploaded_file)
    if st.session_state["Sample Data"] == True:
        st.write(dataframe.head(10))
    columns             = list(columns)

    columns.insert(0, "Not Selected")



st.markdown("---") 



st.header("Configure Test Limits")
st.radio("Torque Analysis", ["Output & Estimated","Output"], key = "Analysis Mode")
limits(st.session_state["Analysis Mode"])



st.markdown("---") 



st.header("Configure Signals")
st.write("All signals must be manually selected if auto-select cannot find them.")

st.selectbox(t_measured,list(columns),  key = t_measured, index = symbol_auto_select(columns, t_measured_symbols))

st.selectbox(t_demanded,list(columns), key = t_demanded, index = symbol_auto_select(columns, t_demanded_symbols))

if st.session_state["Analysis Mode"] == "Output & Estimated":
    st.selectbox(t_estimated,list(columns), key = t_estimated, index = symbol_auto_select(columns, t_estimated_signals))

st.selectbox(speed,list(columns), key = speed, index = symbol_auto_select(columns, speed_rpm_symbols))

st.selectbox(vdc,list(columns), key = vdc, index = symbol_auto_select(columns, vdc_symbols))

st.selectbox(idc,list(columns), key = idc, index = symbol_auto_select(columns, idc_symbols))

if any(value == 'Not Selected' for value in st.session_state.values()) == True:
    st.stop()

selected_data = col_removal(dataframe, list(st.session_state.values()))

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

    dwell_col, sample_col, t_d_filter_col = st.columns(3)
    dwell_col.slider("Dwell Period", min_value=0, max_value=2000, step=1, value= 500, key = "Dwell Period")
    t_d_filter_col.number_input("Torque Demanded Filter", min_value=0.0,max_value=300.0,step=0.1,value=1.0,help="If torque demand is not as consistent as expected i.e. during derate, apply a threshold to ignore changes smaller than the filter",key = "Torque Demanded Filter")

    Step_index, Stop_index          = determine_transients(selected_data,t_demanded,st.session_state["Torque Demanded Filter"], st.session_state["Dwell Period"]) 
    
    sample_col.slider("Sample", min_value=1, max_value=abs(len(Stop_index)-1), step=1, value= round(abs(len(Stop_index)-1)/2), key = "Sample")


    transient_sample                = sample_transients(Step_index, Stop_index, selected_data, st.session_state)    
    transient_removal_sample_plot   = transient_removal_plot(transient_sample, Step_index, Stop_index, selected_data, st.session_state,  t_demanded, t_estimated, t_measured)

    selected_data = selected_data.drop(['Step_Change'], axis = 1)

    st.plotly_chart(transient_removal_sample_plot)

rem_trans_col1, rem_trans_col2, rem_trans_col3 = st.columns(3)
    
if rem_trans_col2.checkbox("Remove Transients", key = "Remove Transients") == True: 
    with st.spinner("Removing Transients from data"):
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
st.subheader("Voltage")


st.markdown("---") 



st.header("Torque Demanded against Speed - (*Optional*)")
if st.checkbox("Plot Test Data", key = "Plot Test Data") == True:
    st.write("Below is a plot of the data representing Torque Demanded and Speed")
    st.write("This is useful to determine if the data uploaded and rounded represent the correct test cases / behaviour")
    with st.spinner("Generating Demanded Test Point Plot"):
        st.plotly_chart(demanded_plot(selected_data, t_demanded, speed_round))



st.markdown("---") 



st.header("Torque Output Accuracy")
st.write("Minimum, Mean and Maximum errors are absoluted.")
with st.spinner("Calculating errors..."):
    selected_data = torque_error_calc(selected_data, t_demanded, t_estimated, t_measured, t_demanded_error_nm, t_demanded_error_pc, t_estimated_error_nm, t_estimated_error_pc)

st.subheader("Newton Meter Error")
st.write("Limit: " + "`± "+str(st.session_state["Output Limit [Nm]"]) + " Nm`")
with st.spinner("Generating Torque Output [Nm] Accuracy Table"):
    t_demanded_error_table_nm, min_error_demanded_nm, average_error_demanded_nm, max_error_demanded_nm, t_d_nm_flag = error_nm_analysis(selected_data, st.session_state["Output Limit [Nm]"], st.session_state["Output Limit [%]"], t_demanded, t_demanded, t_estimated, t_measured, speed_round, vdc, idc, t_demanded_error_nm, t_demanded_error_pc)
    
    if t_d_nm_flag == True:
        st.write("✔️ No torque error (Nm) resulted in surpassing the limits")
        st.write("Upto five of the maximum torque errors shown below")
        t_d_nm_flag_html = '''<p><svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="green" class="bi bi-check-lg" viewBox="0 0 16 16">
        <path d="M13.485 1.431a1.473 1.473 0 0 1 2.104 2.062l-7.84 9.801a1.473 1.473 0 0 1-2.12.04L.431 8.138a1.473 1.473 0 0 1 2.084-2.083l4.111 4.112 6.82-8.69a.486.486 0 0 1 .04-.045z"/>
        </svg>No torque error (Nm) resulted in surpassing the limits </p>
        <p>Upto five of the maximum torque errors shown below</p>'''

    else:
        st.write("❌ The following Torque error(s) (Nm) resulted in surpassing the limits")
        t_d_nm_flag_html = '''<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="red" class="bi bi-x-lg" viewBox="0 0 16 16">
        <path d="M1.293 1.293a1 1 0 0 1 1.414 0L8 6.586l5.293-5.293a1 1 0 1 1 1.414 1.414L9.414 8l5.293 5.293a1 1 0 0 1-1.414 1.414L8 9.414l-5.293 5.293a1 1 0 0 1-1.414-1.414L6.586 8 1.293 2.707a1 1 0 0 1 0-1.414z"/>
        </svg>The following Torque error(s) (Nm) resulted in surpassing the limits'''

    t_dem_err_nm_col1, t_dem_err_nm_col2, t_dem_err_nm_col3 = st.columns(3)
    min_error_demanded_nm_display, average_error_demanded_nm_display, max_error_demanded_nm_display = limit_format(t_d_nm_flag, min_error_demanded_nm, average_error_demanded_nm, max_error_demanded_nm, "Output", "Nm")

    t_dem_err_nm_col1.subheader("Minimum Error")
    t_dem_err_nm_col1.markdown(min_error_demanded_nm_display, unsafe_allow_html=True)

    t_dem_err_nm_col2.subheader("Mean Error")
    t_dem_err_nm_col2.markdown(average_error_demanded_nm_display, unsafe_allow_html=True)

    t_dem_err_nm_col3.subheader("Maximum Error")
    t_dem_err_nm_col3.markdown(max_error_demanded_nm_display, unsafe_allow_html=True)

    st.write(t_demanded_error_table_nm)

    t_demanded_error_table_nm_html= t_demanded_error_table_nm.to_html()

st.subheader("Percentage Error")
with st.spinner("Generating Torque Output [%] Accuracy Table"):
    st.write("Limit: " + "`± "+str(st.session_state["Output Limit [%]"]) + " %`")
    t_demanded_error_table_pc, min_error_demanded_pc, average_error_demanded_pc, max_error_demanded_pc, t_d_pc_flag = error_pc_analysis(selected_data, st.session_state["Output Limit [Nm]"], st.session_state["Output Limit [%]"], t_demanded, t_demanded, t_estimated, t_measured, speed_round, vdc, idc, t_demanded_error_nm, t_demanded_error_pc)
    
    if t_d_pc_flag == True:
        st.write("✔️ No torque error (%) resulted in surpassing the limits")
        st.write("Upto five of the maximum torque errors shown below")
        t_d_pc_flag_html = '''<p><svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="green" class="bi bi-check-lg" viewBox="0 0 16 16">
        <path d="M13.485 1.431a1.473 1.473 0 0 1 2.104 2.062l-7.84 9.801a1.473 1.473 0 0 1-2.12.04L.431 8.138a1.473 1.473 0 0 1 2.084-2.083l4.111 4.112 6.82-8.69a.486.486 0 0 1 .04-.045z"/>
        </svg>No torque error (%) resulted in surpassing the limits </p>
        <p>Upto five of the maximum torque errors shown below</p>'''

    else:
        st.write("❌ The following Torque error(s) (%) resulted in surpassing the limits")
        t_d_pc_flag_html = '''<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="red" class="bi bi-x-lg" viewBox="0 0 16 16">
        <path d="M1.293 1.293a1 1 0 0 1 1.414 0L8 6.586l5.293-5.293a1 1 0 1 1 1.414 1.414L9.414 8l5.293 5.293a1 1 0 0 1-1.414 1.414L8 9.414l-5.293 5.293a1 1 0 0 1-1.414-1.414L6.586 8 1.293 2.707a1 1 0 0 1 0-1.414z"/>
        </svg>The following Torque error(s) (%) resulted in surpassing the limits'''

    t_dem_err_pc_col1, t_dem_err_pc_col2, t_dem_err_pc_col3 = st.columns(3)

    min_error_demanded_pc_display, average_error_demanded_pc_display, max_error_demanded_pc_display = limit_format(t_d_pc_flag, min_error_demanded_pc, average_error_demanded_pc, max_error_demanded_pc, "Output", "%")

    t_dem_err_pc_col1.subheader("Minimum Error")
    t_dem_err_pc_col1.markdown(min_error_demanded_pc_display, unsafe_allow_html=True)

    t_dem_err_pc_col2.subheader("Mean Error")
    t_dem_err_pc_col2.markdown(average_error_demanded_pc_display, unsafe_allow_html=True)

    t_dem_err_pc_col3.subheader("Maximum Error")
    t_dem_err_pc_col3.markdown(max_error_demanded_pc_display, unsafe_allow_html=True)

    st.write(t_demanded_error_table_pc)

dem_pie = plot_pie(selected_data, selected_data["Torque Demanded Error [Nm]"], selected_data["Torque Demanded Error [%]"], st.session_state["Output Limit [Nm]"],  st.session_state["Output Limit [%]"])
st.plotly_chart(dem_pie)



st.markdown("---") 



st.header("Torque Estimated Accuracy")
st.write("Minimum, Mean and Maximum errors are absoluted.")
st.subheader("Newton Meter Error")

with st.spinner("Generating Torque Estimated [Nm] Accuracy Table"):
    st.write("Limit: " + "`± "+str(st.session_state["Estimated Limit [Nm]"]) + " Nm`")

    t_estimated_error_table_nm, min_error_estimated_nm, average_error_estimated_nm, max_error_estimated_nm, t_e_nm_flag = error_nm_analysis(selected_data, st.session_state["Estimated Limit [Nm]"], st.session_state["Estimated Limit [%]"], t_estimated, t_demanded, t_estimated, t_measured, speed_round, vdc, idc, t_estimated_error_nm, t_estimated_error_pc)

    if t_e_nm_flag == True:
        st.write("✔️ No torque error (Nm) resulted in surpassing the limits")
        st.write("Upto five of the maximum torque errors shown below")
        t_e_nm_flag_html = '''<p><svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="green" class="bi bi-check-lg" viewBox="0 0 16 16">
        <path d="M13.485 1.431a1.473 1.473 0 0 1 2.104 2.062l-7.84 9.801a1.473 1.473 0 0 1-2.12.04L.431 8.138a1.473 1.473 0 0 1 2.084-2.083l4.111 4.112 6.82-8.69a.486.486 0 0 1 .04-.045z"/>
        </svg> No torque error (Nm) resulted in surpassing the limits </p>
        <p>Upto five of the maximum torque errors shown below</p>'''

    else:
        st.write("❌ The following Torque error(s) (Nm) resulted in surpassing the limits")
        t_e_nm_flag_html = '''<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="red" class="bi bi-x-lg" viewBox="0 0 16 16">
        <path d="M1.293 1.293a1 1 0 0 1 1.414 0L8 6.586l5.293-5.293a1 1 0 1 1 1.414 1.414L9.414 8l5.293 5.293a1 1 0 0 1-1.414 1.414L8 9.414l-5.293 5.293a1 1 0 0 1-1.414-1.414L6.586 8 1.293 2.707a1 1 0 0 1 0-1.414z"/>
        </svg> The following Torque error(s) (Nm) resulted in surpassing the limits'''

    t_est_err_nm_col1, t_est_err_nm_col2, t_est_err_nm_col3 = st.columns(3)

    min_error_estimated_nm_display, average_error_estimated_nm_display, max_error_estimated_nm_display = limit_format(t_e_nm_flag, min_error_estimated_nm, average_error_estimated_nm, max_error_estimated_nm, "Estimated", "Nm")

    t_est_err_nm_col1.subheader("Minimum Error")
    t_est_err_nm_col1.markdown(min_error_estimated_nm_display, unsafe_allow_html=True)

    t_est_err_nm_col2.subheader("Mean Error")
    t_est_err_nm_col2.markdown(average_error_estimated_nm_display, unsafe_allow_html=True)

    t_est_err_nm_col3.subheader("Maximum Error")
    t_est_err_nm_col3.markdown(max_error_estimated_nm_display, unsafe_allow_html=True)

    st.write(t_estimated_error_table_nm)

st.subheader("Percentage Error")
with st.spinner("Generating Torque Estimated [%] Accuracy Table"):
    st.write("Limit: " + "`± "+str(st.session_state["Estimated Limit [%]"]) + " %`")

    t_estimated_error_table_pc, min_error_estimated_pc, average_error_estimated_pc, max_error_estimated_pc, t_e_pc_flag = error_pc_analysis(selected_data, st.session_state["Estimated Limit [Nm]"], st.session_state["Estimated Limit [%]"], t_estimated, t_demanded, t_estimated, t_measured, speed_round, vdc, idc, t_estimated_error_nm, t_estimated_error_pc)
    
    if t_e_pc_flag == True:
        st.write("✔️ No torque error (%) resulted in surpassing the limits")
        st.write("Upto five of the maximum torque errors shown below")
        t_e_pc_flag_html = '''<p><svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="green" class="bi bi-check-lg" viewBox="0 0 16 16">
        <path d="M13.485 1.431a1.473 1.473 0 0 1 2.104 2.062l-7.84 9.801a1.473 1.473 0 0 1-2.12.04L.431 8.138a1.473 1.473 0 0 1 2.084-2.083l4.111 4.112 6.82-8.69a.486.486 0 0 1 .04-.045z"/>
        </svg> No torque error (%) resulted in surpassing the limits </p>
        <p>Upto five of the maximum torque errors shown below</p>'''

    else:
        st.write("❌ The following Torque error(s) (%) resulted in surpassing the limits")
        t_e_pc_flag_html = '''<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="red" class="bi bi-x-lg" viewBox="0 0 16 16">
        <path d="M1.293 1.293a1 1 0 0 1 1.414 0L8 6.586l5.293-5.293a1 1 0 1 1 1.414 1.414L9.414 8l5.293 5.293a1 1 0 0 1-1.414 1.414L8 9.414l-5.293 5.293a1 1 0 0 1-1.414-1.414L6.586 8 1.293 2.707a1 1 0 0 1 0-1.414z"/>
        </svg> The following Torque error(s) (%) resulted in surpassing the limits'''

    t_est_err_pc_col1, t_est_err_pc_col2, t_est_err_pc_col3 = st.columns(3)
    
    min_error_estimated_pc_display, average_error_estimated_pc_display, max_error_estimated_pc_display = limit_format(t_e_pc_flag, min_error_estimated_pc, average_error_estimated_pc, max_error_estimated_pc, "Estimated", "%")

    t_est_err_pc_col1.subheader("Minimum Error")
    t_est_err_pc_col1.markdown(min_error_estimated_pc_display, unsafe_allow_html=True)

    t_est_err_pc_col2.subheader("Mean Error")
    t_est_err_pc_col2.markdown(average_error_estimated_pc_display, unsafe_allow_html=True)

    t_est_err_pc_col3.subheader("Maximum Error")
    t_est_err_pc_col3.markdown(max_error_estimated_pc_display, unsafe_allow_html=True)

    st.write(t_estimated_error_table_pc)

est_pie = plot_pie(selected_data, selected_data["Torque Estimated Error [Nm]"], selected_data["Torque Estimated Error [%]"], st.session_state["Estimated Limit [Nm]"],  st.session_state["Estimated Limit [%]"])
st.plotly_chart(est_pie)


st.markdown("---")


st.header("Torque Accuracy Plots - *Optional*")
st.subheader("Plot Configuration")


if 'plot_demanded_error_nm' not in st.session_state:
    st.session_state.plot_demanded_error_nm = False
if 'plot_demanded_error_pc' not in st.session_state:
    st.session_state.plot_demanded_error_pc = False
if 'plot_estimated_error_nm' not in st.session_state:
    st.session_state.plot_estimated_error_nm = False
if 'plot_estimated_error_pc' not in st.session_state:
    st.session_state.plot_estimated_error_pc = False

t_d_error_nm_plot1, t_d_error_nm_plot2, t_d_error_nm_plot3, col_preview = st.columns(4)
t_d_error_nm_plot1.selectbox("Chart Type", ["Bowtie","Contour", "Surface","Heatmap","3D Scatter"], key = "T_d_error_chart_type" )

if st.session_state["T_d_error_chart_type"] == "Bowtie":
    st.checkbox("Plot Torque Demanded Bowtie Chart", key = "plot_demanded_error_bowtie")
    st.checkbox("Plot Torque Estimated Bowtie Chart", key = "plot_estimated_error_bowtie")
else:
    st.checkbox("Plot Torque Demanded [Nm] Accuracy Chart", key = "plot_demanded_error_nm")
    st.checkbox("Plot Torque Demanded [%] Accuracy Chart", key = "plot_demanded_error_pc")
    st.checkbox("Plot Torque Estimated [Nm] Accuracy Chart", key = "plot_estimated_error_nm")
    st.checkbox("Plot Torque Estimated [%] Accuracy Chart", key = "plot_estimated_error_pc")
    
t_d_error_nm_plot2.selectbox("Color Scale", ["Sequential", "Diverging"], key = "T_d_error_chart_scale" )

if st.session_state["T_d_error_chart_scale"] == 'Sequential':
    color_map = list(sequential_color_dict().keys())
else:
    color_map = list(diverging_color_dict().keys())

t_d_error_nm_plot3.selectbox("Color Map", color_map, key = "T_d_error_chart_color" )
if  st.session_state["T_d_error_chart_scale"] == 'Sequential':
    color_palette = sequential_color_dict().get(st.session_state["T_d_error_chart_color"])
else:
    color_palette = diverging_color_dict().get(st.session_state["T_d_error_chart_color"])

colormap_preview = plot_color_set(color_palette, st.session_state["T_d_error_chart_color"])
col_preview.image(colormap_preview, use_column_width = True)

t_d_error_nm_plot4, t_d_error_nm_plot5, t_d_error_nm_plot6 = st.columns(3)
t_d_error_nm_plot4.selectbox("Fill", ["NaN", "0"], key = "T_d_error_chart_fill" )
t_d_error_nm_plot5.selectbox("Method", ["linear", "cubic"], key = "T_d_error_chart_method" )
t_d_error_nm_plot6.number_input("Grid Resolution",  min_value = float(-500.0), max_value = float(500.0), value = float(50.0), step = float(1.0), key = "T_d_error_chart_grid")
st.subheader("Data Overlay")
if st.checkbox("Show Data Overlayed"):
    overlay = True
else:
    overlay = False
t_d_error_nm_ovr1, t_d_error_nm_ovr2 = st.columns(2)
t_d_error_nm_ovr1.slider("Opacity",value=0.5,min_value=0.0, max_value=1.0, step=0.01, key = "T_d_error_overlay_opacity")
t_d_error_nm_ovr2.color_picker("Overlay Color", key = "T_d_error_overlay_color")

if (st.session_state["plot_demanded_error_bowtie"] == True) and (st.session_state["T_d_error_chart_type"] == "Bowtie"):
    td_bowtie = plot_bowtie(selected_data,t_demanded, t_demanded_error_nm,t_demanded_error_pc, t_measured,speed_round, st.session_state["Output Limit [Nm]"], st.session_state["Output Limit [%]"])
    st.plotly_chart(td_bowtie)
    td_bowtie_html_string = '''<br><h4> Torque Demanded Error [Nm] ''' + str(st.session_state["T_d_error_chart_type"]) + ''' </h4>'''
    td_bowtie_html_plot = td_bowtie.to_html(default_width = "1200px",default_height = "720px")
else:
    td_bowtie_html_string = ""
    td_bowtie_html_plot = ""


if (st.session_state["plot_estimated_error_bowtie"] == True) and (st.session_state["T_d_error_chart_type"] == "Bowtie"):
    te_bowtie = plot_bowtie(selected_data, t_estimated, t_estimated_error_nm,t_estimated_error_pc, t_measured,speed_round, st.session_state["Estimated Limit [Nm]"], st.session_state["Estimated Limit [%]"])
    st.plotly_chart(te_bowtie)
    te_bowtie_html_string = '''<br><h4> Torque Estimated Error [Nm] ''' + str(st.session_state["T_d_error_chart_type"]) + ''' </h4>'''
    te_bowtie_html_plot = te_bowtie.to_html(default_width = "1200px",default_height = "720px")
else:
    te_bowtie_html_string = ""
    te_bowtie_html_plot = ""

if st.session_state["plot_demanded_error_nm"] == True:
    with st.spinner("Generating Plot"):
        x_td_nm_formatted, y_td_nm_formatted, z_td_nm_formatted = z_col_or_grid(st.session_state["T_d_error_chart_type"],  st.session_state["T_d_error_chart_fill"],  st.session_state["T_d_error_chart_method"],  st.session_state["T_d_error_chart_grid"], selected_data["Speed [rpm] Rounded"],selected_data["Torque Demanded [Nm]"], selected_data["Torque Demanded Error [Nm]"])
        t_d_error_nm_plot = plot_3D(selected_data, speed_round,t_demanded,t_demanded_error_nm,x_td_nm_formatted, y_td_nm_formatted, z_td_nm_formatted, st.session_state["T_d_error_chart_type"], color_palette, overlay, st.session_state["T_d_error_overlay_opacity"], st.session_state["T_d_error_overlay_color"])
        st.plotly_chart(t_d_error_nm_plot)
 
        t_d_error_nm_html_string = '''<br><h4> Torque Demanded Error [Nm] ''' + str(st.session_state["T_d_error_chart_type"]) + ''' </h4>'''

        t_d_error_nm_html_plot = t_d_error_nm_plot.to_html(default_width = "1200px",default_height = "720px")
else:
    t_d_error_nm_html_string = ""
    t_d_error_nm_html_plot = ""

if st.session_state["plot_demanded_error_pc"] == True:
    with st.spinner("Generating Plot"):
        x_td_pc_formatted, y_td_pc_formatted, z_td_pc_formatted = z_col_or_grid(st.session_state["T_d_error_chart_type"],  st.session_state["T_d_error_chart_fill"],  st.session_state["T_d_error_chart_method"],  st.session_state["T_d_error_chart_grid"], selected_data["Speed [rpm] Rounded"],selected_data["Torque Demanded [Nm]"], selected_data["Torque Demanded Error [%]"])
        t_d_error_pc_plot = plot_3D(selected_data, speed_round,t_demanded,t_demanded_error_pc,x_td_pc_formatted, y_td_pc_formatted, z_td_pc_formatted, st.session_state["T_d_error_chart_type"], color_palette, overlay, st.session_state["T_d_error_overlay_opacity"], st.session_state["T_d_error_overlay_color"])
        st.plotly_chart(t_d_error_pc_plot)

        t_d_error_pc_html_string = '''<br><h4> Torque Demanded Error [%] ''' + str(st.session_state["T_d_error_chart_type"]) + ''' </h4>
        <br>'''

        t_d_error_pc_html_plot = t_d_error_pc_plot.to_html(default_width = "1200px",default_height = "720px")
else:
    t_d_error_pc_html_string = ""
    t_d_error_pc_html_plot = ""

if st.session_state["plot_estimated_error_nm"] == True:
    with st.spinner("Generating Plot"):
        x_te_nm_formatted, y_te_nm_formatted, z_te_nm_formatted = z_col_or_grid(st.session_state["T_d_error_chart_type"],  st.session_state["T_d_error_chart_fill"],  st.session_state["T_d_error_chart_method"],  st.session_state["T_d_error_chart_grid"], selected_data["Speed [rpm] Rounded"],selected_data["Torque Demanded [Nm]"], selected_data["Torque Estimated Error [Nm]"])
        t_e_error_nm_plot = plot_3D(selected_data, speed_round,t_estimated,t_estimated_error_nm,x_te_nm_formatted, y_te_nm_formatted, z_te_nm_formatted, st.session_state["T_d_error_chart_type"], color_palette, overlay, st.session_state["T_d_error_overlay_opacity"], st.session_state["T_d_error_overlay_color"])
        st.plotly_chart(t_e_error_nm_plot)

        t_e_error_nm_html_string = '''<br><h4> Torque Estimated Error [Nm] ''' + str(st.session_state["T_d_error_chart_type"]) + ''' </h4>
        <br>'''

        t_e_error_nm_html_plot = t_e_error_nm_plot.to_html(default_width = "1200px",default_height = "720px")
else:
    t_e_error_nm_html_string = ""
    t_e_error_nm_html_plot = ""

if st.session_state["plot_estimated_error_pc"] == True:
    with st.spinner("Generating Plot"):
        x_te_pc_formatted, y_te_pc_formatted, z_te_pc_formatted = z_col_or_grid(st.session_state["T_d_error_chart_type"],  st.session_state["T_d_error_chart_fill"],  st.session_state["T_d_error_chart_method"],  st.session_state["T_d_error_chart_grid"], selected_data["Speed [rpm] Rounded"],selected_data["Torque Demanded [Nm]"], selected_data["Torque Estimated Error [%]"])
        t_e_error_pc_plot = plot_3D(selected_data, speed_round,t_estimated,t_estimated_error_pc, x_te_pc_formatted, y_te_pc_formatted, z_te_pc_formatted, st.session_state["T_d_error_chart_type"], color_palette, overlay, st.session_state["T_d_error_overlay_opacity"], st.session_state["T_d_error_overlay_color"])
        st.plotly_chart(t_e_error_pc_plot)

        t_e_error_pc_html_string = '''<br><h4> Torque Est Error [%] ''' + str(st.session_state["T_d_error_chart_type"]) + ''' </h4>
        <br>'''

        t_e_error_pc_html_plot = t_e_error_pc_plot.to_html(default_width = "1200px",default_height = "720px")
else:
    t_e_error_pc_html_string = ""
    t_e_error_pc_html_plot = ""


st.markdown("---")


st.header("Appendix")
st.subheader("Averaged Results")
st.write(selected_data)
st.subheader("Dataset Table")
st.checkbox("Display original dataset",help="Show orginal data in table, If large dataset could take a long time", key = "Dataset Display")
st.checkbox("Display unaveraged selected symbol dataset, with transients", help = "Show selected symbol dataset,  If large dataset could take a long time", key = "Selected Transient Display")
st.checkbox("Display unaveraged selected symbol dataset, without transients",help = "Show selected symbol dataset,  If large dataset could take a long time", key = "Selected Display")


st.markdown("---") 


st.header("Report")
test_dict = report_details()

st.header("Report Appendix Items")
st.checkbox("Include original dataset",help="Show orginal data as table, If large dataset could take a long time", key = "Report Appendix Full Dataset")

if st.session_state["Report Appendix Full Dataset"] == True:
    report_appendix_full = '''
    <br><h4>Full Dataset Table</h4>
    <br><p>The below table contains all the data uploaded.</p>
    <br>'''+ dataframe.to_html().replace('<table border="1" class="dataframe">','<table class="table table-sm">') +'''
    '''
else: 
    report_appendix_full = ""


files = []
for file in uploaded_file:
    files.append(file.name)

input_files_table = pd.DataFrame(files)
input_files_table = input_files_table.to_html(header=False).replace('<table border="1" class="dataframe">','<table class="table table-borderless table-sm table-hover">')

if st.session_state["Remove Transients"] == True:
    transient_removal_html = ''' 
    <p>Dwell Period: '''+str(st.session_state["Dwell Period"])+'''</p>'''+'''
    <p>Torque Demanded Filter : '''+str(st.session_state["Torque Demanded Filter"])+''' Nm </p>'''

else:
    transient_removal_html = ''' 
    <p>Not applied</p>
    '''

if st.session_state["T_d_error_chart_type"] == "Contour":
    plot_info = '''The below contour plot(s) shows Torque against speed rounded (to the nearest: ''' + str(st.session_state["Speed Base"]) + ''' rpm) 
    <br>Data between measured data points have been interpolated between the nearest available data using the '''+ str(st.session_state["T_d_error_chart_method"])+''' method.
    <br>The grid resolution for this contour plot has been set to '''+ str(st.session_state["T_d_error_chart_grid"]) + '''
    <br>Missing data has been filled with the following value: ''' + str(st.session_state["T_d_error_chart_fill"])+'''
    '''

elif st.session_state["T_d_error_chart_type"] == "Surface":
    plot_info = '''The below surface plot(s) shows Torque against speed rounded (to the nearest: ''' + str(st.session_state["Speed Base"]) + ''' rpm) and Torque error
    <br>Data between measured data points have been interpolated between the nearest available data using the '''+ str(st.session_state["T_d_error_chart_method"])+''' method.
    <br>The grid resolution for this contour plot has been set to '''+ str(st.session_state["T_d_error_chart_grid"]) + '''
    <br>Missing data has been filled with the following value: ''' + str(st.session_state["T_d_error_chart_fill"])+'''
    '''

elif st.session_state["T_d_error_chart_type"] == "Heatmap":
    plot_info = '''The below heatmap plot(s) shows Torque against speed rounded (to the nearest: ''' + str(st.session_state["Speed Base"]) + ''' rpm)
    <br>Data between measured data points have been interpolated between the nearest available data using the '''+ str(st.session_state["T_d_error_chart_method"])+''' method.
    <br>The grid resolution for this contour plot has been set to '''+ str(st.session_state["T_d_error_chart_grid"]) + '''
    <br>Missing data has been filled with the following value: ''' + str(st.session_state["T_d_error_chart_fill"])+'''
    '''

elif st.session_state["T_d_error_chart_type"] == "Scatter 3D":
    plot_info = '''The below 3D Scatter plot(s) shows Torque against speed rounded (to the nearest: ''' + str(st.session_state["Speed Base"]) + ''' rpm) and Torque error'''
             
elif st.session_state["T_d_error_chart_type"] == "Bowtie":
    plot_info = '''The bowtie plot(s) below shows the averaged torque errors and the associated error limits.'''





html_string = '''
<html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU" crossorigin="anonymous">
        <style>body{ margin:100 100; background:white; }</style>
    </head>
    <body>
        <div class="container h-10">
            <div class="row h-10 justify-content-center align-items-center">
            <img src="https://turntide.com/wp-content/themes/turntide2021/theme/static/images/logo-color.svg" style="width: 400px" />
            <br>
            </div>
        </div>

        <h1 class="display-1 text-center">Torque Accuracy Results</h1>

        <br>

        <!-- *** Section 1 *** --->
        <h2>Report Details</h2>
        <br>
            <h4>Testing</h4>

            <table class="table">
              <tbody>
                <tr>
                <th scope="row", width = 300>Test Name</th>
                  <td>'''+ str(st.session_state["Test Name"]) + '''</td>
                </tr>
                <th scope="row", width = 300>User</th>
                  <td>'''+ str(st.session_state["User"]) + '''</td>
                </tr>
                <th scope="row", width = 300>Test Date</th>
                  <td>'''+ str(st.session_state["Test Date"]) + '''</td>
                </tr>
                <th scope="row", width = 300>Test Note</th>
                  <td>'''+ str(st.session_state["Test Note"]) + '''</td>
                </tr>
              </tbody>
            </table>


                <br>

            <h4>Software</h4>

            <table class="table">
              <tbody>
                <tr>
                <th scope="row", width = 300>Dyno</th>
                  <td>'''+ str(st.session_state["Dyno"]) + '''</td>
                </tr>
                <th scope="row", width = 300>Torque Speed Sensor</th>
                  <td>'''+ str(st.session_state["Torque Speed Sensor"]) + '''</td>
                </tr>
                <th scope="row", width = 300>Sensor Calibration Date</th>
                  <td>'''+ str(st.session_state["Sensor Calibration Date"]) + '''</td>
                </tr>
              </tbody>
            </table>
            <br>

            <h4>Motor</h4>
            <table class="table">
              <tbody>
                <tr>
                <th scope="row", width = 300>Software Level</th>
                  <td>'''+ str(st.session_state["Software Level"]) + '''</td>
                </tr>
                <th scope="row", width = 300>Software Location</th>
                  <td>'''+ str(st.session_state["Software Location"]) + '''</td>
                </tr>
                <th scope="row", width = 300>Software Notes</th>
                  <td>'''+ str(st.session_state["Software Notes"]) + '''</td>
                </tr>
              </tbody>
            </table>
            <br>

            <h4>Controller</h4>
            <table class="table">
              <tbody>
                <tr>
                <th scope="row", width = 300>Controller Manufacturer</th>
                  <td>'''+ str(st.session_state["Controller Manufacturer"]) + '''</td>
                </tr>
                <th scope="row", width = 300>Controller Model</th>
                  <td>'''+ str(st.session_state["Controller Model"]) + '''</td>
                </tr>
                <th scope="row", width = 300>Controller Sample</th>
                  <td>'''+ str(st.session_state["Controller Sample"]) + '''</td>
                </tr>
                <th scope="row", width = 300>Controller Notes</th>
                  <td>'''+ str(st.session_state["Controller Notes"]) + '''</td>
                </tr>
              </tbody>
            </table>
            <br>

            <h4>Dyno</h4>
            <table class="table">
              <tbody>
                <tr>
                <th scope="row", width = 300>Motor Manufacturer</th>
                  <td>'''+ str(st.session_state["Motor Manufacturer"]) + '''</td>
                </tr>
                <th scope="row", width = 300>Motor Model</th>
                  <td>'''+ str(st.session_state["Motor Model"]) + '''</td>
                </tr>
                <th scope="row", width = 300>Motor Sample</th>
                  <td>'''+ str(st.session_state["Motor Sample"]) + '''</td>
                </tr>
                <th scope="row", width = 300>Motor Notes</th>
                  <td>'''+ str(st.session_state["Motor Notes"]) + '''</td>
                </tr>
              </tbody>
            </table>
            <br>

            <h4>Limits</h4>
            <table class="table">
              <tbody>
                <tr>
                <th scope="row", width = 300>Output [Nm]</th>
                  <td>'''+ str(st.session_state["Output Limit [Nm]"]) + '''</td>
                </tr>
                <th scope="row", width = 300>Output [%]</th>
                  <td>'''+ str(st.session_state["Output Limit [%]"]) + '''</td>
                </tr>
                <th scope="row", width = 300>Estimated [Nm]</th>
                  <td>'''+ str(st.session_state["Estimated Limit [Nm]"]) + '''</td>
                </tr>
                <th scope="row", width = 300>Estimated [%]</th>
                  <td>'''+ str(st.session_state["Estimated Limit [%]"]) + '''</td>
                </tr>
              </tbody>
            </table>
            <br>

            <!-- *** Section 2 *** --->
            <h2>Input Files</h2>
                '''+ input_files_table +'''
                <br>

            <h2>Transient Removal</h2> 
                '''+ transient_removal_html +'''
                '''+ transient_removal_sample_plot.to_html(default_width = "1200px",default_height = "720px") +'''
                <br>

            <h2>Unique Points</h2>
                <p>There are '''+ str(number_of_rounded_speeds)+''' unique speed points identified.</p>
                <p>There are X unique voltage points indentified.</p>
                <br>

        <!-- *** Section 3 *** --->
        <h2>Torque Output Accuracy</h2>
        <p>Minimum, Mean and Maximum errors are absoluted.</p>

            <br>
            <h4>Newton Meter Error</h4>
            <p>Limit:&plusmn'''+ str(st.session_state["Output Limit [Nm]"]) +'''Nm</p>
            ''' + t_d_nm_flag_html + '''
            
            <table class="table">
              <thead>
                <tr>
                  <th scope="col">Minimum</th>
                  <th scope="col">Mean</th>
                  <th scope="col">Maximum</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>''' + min_error_demanded_nm_display + '''</td>
                  <td>''' + average_error_demanded_nm_display + '''</td>
                  <td>''' + max_error_demanded_nm_display + '''</td>
                </tr>
              </tbody>
            </table>

            ''' + t_demanded_error_table_nm.to_html(index=False, classes='table table-striped table-sm text-right', justify='center', border="0") + '''
            <br>
            <h4>Percentage Error</h4>
            
            <p>Limit:&plusmn'''+ str(st.session_state["Output Limit [%]"]) +'''%</p>
            ''' + t_d_pc_flag_html + '''
            
            <table class="table">
              <thead>
                <tr>
                  <th scope="col">Minimum</th>
                  <th scope="col">Mean</th>
                  <th scope="col">Maximum</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>''' + min_error_demanded_pc_display + '''</td>
                  <td>''' + average_error_demanded_pc_display + '''</td>
                  <td>''' + max_error_demanded_pc_display + '''</td>
                </tr>
              </tbody>
            </table>

            ''' + t_demanded_error_table_pc.to_html(index=False, classes='table table-striped table-sm text-right', justify='center', border="0") + '''
            <br>

            <h4> Pass : Fail </h4>

            <div class="container">
            <div class="row">
                <div class="col align-self-start">
                
                </div>
                <div class="col align-self-center">
                ''' + dem_pie.to_html(default_width = "500px",default_height = "500px") + '''
                </div>
                <div class="col align-self-end">
                
                </div>
            </div>
            </div> 

            <br>

        <h2>Torque Estimated Accuracy</h2>

            <br>
            <h4>Newton Meter Error</h4>
            <p>Limit:&plusmn'''+ str(st.session_state["Estimated Limit [Nm]"]) +'''Nm</p>
            ''' + t_e_nm_flag_html + '''
            
            <table class="table">
              <thead>
                <tr>
                  <th scope="col">Minimum</th>
                  <th scope="col">Mean</th>
                  <th scope="col">Maximum</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>''' + min_error_estimated_nm_display + '''</td>
                  <td>''' + average_error_estimated_nm_display + '''</td>
                  <td>''' + max_error_estimated_nm_display + '''</td>
                </tr>
              </tbody>
            </table>

            '''+ t_estimated_error_table_nm.to_html(index=False, classes='table table-striped table-sm text-right', justify='center', border="0") +'''

            <br>
            <h4>Percentage Error</h4>

            <p>Limit:&plusmn'''+ str(st.session_state["Estimated Limit [%]"]) +'''%</p>
            ''' + t_e_pc_flag_html + '''
            
            <table class="table">
              <thead>
                <tr>
                  <th scope="col">Minimum</th>
                  <th scope="col">Mean</th>
                  <th scope="col">Maximum</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>''' + min_error_estimated_pc_display + '''</td>
                  <td>''' + average_error_estimated_pc_display + '''</td>
                  <td>''' + max_error_estimated_pc_display + '''</td>
                </tr>
              </tbody>
            </table>

            '''+ t_estimated_error_table_pc.to_html(index=False, classes='table table-striped table-sm text-right', justify='center', border="0") +'''
            <br>

            <h4> Pass : Fail </h4>
            <div class="container">
            <div class="row">
                <div class="col align-self-start">
                
                </div>
                <div class="col align-self-center">
                ''' + est_pie.to_html(default_width = "500px",default_height = "500px") + '''
                </div>
                <div class="col align-self-end">
                
                </div>
            </div>
            </div> 

        <!-- *** Section 4 *** --->
        <h2>Plots</h2>
            <p>Selected plots will appear here.</p>  

            <div class="container">
            <div class="row">
                <div class="col align-self-start">
                
                </div>
                <div class="col align-self-center">
                ''' + dem_pie.to_html(default_width = "500px",default_height = "500px") + '''
                </div>
                <div class="col align-self-end">
                
                </div>
            </div>
        </div>         
            ''' + plot_info + '''
  
                    ''' + td_bowtie_html_string + '''
            <div class="container">
                <div class="row">
                    <div class="col align-self-start">

                    </div>
                    <div class="col align-self-center">
                    ''' + td_bowtie_html_plot + '''
                    </div>
                    <div class="col align-self-end">

                    </div>
                </div>
            </div>

            ''' + te_bowtie_html_string + '''
            <div class="container">
                <div class="row">
                    <div class="col align-self-start">

                    </div>
                    <div class="col align-self-center">
                    ''' + te_bowtie_html_plot + '''
                    </div>
                    <div class="col align-self-end">

                    </div>
                </div>
            </div>

            ''' + t_d_error_nm_html_string + '''
            <div class="container">
                <div class="row">
                    <div class="col align-self-start">

                    </div>
                    <div class="col align-self-center">
                    ''' + t_d_error_nm_html_plot + '''
                    </div>
                    <div class="col align-self-end">

                    </div>
                </div>
            </div>

            ''' + t_d_error_pc_html_string + '''
            <div class="container">
                <div class="row">
                    <div class="col align-self-start">

                    </div>
                    <div class="col align-self-center">
                    ''' + t_d_error_pc_html_plot + '''
                    </div>
                    <div class="col align-self-end">

                    </div>
                </div>
            </div>
            
        
        <!-- *** Section 4 *** --->
        <br>
        <h2>Appendix</h2>
        <br>
            <h4>Data analysed as Table</h4> 
            ''' + selected_data.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped table-sm">') + '''
            ''' + report_appendix_full + '''
    </body>
</html>
'''

bl, report_col ,br = st.columns(3)

report_col.download_button(
    label="Download Report",
    data=html_string,
    file_name="myfile.html",
    mime="application/octet-stream"
)