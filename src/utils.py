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

def determine_transients(df, t_demanded, dwell_period):
    df["Step_Change"] = '0'
    df["Step_Change"] = df[t_demanded].diff()

    Step_index          = ( df.index[df['Step_Change'] != 0] - 1 )
    Stop_index          = Step_index + dwell_period

    return Step_index, Stop_index

def sample_transients(Step_index, Stop_index, df, test_dict):

    transient_sample = df.iloc[Step_index[test_dict["Sample"]]-250 : Stop_index[test_dict["Sample"]]+250]
    
    return transient_sample

def col_removal(data, list_to_keep):
    selected_data = pd.DataFrame
    selected_data = data.columns.intersection(list_to_keep)
    data = data[selected_data]

    return data

def transient_removal(df, Step_index, Stop_index):
    
#Transient Removal
    delete_slice = np.array(0)

    for x in range( len(Step_index) ):
        temp_slice = np.arange(Step_index[x], Stop_index[x])
        delete_slice = np.append(delete_slice, temp_slice)

    delete_slice = abs(delete_slice)
    df = df.drop(index = delete_slice)
    return df

def myround(x, base):
    return base * round(x/base)

def round_speeds(df, speed_signal, torque_demanded_signal, base):
    # Round measured speed to the nearest 50rpm.
    
    df[speed_signal + " Rounded"] = myround(df[speed_signal], base)

    # Group the data in the dataframe by the measured speed (rounded) and torque demanded.
    # Get average of all data within those subgroups and create new dataframe, df.
    df = df.groupby([speed_signal + " Rounded", torque_demanded_signal], as_index=False).agg("mean")

    return df

def torque_error_calc(df, t_demanded, t_estimated, t_measured, t_demanded_error_nm, t_demanded_error_pc, t_estimated_error_nm, t_estimated_error_pc):
    df[t_demanded_error_nm]    = 0
    df[t_demanded_error_nm]    = df[t_demanded_error_nm].where(df[t_demanded] >= 0, df[t_measured] - df[t_demanded])
    df[t_demanded_error_nm]    = df[t_demanded_error_nm].where(df[t_demanded] < 0, df[t_demanded] - df[t_measured])
    df[t_demanded_error_pc]    = ( (df[t_demanded] - df[t_measured]) / df[t_measured]) * 100

    df[t_estimated_error_nm]   = 0
    df[t_estimated_error_nm]   = df[t_estimated_error_nm].where(df[t_estimated] >= 0, df[t_measured] - df[t_estimated])
    df[t_estimated_error_nm]   = df[t_estimated_error_nm].where(df[t_estimated] < 0, df[t_estimated] - df[t_measured])
    df[t_estimated_error_pc]   =  ( (df[t_measured] - df[t_estimated]) / df[t_estimated]) * 100

    return df

def torque_demanded_error_nm_analysis(df, SpecLimit_Torque_Accuracy_Nm, SpecLimit_Torque_Accuracy_Pc, t_demanded, t_estimated, t_measured, speed_round, vdc, idc, t_demanded_error_nm, t_demanded_error_pc):

    if ( abs(df[t_demanded]) > SpecLimit_Torque_Accuracy_Nm ).any():
    
        T_Demanded_Error_Table_Nm = df[abs(df[t_demanded]) > SpecLimit_Torque_Accuracy_Nm].copy()
    
        if ( abs(T_Demanded_Error_Table_Nm[t_demanded]) < (SpecLimit_Torque_Accuracy_Nm/(SpecLimit_Torque_Accuracy_Pc/100)) ).any():
        
            T_Demanded_Error_Table_Nm = T_Demanded_Error_Table_Nm[abs(T_Demanded_Error_Table_Nm[t_demanded]) < (SpecLimit_Torque_Accuracy_Nm/(SpecLimit_Torque_Accuracy_Pc/100))].copy()

            T_Demanded_Error_Table_Nm.sort_values(by=t_demanded_error_nm, key = abs, ascending = False, inplace = True)

            T_Demanded_Error_Table_Nm = T_Demanded_Error_Table_Nm.filter([vdc,speed_round, t_demanded,t_estimated, t_measured, t_demanded_error_nm, t_demanded_error_pc])

        else:
            st.write("No torque demanded error(Nm) resulted in surpassing the specification")
            st.write("Upto five of the maximum torque demanded errors (Nm) shown below")

            T_Demanded_Error_Table_Nm.sort_values(by=t_demanded_error_nm,key = abs, ascending = False, inplace = True)

            T_Demanded_Error_Table_Nm = T_Demanded_Error_Table_Nm[0:5]

            T_Demanded_Error_Table_Nm = T_Demanded_Error_Table_Nm.filter([vdc, idc,speed_round, t_demanded,t_estimated, t_measured, t_demanded_error_nm, t_demanded_error_pc])
        
    else:
        st.write("No torque demanded error(Nm) resulted in surpassing the specification")
        st.write("Upto five of the maximum torque demanded errors shown below")

        T_Demanded_Error_Table_Nm = df.copy()

        T_Demanded_Error_Table_Nm.sort_values(by=[t_demanded_error_nm, t_demanded_error_pc],key = abs, ascending = False, inplace = True)

        T_Demanded_Error_Table_Nm = T_Demanded_Error_Table_Nm[0:5]

        T_Demanded_Error_Table_Nm = T_Demanded_Error_Table_Nm.filter([vdc,speed_round, t_demanded,t_estimated, t_measured, t_demanded_error_nm, t_demanded_error_pc])
    
    return T_Demanded_Error_Table_Nm