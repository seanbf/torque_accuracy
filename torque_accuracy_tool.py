from hashlib import new
from attr import validate
from numpy.core.fromnumeric import size
from numpy.lib.arraysetops import isin
import streamlit as st
import pandas as pd
from streamlit.state.session_state import SessionState, Value
from src.layout import test_details, limits, signals
from src.utils import load_dataframe, col_removal, determine_transients, sample_transients
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
st.markdown("---")
st.subheader("1. Upload file(s)")
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


st.subheader("2. Test Details - (*Optional*)")
test_dict = test_details()

st.subheader("3. Configure Test Limits")
st.radio("Torque Analysis", ["Output & Estimated","Output"], key = "Analysis Mode")
limits(st.session_state["Analysis Mode"])

st.subheader("4. Configure Signals")
st.write("All signals must be manually selected if auto-select cannot find them.")
signals(st.session_state["Analysis Mode"], columns)
if any(value == 'Not Selected' for value in st.session_state.values()) == True:
    st.stop()

st.subheader("5. Torque Demanded against Speed - (*Optional*)")
st.checkbox("Plot Test Data", value = False, key = "Plot Test Data")
st.write("Below is a plot of the data representing Torque Demanded and Speed")
st.write("This is useful to determine if the data uploaded contains the correct test cases / behaviour")
selected_data = col_removal(dataframe, list(st.session_state.values()))

if (st.session_state["Plot Test Data"] == True):
    with st.spinner("Generating Demanded Test Point Plot"):
        st.plotly_chart(demanded_plot(selected_data, st.session_state))


st.subheader("6. Remove Transients - (*Optional*)")
st.checkbox("Remove Transients from Data", value = True, key = "Transient Removal")
if st.session_state["Transient Removal"] == True:
    with st.spinner("Generating transient removal tool"):
        st.write("Make sure the transient removal process is removing the required data; when there is a step change and time taken until steady state is reached.")
        st.markdown("If this is not achieved, adjust the variable `Dwell Period` using the slider below")
        st.markdown("Scan through torque steps using the `Sample` slider to determine if the `Dwell Period` is appropiate for the range of torque steps.")

        dwell_col, sample_col = st.columns(2)
        dwell_col.slider("Dwell Period", min_value=0, max_value=5000, step=1, value= 500, key = "Dwell Period")
        Step_index, Stop_index          = determine_transients(selected_data, st.session_state) 
        sample_col.slider("Sample", min_value=1, max_value=abs(len(Stop_index)-1), step=1, value= 5, key = "Sample")
        transient_sample                = sample_transients(Step_index, Stop_index, dataframe, st.session_state)    
        transient_removal_sample_plot   = transient_removal_plot(transient_sample, Step_index, Stop_index, dataframe, st.session_state)
        st.plotly_chart(transient_removal_sample_plot)
col1, col2, col3 = st.columns([1,1,1])
col2.button("Remove Transients", key = "Remove Transients")  

if st.session_state["Remove Transients"] == True:
    st.write("clicked")
report_table = pd.DataFrame([test_dict])
report_table = report_table.astype(str)
report_table = report_table.T