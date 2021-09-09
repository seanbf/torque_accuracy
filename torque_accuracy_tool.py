import streamlit as st
import pandas as pd
#from src.layout import sidebar_md
from src.utils import load_dataframe

page_config = st.set_page_config(
                                page_title              ="Torque Accuracy Tool", 
                                page_icon               ="🎯", 
                                layout                  ='wide', 
                                initial_sidebar_state   ='auto'
                                )

def sidebar_md():
    sidebar_config =     """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 600px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 600px;
        margin-left: -600px;
    }   
    </style>
    """
    return sidebar_config

st.sidebar.title('Torque Accuracy Tool')
st.sidebar.markdown('''<small>v0.1</small>''', unsafe_allow_html=True)

#Set up sidebar.
sidebar_config = sidebar_md()
st.markdown(sidebar_config, unsafe_allow_html=True)

#Ask for file upload and read.
uploaded_file = st.sidebar.file_uploader(   
                                        label="",
                                        accept_multiple_files=False,
                                        type=['csv', 'xlsx']
                                        )

if uploaded_file is None:
    st.info("Please upload file(s) in the sidebar")
    st.stop()

elif uploaded_file is not None:

    original_file_name  = uploaded_file.name

    dataframe, columns  = load_dataframe(uploaded_file=uploaded_file)

torque_analysis = st.sidebar.radio("Torque Analysis", ["Output", "Estimated", "Output & Estimated"], key = "torque_analysis")

with st.sidebar.expander("Report", expanded=False):
    report_name             = st.text_input("Test Name")

with st.sidebar.expander("Test Limits", expanded=True):
    if torque_analysis == "Output":
        output_limit_nm     = st.number_input("Output Limit [Nm]",      min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0))
        output_limit_pc     = st.number_input("Output Limit [%]",       min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0))

    elif torque_analysis == "Estimated":
        estimated_limit_nm  = st.number_input("Estimated Limit [Nm]",   min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0))
        estimated_limit_pc  = st.number_input("Estimated Limit [%]",    min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0))

    elif torque_analysis == "Output & Estimated":
        output_limit_nm     = st.number_input("Output Limit [Nm]",      min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0))
        output_limit_pc     = st.number_input("Output Limit [%]",       min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0))
        estimated_limit_nm  = st.number_input("Estimated Limit [Nm]",   min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0))
        estimated_limit_pc  = st.number_input("Estimated Limit [%]",    min_value = float(-100.0), max_value = float(100.0), value = float(5.0), step = float(1.0))

with st.sidebar.expander("Signals", expanded=True):
    if torque_analysis == "Output":
        torque_measured     = st.selectbox("Torque Measured",list(columns) )
        torque_demanded     = st.selectbox("Torque Demanded",list(columns) )

    elif torque_analysis == "Estimated":
        torque_measured     = st.selectbox("Torque Measured",list(columns) )
        torque_estimated    = st.selectbox("Torque Estimated",list(columns) )

    elif torque_analysis == "Output & Estimated":
        torque_measured     = st.selectbox("Torque Measured",list(columns) )
        torque_demanded     = st.selectbox("Torque Demanded",list(columns) )
        torque_estimated    = st.selectbox("Torque Estimated",list(columns) )
    
    dc_voltage              = st.selectbox("DC Voltage",list(columns) )
    dc_current              = st.selectbox("DC Current",list(columns) )
    speed                   = st.selectbox("Speed",list(columns) )
    #id                      = st.selectbox("Id",list(columns) )
    #iq                      = st.selectbox("Iq",list(columns) )
    #id                      = st.selectbox("Ud",list(columns) )
    #iq                      = st.selectbox("Uq",list(columns) )

