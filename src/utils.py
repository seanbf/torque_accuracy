import numpy as np
import pandas as pd
import streamlit as st

@st.cache
def load_dataframe(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
    except:
        df = pd.read_excel(uploaded_file)

    columns = list(df.columns)
    columns.append(None)

    return df, columns

#def remove_unused(data, test_dict):
#    col_to_drop = []
#    for column in data.column()


@st.cache
def transient_removal(data, test_dict):
    data["Step_Change"]   = '0'
    data["Step_Change"]   = data["Torque Demanded"].diff()

    Step_index = ( data.index[data['Step_Change'] != 0] - 1 )
    Stop_index = Step_index + test_dict["Dwell Period"]

    # Plot transient removal sample
    transient_sample = data.iloc[Step_index[3]-250 : Stop_index[3]+250]

    return Step_index, Stop_index, transient_sample