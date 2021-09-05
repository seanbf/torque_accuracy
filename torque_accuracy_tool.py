import streamlit as st
import pandas as pd
from src.layout import containers
from src.utils import load_dataframe
from src.plotter import demanded_plot

page_config = st.set_page_config(
                                page_title              ="Torque Accuracy Tool", 
                                page_icon               ="🎯", 
                                layout                  ='wide', 
                                initial_sidebar_state   ='auto'
                                )

st.sidebar.title('Torque Accuracy Tool')
st.sidebar.markdown('''<small>v0.1</small>''', unsafe_allow_html=True)

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

    columns             = list(columns)

    columns.insert(0, "Not Selected")

plot_test_data = st.sidebar.checkbox("Plot Test Data", value = True)
transient_removal = st.sidebar.checkbox("Remove Transients from Data", value = True)
analysis_toggle = st.sidebar.radio("Torque Analysis", ["Output", "Estimated", "Output & Estimated"], key = "torque_analysis")

test_dict = containers(analysis_toggle, columns)

if any(value == 'Not Selected' for value in test_dict.values()) == True:
    st.info("Please select symbols in the sidebar")
    st.stop()

l_func = lambda x, y: list((set(x)- set(y))) + list((set(y)- set(x))) 

non_match = l_func(columns, test_dict.values())

dataframe = dataframe.drop(columns=[col for col in dataframe if col not in non_match])

st.write(dataframe.head())

report_table = pd.DataFrame([test_dict])
report_table = report_table.astype(str)
report_table = report_table.T

if (plot_test_data == True):
    with st.expander("Test Demanded", expanded = True):
        with st.spinner("Generating Demanded Test Point Plot"):
            st.plotly_chart(demanded_plot(dataframe, test_dict))

if transient_removal == True:
    with st.expander("Transient Removal", expanded=True):
        st.write("Make sure the transient removal process is removing the required data; when there is a step change and time taken until steady state is reached.")
        st.write("If this is not achieved, adjust the variable dwell using the slider")
        st.slider("Dwell Period", min_value=0, max_value=5000, step=1, value= 500)  
        st.plotly_chart()