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



def determine_transients(data, test_dict):
    data["Step_Change"] = '0'
    data["Step_Change"] = data[test_dict["Torque Demanded"]].diff()

    Step_index          = ( data.index[data['Step_Change'] != 0] - 1 )
    Stop_index          = Step_index + test_dict["Dwell Period"]

    return Step_index, Stop_index

def sample_transients(Step_index, Stop_index, data, test_dict):

    transient_sample = data.iloc[Step_index[test_dict["Sample"]]-250 : Stop_index[test_dict["Sample"]]+250]
    
    return transient_sample

def col_removal(data, list_to_keep):
    selected_data = pd.DataFrame
    selected_data = data.columns.intersection(list_to_keep)
    data = data[selected_data]

    return data