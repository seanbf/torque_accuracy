import plotly.graph_objects as go
import streamlit as st
def demanded_plot(data, test_dict):

    test_plot = go.Figure()
    test_plot.add_trace	(go.Scattergl (  
                                x       		= data[test_dict["Speed"]],
                                y       		= data[test_dict["Torque Demanded"]],
                                name 			= "Demanded Torque : Speed",
                                mode            = 'markers',

                                        )
                        )
    test_plot.update_layout    (   
                                title       = 'Demanded Test Points',
                                xaxis_title = test_dict["Speed"],
                                yaxis_title = test_dict["Torque Demanded"]
                                )
    return test_plot

def transient_removal_plot(transient_sample, Step_index, Stop_index, df, test_dict):
    transient_plot = go.Figure()

    transient_plot.add_trace(go.Scatter (  
                                        x       = transient_sample.index.values, 
                                        y       = transient_sample[test_dict["Torque Demanded"]], 
                                        name    = "Demanded Torque (Nm)",
                                        hovertemplate = '%{y:.2f} Nm'
                            )           )

    transient_plot.add_trace(go.Scatter (  
                                        x       = transient_sample.index.values, 
                                        y       = transient_sample[test_dict["Torque Estimated"]],
                                        name    = "Estimated Torque (Nm)",
                                        hovertemplate = '%{y:.2f} Nm'
                            )           )

    transient_plot.add_trace(go.Scatter (  
                                        x       = transient_sample.index.values, 
                                        y       = transient_sample[test_dict["Torque Measured"]], 
                                        name    = "Measured Torque (Nm)",
                                        hovertemplate = '%{y:.2f} Nm'
                            )           )

    transient_plot.update_layout    (   
                                    title       = 'Transient Removal Example',
                                    xaxis_title = 'Sample (N)',
                                    yaxis_title = 'Torque (Nm)'
                                    )
    transient_plot.add_annotation   (
                                    x           = Step_index[test_dict["Sample"]],
                                    y           = df[test_dict["Torque Demanded"]][Step_index[test_dict["Sample"]]],
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
                                    y           = df[test_dict["Torque Demanded"]][Stop_index[test_dict["Sample"]]],
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
                                    hovermode="x unified",
                                    template="plotly_white"
                                    )
    return transient_plot