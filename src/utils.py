import numpy as np
from scipy.interpolate import griddata
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
    df[t_demanded_error_nm]    = df[t_demanded_error_nm].where(df[t_demanded] >= 0, df[t_demanded] - df[t_measured])
    df[t_demanded_error_nm]    = df[t_demanded_error_nm].where(df[t_demanded] < 0, df[t_measured] - df[t_demanded])
    df[t_demanded_error_pc]    = ( (df[t_demanded] - df[t_measured]) / df[t_measured]) * 100

    df[t_estimated_error_nm]   = 0
    df[t_estimated_error_nm]   = df[t_estimated_error_nm].where(df[t_estimated] >= 0, df[t_measured] - df[t_estimated])
    df[t_estimated_error_nm]   = df[t_estimated_error_nm].where(df[t_estimated] < 0, df[t_estimated] - df[t_measured])
    df[t_estimated_error_pc]   =  ( (df[t_measured] - df[t_estimated]) / df[t_estimated]) * 100

    return df

def error_nm_analysis(df, limit_nm, limit_pc, t_to_analyse ,t_demanded, t_estimated, t_measured, speed_round, vdc, idc, error_nm, error_pc):

    if ( abs(df[error_nm]) > limit_nm ).any():
    
        error_table_nm = df[abs(df[error_nm]) > limit_nm].copy()
    
        if ( abs(error_table_nm[t_to_analyse]) < (limit_nm/(limit_pc/100)) ).any():
            st.write((limit_nm/(limit_pc/100)))
            error_table_nm = error_table_nm[abs(error_table_nm[t_to_analyse]) < (limit_nm/(limit_pc/100))].copy()

            error_table_nm.sort_values(by=error_nm, key = abs, ascending = False, inplace = True)

            error_table_nm = error_table_nm.filter([error_nm, error_pc, t_measured, t_demanded, t_estimated, speed_round, vdc, idc])
            
            st.write("❌ The following Torque error(s) (Nm) resulted in surpassing the limits")
        else:

            error_table_nm.sort_values(by=error_nm,key = abs, ascending = False, inplace = True)

            error_table_nm = error_table_nm[0:5]

            error_table_nm = error_table_nm.filter([error_nm, error_pc, t_measured, t_demanded, t_estimated, speed_round, vdc, idc])
            
            st.write("✔️ No torque error (Nm) resulted in surpassing the limits")
            st.write("Upto five of the maximum torque errors (Nm) shown below")
            st.write("These errors are above " + str((limit_nm/(limit_pc/100))) + " Nm demand, and therefore are omitted.")
    else:
        error_table_nm = df.copy()

        error_table_nm.sort_values(by=[error_nm, error_pc],key = abs, ascending = False, inplace = True)

        error_table_nm = error_table_nm[0:5]

        error_table_nm = error_table_nm.filter([error_nm, error_pc, t_measured, t_demanded, t_estimated, speed_round, vdc, idc])
        
        st.write("✔️ No torque error (Nm) resulted in surpassing the limits")
        st.write("Upto five of the maximum torque errors shown below")

    min_error       = min(abs(error_table_nm[error_nm]))
    average_error   = np.mean(abs(error_table_nm[error_nm]))
    max_error       = max(abs(error_table_nm[error_nm]))

    return error_table_nm, min_error, average_error, max_error

def error_pc_analysis(df, limit_nm, limit_pc, t_to_analyse, t_demanded, t_estimated, t_measured, speed_round, vdc, idc, error_nm, error_pc):

    if ( abs(df[error_pc]) > limit_pc ).any():
    
        error_table_pc = df[abs(df[error_pc]) > limit_pc].copy()

        if ( abs(error_table_pc[t_to_analyse]) < (limit_nm/(limit_pc/100)) ).any():
        
            error_table_pc = error_table_pc[abs(error_table_pc[t_to_analyse]) < (limit_nm/(limit_pc/100))].copy()

            error_table_pc.sort_values(by=error_pc, key = abs, ascending = False, inplace = True)

            error_table_pc = error_table_pc.filter([error_pc, error_nm, t_measured, t_demanded, t_estimated, speed_round, vdc, idc])

            st.write("❌ The following Torque error(s) (%) resulted in surpassing the limits")
        else:

            st.write("✔️ No torque error(Nm) resulted in surpassing the limits")
            st.write("Upto five of the maximum torque errors (%) shown below")

            error_table_pc.sort_values(by=error_pc,key = abs, ascending = False, inplace = True)

            error_table_pc = error_table_pc[0:5]

            error_table_pc = error_table_pc.filter([error_pc, error_nm, t_measured, t_demanded, t_estimated, speed_round, vdc, idc])

    else:
        st.write("✔️ No torque error (%) resulted in surpassing the limits")
        st.write("Upto five of the maximum torque errors shown below")

        error_table_pc = df.copy()

        error_table_pc.sort_values(by=[error_pc, error_nm],key = abs, ascending = False, inplace = True)

        error_table_pc = error_table_pc[0:5]

        error_table_pc = error_table_pc.filter([error_pc, error_nm, t_measured, t_demanded, t_estimated, speed_round, vdc, idc])


    min_error       = min(abs(error_table_pc[error_pc]))
    average_error   = np.mean(abs(error_table_pc[error_pc]))
    max_error       = max(abs(error_table_pc[error_pc]))
    
    return error_table_pc, min_error, average_error, max_error

def z_col_or_grid(chart_type, fill, method, grid_res, x_in, y_in, z_in):
    '''
    Depending on graph wanted, format data as grid or columns
    '''
    x = x_in
    y = y_in
    z = z_in

    if chart_type != '3D Scatter':

        xi = np.linspace( float(min(x)), float(max(x)), int(grid_res) )
        yi = np.linspace( float(min(y)), float(max(y)), int(grid_res) )

        X,Y = np.meshgrid(xi,yi)

        z = griddata( (x,y),z,(X,Y), fill_value=fill, method=method)  
        x = xi
        y = yi

    return x, y, z