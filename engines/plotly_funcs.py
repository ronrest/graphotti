import numpy as np
import pandas as pd

from plotly.offline import plot, iplot, init_notebook_mode
import plotly.graph_objs as go
# init_notebook_mode(connected=True)


CATEGORICAL_COLORS = ["blue", "orange", "green", "purple", "red", "pink", "grey"]

def create_figure(traces, title, xlabel="x", ylabel="y", sharey=None):
    n = len(traces)
    last_shared_y_axis = 1
    sharey = [True for _ in range(n)] if sharey is None else sharey
    layout = go.Layout(
        title=title,
        hovermode="closest",
        xaxis=dict(
            title=xlabel,
            ),
        )
    for i in range(len(traces)):
        if not sharey[i]:
            last_shared_y_axis = i+1
            ykey_suffix = "{}".format(last_shared_y_axis) if last_shared_y_axis > 1 else ""
            layout["yaxis"+ykey_suffix] = dict(
                                            # title="y{}".format(i),
                                            overlaying="y" if (i > 0) else None,
                                            )
        else:
            ykey_suffix = "{}".format(last_shared_y_axis) if last_shared_y_axis > 1 else ""
        traces[i]["yaxis"] = "y"+ykey_suffix


    fig = go.Figure(data=traces, layout=layout)
    return fig

def lineplot(p, color=None):
    trace = go.Scatter(x=p.x, y=p.y, text=p.labels,
                        name=p.name,
                        mode="lines",
                        marker=dict(color=p.color,
                                    size=p.size,
                                    opacity=p.alpha)
                        )
    return trace

def scatter(p, color=None):
    trace = go.Scatter(x=p.x, y=p.y, text=p.labels,
                        name=p.name,
                        mode="markers",
                        marker=dict(color=p.color,
                                    size=p.size,
                                    opacity=p.alpha)
                        )
    return trace

# def compare_lines_sep(series, names=None, startdate=None, enddate=None, title="plot", sharey=True, width=1):
#     """ Plotly implementation of compare lines sep, using same api as the mpl version
#         FOr where the timeseries are in sepearate dataframes/series, with
#         potentially different time indices.
#         names: (list) lables to assign to each plot
#         series: a list of pandas series to use
#         sharey: share y axis?
#                 TODO: NOT IMPLEMENTED YET
#     """
#     # colors = ["red", "blue", "green", "purple", "yellow", "pink", "gray", "orange"]
#     # names = names if names is not None else [i for i in range(len(series))]
#     # for i, x in enumerate(series):
#     #     if i == 0:
#     #         fig, ax = timeline_plot(x[startdate:enddate], color=colors[i], name=names[i], title=title)
#     #     else:
#     #         fig, ax = timeline_plot(x[startdate:enddate], color=colors[i], ax=ax, name=names[i], title=title)
#     # return fig, ax
#
#     fig = plotly_scatters(xx=[s.index for s in series],
#                     yy=series,
#                     size=3,
#                     width=width,
#                     color=None,
#                     opacity=0.5,
#                     labels=None,
#                     title=title, names=names,
#                     xlabel="time", ylabel="y",
#                     show=True,
#                     category_colors=None, marker_mode="lines+markers")
#     return fig, None



def plotly_scatter(x,y, size=10, color="blue", opacity=0.5, labels=None, title="Scatter Plot", name=None, xlabel="x", ylabel="y", show=True, category_colors=None, marker_mode="markers"):
    """ category_colors: array-like object that contains some kind of category label for each datapoint in x.
                         it is used to assign a different color to each category
        marker_mode: one of markers, lines, lines+markers
    """
    if category_colors is not None:
        color = [CATEGORICAL_COLORS[i] for i in pd.Series(category_colors).astype('category').cat.codes]

    trace1 = go.Scatter(x=x, y=y, text=labels,
                        name=name,
                        mode=marker_mode,
                        marker=dict(color=color,
                                    size=size,
                                    opacity=opacity)
                        )
    data = [trace1]
    layout = dict(
        title=title,
        hovermode="closest",
        xaxis=dict(
            title=xlabel,
        ),
        yaxis=dict(
            title=ylabel,
        )
        )

    fig = go.Figure(data=data, layout=layout)
    if show:
        iplot(fig)
    return fig



# def plotly_scatters(xx, yy, size=10, width=1, color=None, opacity=0.5, labels=None, title="Scatter Plot", names=None, xlabel="x", ylabel="y", show=True, category_colors=None, marker_mode="markers"):
#     """ category_colors: array-like object that contains some kind of category label for each datapoint in x.
#                          it is used to assign a different color to each category
#         marker_mode: one of markers, lines, lines+markers
#         width: line width
#         size: size pf the points
#     """
#     n = range(len(yy))
#     if category_colors is not None:
#         color = [CATEGORICAL_COLORS[i] for i in pd.Series(category_colors).astype('category').cat.codes]
#     if names is None:
#         names = ["plot {}".format(i) for i in range(len(yy))]
#     if isinstance(size, (int, float)):
#         size  = [size for _ in n]
#     if isinstance(width, (int, float)):
#         width = [width for i in range(n)]
#
#     data = []
#     if color is None:
#         color = CATEGORICAL_COLORS
#
#     for i in range(len(yy)):
#         trace = go.Scatter(x=xx[i], y=yy[i], text=labels,
#                             name=names[i],
#                             mode=marker_mode,
#                             marker=dict(color=color[i],
#                                         size=size[i],
#                                         opacity=opacity,
#                                         ),
#                             line = dict(color = color[i],
#                                         width = width[i],
#                                         ),
#                             )
#         data.append(trace)
#     layout = dict(
#         title=title,
#         hovermode="closest",
#         xaxis=dict(
#             title=xlabel,
#         ),
#         yaxis=dict(
#             title=ylabel,
#         )
#         )
#
#     fig = go.Figure(data=data, layout=layout)
#     if show:
#         iplot(fig)
#     return fig
# #
# def plotly_lineplot(x, y=None, size=10, color=None, opacity=0.5, labels=None, title="Plot", name=None, xlabel="x", ylabel="y", show=True, ylog=False):
#     """
#         ylog: (bool) should y axis be log scale?
#     """
#     if y is None:
#         y = x
#         x = list(range(len(x)))
#
#     trace1 = go.Scatter(x=x, y=y, text=labels,
#                         name=name,
#                         mode='lines',
#                         marker=dict(color=color,
#                                     size=size,
#                                     opacity=opacity)
#                         )
#     data = [trace1]
#     layout = dict(
#         title=title,
#         hovermode="closest",
#         xaxis=dict(
#             title=xlabel,
#         ),
#         yaxis=dict(
#             type = "log" if ylog else "linear",
#             title=ylabel,
#         )
#         )
#     fig = go.Figure(data=data, layout=layout)
#     if show:
#         iplot(fig)
#     return fig
#
#
# def plotly_heatmap(z, x=None, y=None, title="Plot", name=None, xlabel="x", ylabel="y", zmin=None, zmax=None, show=True):
#     trace = go.Heatmap(z=z, x=x, y=y,
#                        name=name,
#                        zmin=zmin, zmax=zmax)
#     layout = dict(
#         title=title,
#         hovermode="closest",
#         xaxis=dict(
#             title=xlabel,
#         ),
#         yaxis=dict(
#             title=ylabel,
#         ),
#         )
#
#     data=[trace]
#     fig = go.Figure(data=data, layout=layout)
#     if show:
#         iplot(fig)
#     return fig
#
#
# # TODO: this is an OLD, primitive version of the function. FInd, or create one
# #       that is more in line with my current pipeline
# def plotly_timeseries(x, label="line1"):
#     """ Given a pandas timeseries object, it plots a plotply plot of it """
#     trace1 = go.Scatter(
#     x=x.index.strftime("%Y-%m-%d"),
#     y=list(x),
#     name = label, # Style name/legend entry with html tags
#     connectgaps=True
#     )
#     data = [trace1]
#     fig = dict(data=data)
#     iplot(fig)
