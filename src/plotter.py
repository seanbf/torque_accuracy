import plotly.graph_objects as go
import streamlit as st

def demanded_plot(data, t_demanded, speed_round):

    test_plot = go.Figure()
    test_plot.add_trace	(go.Scattergl (  
                                x       		= data[speed_round],
                                y       		= data[t_demanded],
                                name 			= t_demanded + " : " + speed_round,
                                mode            = 'markers',

                                        )
                        )
    test_plot.update_layout    (   
                                title       = 'Demanded Test Points',
                                xaxis_title = speed_round,
                                yaxis_title = t_demanded
                                )
    return test_plot

def transient_removal_plot(transient_sample, Step_index, Stop_index, df, test_dict, t_demanded, t_estimated, t_measured):
    transient_plot = go.Figure()

    transient_plot.add_trace(go.Scatter (  
                                        x       = transient_sample.index.values, 
                                        y       = transient_sample[t_demanded], 
                                        name    = t_demanded,
                                        hovertemplate = '%{y:.2f} Nm'
                            )           )

    transient_plot.add_trace(go.Scatter (  
                                        x       = transient_sample.index.values, 
                                        y       = transient_sample[t_estimated],
                                        name    = t_estimated,
                                        hovertemplate = '%{y:.2f} Nm'
                            )           )

    transient_plot.add_trace(go.Scatter (  
                                        x       = transient_sample.index.values, 
                                        y       = transient_sample[t_measured], 
                                        name    = t_measured,
                                        hovertemplate = '%{y:.2f} Nm'
                            )           )

    transient_plot.update_layout    (   
                                    title       = 'Transient Removal Example',
                                    xaxis_title = 'Sample [N]',
                                    yaxis_title = 'Torque [Nm]'
                                    )
    transient_plot.add_annotation   (
                                    x           = Step_index[test_dict["Sample"]],
                                    y           = df[t_demanded][Step_index[test_dict["Sample"]]],
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
                                    y           = df[t_demanded][Stop_index[test_dict["Sample"]]],
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

@st.cache
def plot_3D(x_string, y_string, z_string, x, y, z, chart_type, color_palette, overlay, overlay_alpha, overlay_color):
    with st.spinner("Generating 3D Plot"):

        plot_3D = go.Figure()

        if chart_type == 'Contour':
            plot_3D.add_trace(go.Contour    (
                                            z           = z,
                                            x           = x, 
                                            y           = y,
                                            colorscale  = color_palette,
                                            hovertemplate = x_string + ': %{x:.2f}' + 
                                                            '<br>' + y_string + ': %{y:.2f}</br>' +
                                                            z_string + ': %{z:.2f}',

                                            contours    = dict  (
                                                                coloring    ='heatmap',
                                                                showlabels  = True,
                                                                labelfont   = dict  (
                                                                                    size = 10,
                                                                                    color = 'white',
                                                                                    )
                                                                ), 

                                            colorbar    = dict  (
                                                                title       = z_string,
                                                                titleside   = 'right',
                                                                titlefont   = dict  (
                                                                                    size=12,
                                                                                    family='Arial, sans'
                                                                                    )
                                                                )
                                    )       )

        if chart_type == 'Surface':
                        plot_3D.add_trace(go.Surface  (
                                            z           = z,
                                            x           = x, 
                                            y           = y,

                                            contours =  {
                                                        "x": {"show": True},
                                                        "z": {"show": True}
                                                        },

                                            colorscale  = color_palette,
                                     
                            
                                            hovertemplate = x_string + ': %{x:.2f}' + 
                                                            '<br>' + y_string + ': %{y:.2f}</br>' +
                                                            z_string + ': %{z:.2f}',

                                            colorbar    = dict  (
                                                                title       = z_string,
                                                                titleside   = 'right',
                                                                titlefont   = dict  (
                                                                                    size=12,
                                                                                    family='Arial, sans'
                                                                                    )
                                                                )
                                            )           )
        if chart_type == 'Heatmap':
                        plot_3D.add_trace(go.Heatmap  (
                                            z           = z,
                                            x           = x, 
                                            y           = y,

                                            colorscale  = color_palette,

                                            hovertemplate = x_string + ': %{x:.2f}' + 
                                                            '<br>' + y_string + ': %{y:.2f}</br>' +
                                                            z_string + ': %{z:.2f}',

                                            colorbar    = dict  (
                                                                title       = z_string,
                                                                titleside   = 'right',
                                                                titlefont   = dict  (
                                                                                    size=12,
                                                                                    family='Arial, sans'
                                                                                    )
                                                                )
                                            )           )

        if chart_type == '3D Scatter':
            plot_3D.add_trace(go.Scatter3d  (
                                            z           = z,
                                            x           = x, 
                                            y           = y,
                                            mode        = 'markers',
                                            marker      = dict(
                                                        color       = z,
                                                        colorscale  = color_palette,
                                                        opacity     = 0.7,
                                                        colorbar    = dict  (
                                                                            title       = z_string,
                                                                            titleside   = 'right',
                                                                            titlefont   = dict  (
                                                                                                size=12,
                                                                                                family='Arial, sans'
                                                                                                )
                                                                            )  
                                                                ),

                                            hovertemplate = x_string + ': %{x:.2f}' + 
                                                            '<br>' + y_string + ': %{y:.2f}</br>' +
                                                            z_string + ': %{z:.2f}',

          

                                            )           )
        
        if (overlay == True) and (chart_type != "3D Scatter" or "Surface") :
            plot_3D.add_trace	(go.Scatter (  
                            x       		= x,
                            y       		= y,
                            name 			= "X: "  + x_string + "Y: "  + y_string,
                            mode            = 'markers',
                            opacity         = overlay_alpha,
                            marker          = dict  (
                                                    color   = overlay_color, 
                                                    symbol  = "circle",
                                                    line  =dict (
                                                                    color='MediumPurple',
                                                                    width=2
                                                                )
                                                    ),
                            ),     
                )
        label_dict = dict()
        if chart_type == "3D Scatter" or "Surface":
        
            label_dict["autosize"] = True
            label_dict["title"]    = z_string
            label_dict["xaxis"]    = dict(title=x_string)
            label_dict["yaxis"]    = dict(title=y_string)
        else:
            label_dict["autosize"] = True,
            label_dict["title"]    = z_string
            label_dict["xaxis"]    = dict(title=x_string)
            label_dict["yaxis"]    = dict(title=y_string)
                       
        plot_3D.update_layout(label_dict)

        return plot_3D