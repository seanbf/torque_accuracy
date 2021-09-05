from hashlib import new
from numpy.core.fromnumeric import size
from numpy.lib.arraysetops import isin
import streamlit as st
import pandas as pd
from src.layout import containers
from src.utils import load_dataframe, col_removal, determine_transients, sample_transients
from src.plotter import demanded_plot, transient_removal_plot

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

plot_test_data      = st.sidebar.checkbox("Plot Test Data", value = True)
transient_removal   = st.sidebar.checkbox("Remove Transients from Data", value = True)
analysis_toggle     = st.sidebar.radio("Torque Analysis", ["Output & Estimated","Output"], key = "torque_analysis")

test_dict = containers(analysis_toggle, columns)

if any(value == 'Not Selected' for value in test_dict.values()) == True:
    st.info("Please select symbols in the sidebar")
    st.stop()

# may just have dataframe reassign.
selected_data = col_removal(dataframe, list(test_dict.values()))

report_table = pd.DataFrame([test_dict])
report_table = report_table.astype(str)
report_table = report_table.T

if (plot_test_data == True):
    with st.expander("Test Demanded", expanded = True):
        with st.spinner("Generating Demanded Test Point Plot"):
            st.plotly_chart(demanded_plot(selected_data, test_dict))

if transient_removal == True:
    with st.expander("Transient Removal", expanded=True):
        st.write("Make sure the transient removal process is removing the required data; when there is a step change and time taken until steady state is reached.")
        st.write("If this is not achieved, adjust the variable dwell using the slider")
        
        dwell_col, sample_col = st.columns(2)
        test_dict["Dwell Period"]       = dwell_col.slider("Dwell Period", min_value=0, max_value=5000, step=1, value= 500)

        Step_index, Stop_index          = determine_transients(selected_data, test_dict)
        test_dict["Sample"]             = sample_col.slider("Sample", min_value=0, max_value=len(Stop_index), step=1, value= 5)
        transient_sample                = sample_transients(Step_index, Stop_index, dataframe, test_dict)

        transient_removal_sample_plot   = transient_removal_plot(transient_sample, Step_index, Stop_index, dataframe, test_dict)
        st.plotly_chart(transient_removal_sample_plot)
        