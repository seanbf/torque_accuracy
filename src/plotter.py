import plotly.graph_objects as go
import streamlit as st

def demanded_plot(data, speed_signal, torque_demanded_signal):

    test_plot = go.Figure()
    test_plot.add_trace	(go.Scattergl (  
                                x       		= data[speed_signal],
                                y       		= data[torque_demanded_signal],
                                name 			= "Torque Demanded [Nm] : Speed [rpm] Rounded",
                                mode            = 'markers',

                                        )
                        )
    test_plot.update_layout    (   
                                title       = 'Demanded Test Points',
                                xaxis_title = speed_signal,
                                yaxis_title = torque_demanded_signal
                                )
    return test_plot

def transient_removal_plot(transient_sample, Step_index, Stop_index, df, test_dict):
    transient_plot = go.Figure()

    transient_plot.add_trace(go.Scatter (  
                                        x       = transient_sample.index.values, 
                                        y       = transient_sample["Torque Demanded [Nm]"], 
                                        name    = "Demanded Torque [Nm]",
                                        hovertemplate = '%{y:.2f} Nm'
                            )           )

    transient_plot.add_trace(go.Scatter (  
                                        x       = transient_sample.index.values, 
                                        y       = transient_sample["Torque Estimated [Nm]"],
                                        name    = "Estimated Torque [Nm]",
                                        hovertemplate = '%{y:.2f} Nm'
                            )           )

    transient_plot.add_trace(go.Scatter (  
                                        x       = transient_sample.index.values, 
                                        y       = transient_sample["Torque Measured [Nm]"], 
                                        name    = "Measured Torque [Nm]",
                                        hovertemplate = '%{y:.2f} Nm'
                            )           )

    transient_plot.update_layout    (   
                                    title       = 'Transient Removal Example',
                                    xaxis_title = 'Sample [N]',
                                    yaxis_title = 'Torque [Nm]'
                                    )
    transient_plot.add_annotation   (
                                    x           = Step_index[test_dict["Sample"]],
                                    y           = df["Torque Demanded [Nm]"][Step_index[test_dict["Sample"]]],
                                    xref        = "x",
                                    yref        = "y",
                                    text        = "Start of removal",
                                    showarrow   = True,
                                    font        = dict   (
                                                        family  = "Arial, monospace",
                                                        size    = 14,
                                                        color   = "#ffffff"
                                                        ),
                                    align       = "center",
                                    arrowhead   = 2,
                                    arrowsize   = 1,
                                    arrowwidth  = 2,
                                    arrowcolor  = "#636363",
                                    bordercolor = "#c7c7c7",
                                    borderwidth = 2,
                                    borderpad   = 4,
                                    bgcolor     = "#ff7f0e",
                                    )

    transient_plot.add_annotation   (
                                    x           = Stop_index[test_dict["Sample"]],
                                    y           = df["Torque Demanded [Nm]"][Stop_index[test_dict["Sample"]]],
                                    xref        = "x",
                                    yref        = "y",
                                    text        = "End of removal",
                                    showarrow   = True,
                                    font        = dict   (
                                                        family  = "Arial, monospace",
                                                        size    = 14,
                                                        color   = "#ffffff"
                                                        ),
                                    align       = "center",
                                    arrowhead   = 2,
                                    arrowsize   = 1,
                                    arrowwidth  = 2,
                                    arrowcolor  = "#636363",
                                    bordercolor = "#c7c7c7",
                                    borderwidth = 2,
                                    borderpad   = 4,
                                    bgcolor     = "#ff7f0e",
                                    )

    transient_plot.update_layout    (
                                    hovermode="x unified"
                                    )
    return transient_plot