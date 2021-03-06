import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mpldates
# import seaborn as sns
# import numpy as np


def setgrid(ax, major=True, minor=False):
    """ Given an axis object, it sets the grids on """
    if major or minor:
        ax.grid(True)

    if major:
        ax.grid(b=True, which='major', color='#999999', linestyle='-', linewidth=1)

    if minor:
        ax.minorticks_on()
        ax.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.7, linewidth=0.5)



def lineplot(p, ax=None, legend="br", figsize=(10,6), timeplot=False, dateformat="%Y-%m-%d %H%M", color=None, sharex=True, sharey=True):
    # title="Timeline Plot",
    majorgrid=True
    minorgrid=False
    # plot into existing axis
    if ax is None:
        is_new_fig = True
        fig, ax = plt.subplots(figsize=figsize)
        fig.suptitle(p.title, fontsize=15)
    else:
        is_new_fig = False
        fig = ax.get_figure()
        if not sharey:
            ax = ax.twinx()

    # plot it
    color = color if p.color is None else p.color
    ax.plot(p.x, p.y, color=color,  label=p.name, linewidth=p.width, alpha=p.alpha)
    if is_new_fig:
        plt.xticks(rotation=-30, ha="left")
        ax.set_xlabel(p.xlabel)
        ax.set_ylabel(p.ylabel)
        setgrid(ax, major=majorgrid, minor=minorgrid)
        if timeplot:
            ax.xaxis.set_major_formatter(mpldates.DateFormatter(dateformat))
            ax.xaxis.set_minor_formatter(mpldates.DateFormatter(dateformat))
    if legend is not None:
        add_legend(ax, position=legend)

    return fig, ax


def step_plot(p, ax=None, legend="br", figsize=(10,6), timeplot=False, dateformat="%Y-%m-%d %H%M", color=None, sharex=True, sharey=True):
    # TODO: This shares the majority of code with lineplot, share this code in
    #       a generic function
    # title="Timeline Plot",
    majorgrid=True
    minorgrid=False
    # plot into existing axis
    if ax is None:
        is_new_fig = True
        fig, ax = plt.subplots(figsize=figsize)
        fig.suptitle(p.title, fontsize=15)
    else:
        is_new_fig = False
        fig = ax.get_figure()
        if not sharey:
            ax = ax.twinx()

    # plot it
    color = color if p.color is None else p.color
    ax.step(p.x, p.y, color=color,  label=p.name, linewidth=p.width, alpha=p.alpha, where="post")
    if is_new_fig:
        plt.xticks(rotation=-30, ha="left")
        ax.set_xlabel(p.xlabel)
        ax.set_ylabel(p.ylabel)
        setgrid(ax, major=majorgrid, minor=minorgrid)
        if timeplot:
            ax.xaxis.set_major_formatter(mpldates.DateFormatter(dateformat))
            ax.xaxis.set_minor_formatter(mpldates.DateFormatter(dateformat))
    if legend is not None:
        add_legend(ax, position=legend)

    return fig, ax


#def scatterplot(x, y, ax=None, color=None, alpha=None, size=None, labels=None, title="Scatterplot", figsize=(10,6), cmap=None):
def scatterplot(p, ax=None, legend="br", figsize=(10,6), timeplot=False, dateformat="%Y-%m-%d %H%M", color=None, sharex=True, sharey=True):
    """
        labels: (None or array-like) label for each data point

    """
    # TODO: This shares the majority of code with lineplot, share this code in
    #       a generic function
    # title="Timeline Plot",
    majorgrid=True
    minorgrid=False
    # plot into existing axis
    if ax is None:
        is_new_fig = True
        fig, ax = plt.subplots(figsize=figsize)
        fig.suptitle(p.title, fontsize=15)
    else:
        is_new_fig = False
        fig = ax.get_figure()
        if not sharey:
            ax = ax.twinx()

    # plot it
    # TODO: boolean color coded colors
    color = color if p.color is None else p.color
    size = [sz*10 for sz in p.size] if isinstance(p.size, (list, tuple)) else p.size
    size = size*10 if isinstance(size, (int, float, np.ndarray, pd.Series)) else size
    ax.scatter(x=p.x, y=p.y, c=color, alpha=p.alpha, s=size, label=p.name) #cmap=cmap

    if is_new_fig:
        plt.xticks(rotation=-30, ha="left")
        ax.set_xlabel(p.xlabel)
        ax.set_ylabel(p.ylabel)
        setgrid(ax, major=majorgrid, minor=minorgrid)
        if timeplot:
            ax.xaxis.set_major_formatter(mpldates.DateFormatter(dateformat))
            ax.xaxis.set_minor_formatter(mpldates.DateFormatter(dateformat))
    if legend is not None:
        add_legend(ax, position=legend)

    # POINT LABELS
    if p.labels is not None:
        for xx, yy, label in zip(p.x, p.y, p.labels):
            plt.annotate(label, xy=(xx, yy), xytext=(7, 0),
                         textcoords='offset points',
                         ha='left', va='center')
    return fig, ax

def get_legend_labels_from_fig(fig):
    axes = fig.axes
    lines =  [line for axx in axes for line in axx.lines]
    lines += [line for axx in axes for line in axx.collections]
    labs = [line.get_label() for line in lines]
    return lines, labs

def add_legend(ax, position="br"):
    fig = ax.get_figure()
    legendmap = {"br": "lower right", "tr": "upper right"}
    lines, labs = get_legend_labels_from_fig(fig)
    ax.legend(lines, labs, loc=legendmap.get(position, "lower_right"), title="", frameon=False,  fontsize=10)




# def line_plot(x, y=None, start=None, end=None, ax=None, title="Plot", majorgrid=True, minorgrid=False, sharey=False, name="", color="#307EC7", width=1):
#     """
#     p: graphotti plot object
#     # sharey: share the yaxis (for when overlaying)
#     """
#     n = len(x)
#
#     # Separate the x and y axis data.
#     # If `y` is None, then assume that `x` contains the actual values, and
#     # that the indices are implicitly encoded as either the indices of a
#     # pandas series, or the array-like order of the elements.
#     if y is None:
#         y = x
#         if is instance(x, (pd.Series)):
#             x = x.index
#         else:
#             x = list(range(n))
#
#     # Plot into existing axis, otherwise create a new figure
#     if ax is None:
#         is_new_fig = True
#         fig, ax = plt.subplots(figsize=(10, 6))
#         fig.suptitle(title, fontsize=15)
#     else:
#         is_new_fig = False
#         fig = ax.get_figure()
#         if sharey:
#             ax = ax.twinx()
#
#     # Take a slice of the data
#     x_slice = x[start:end]
#
#     # Plot the data if it exists
#     if len(x_slice) == 0:
#         print("NOTE: No data in this specified start-end slice")
#     else:
#         ax.plot(x_slice, color=color,  label=name, linewidth=width)
#         if is_new_fig:
#             plt.xticks(rotation=-30, ha="left")
#             ax.set_xlabel("x")
#             ax.set_ylabel("val")
#             setgrid(ax, major=majorgrid, minor=minorgrid)
#             # ax.xaxis.set_major_formatter(mpldates.DateFormatter(dateformat))
#             # ax.xaxis.set_minor_formatter(mpldates.DateFormatter(dateformat))
#         ax.legend(loc="lower right", title="", frameon=False,  fontsize=8)
#     return fig, ax


# def timeline_plot(x, startdate=None, enddate=None, dateformat="%Y-%m-%d %H%M", ax=None, title="Timeline Plot", majorgrid=True, minorgrid=False, independent=False, name="", color="#307EC7", width=1):
#     # plot into existing axis
#     if ax is None:
#         is_new_fig = True
#         fig, ax = plt.subplots(figsize=(10, 6))
#         fig.suptitle(title, fontsize=15)
#     else:
#         is_new_fig = False
#         fig = ax.get_figure()
#         if independent:
#             ax = ax.twinx()
#
#     # take a time slice of the data
#     x_slice = x[startdate:enddate]
#     if len(x_slice) == 0:
#         print("NOTE: No data in this specified time slice")
#     else:
#         # plot the data if it exists
#         ax.plot(x_slice, color=color,  label=name, linewidth=width)
#         if is_new_fig:
#             plt.xticks(rotation=-30, ha="left")
#             ax.set_xlabel("date")
#             ax.set_ylabel("val")
#             setgrid(ax, major=majorgrid, minor=minorgrid)
#             ax.xaxis.set_major_formatter(mpldates.DateFormatter(dateformat))
#             ax.xaxis.set_minor_formatter(mpldates.DateFormatter(dateformat))
#         ax.legend(loc="lower right", title="", frameon=False,  fontsize=8)
#     return fig, ax
#
#
# def compare_timelines(df, columns, startdate=None, enddate=None, title="plot"):
#     colors = ["red", "blue", "green", "purple", "yellow", "pink", "gray", "orange"]
#     for i, column in enumerate(columns):
#         if i == 0:
#             fig, ax = timeline_plot(df[startdate:enddate][column], color=colors[i], name=column, title=title)
#         else:
#             fig, ax = timeline_plot(df[startdate:enddate][column], color=colors[i], ax=ax, name=column)
#     return fig, ax
#
#
# def compare_timelines_sep(series, names=None, startdate=None, enddate=None, title="plot", sharey=True, width=2):
#     """ FOr where the timeseries are in sepearate dataframes/series, with
#         potentially different time indices.
#         names: (list) lables to assign to each plot
#         series: a list of pandas series to use
#         sharey: share y axis?
#                 TODO: NOT IMPLEMENTED YET
#     """
#     n = len(series)
#     colors = ["red", "blue", "green", "purple", "yellow", "pink", "gray", "orange"]
#     names = names if names is not None else [i for i in range(n)]
#     if isinstance(width, (int, float)):
#         width = [width for i in range(n)]
#
#     for i, x in enumerate(series):
#         if i == 0:
#             fig, ax = timeline_plot(x[startdate:enddate], color=colors[i], name=names[i], title=title, width=width[i])
#         else:
#             fig, ax = timeline_plot(x[startdate:enddate], color=colors[i], ax=ax, name=names[i], title=title, width=width[i])
#     return fig, ax
#
#
# def compare_lines_sep(series, names=None, startdate=None, enddate=None, title="plot", sharey=True, width=2):
#     """ FOr where the pandas series are in sepearate dataframes/series, with
#         potentially different indices.
#         names: (list) lables to assign to each plot
#         series: a list of pandas series to use
#         sharey: share y axis?
#                 TODO: NOT IMPLEMENTED YET
#     """
#     n = len(series)
#     colors = ["red", "blue", "green", "purple", "yellow", "pink", "gray", "orange"]
#     names = names if names is not None else [i for i in range(n)]
#     if isinstance(width, (int, float)):
#         width = [width for i in range(n)]
#
#     for i, x in enumerate(series):
#         if i == 0:
#             fig, ax = line_plot(x[startdate:enddate], color=colors[i], name=names[i], title=title, width=width[i])
#         else:
#             fig, ax = line_plot(x[startdate:enddate], color=colors[i], ax=ax, name=names[i], title=title, width=width[i])
#     return fig, ax
#
#
# def scatterplot(x, y, ax=None, color=None, alpha=None, size=None, labels=None, title="Scatterplot", figsize=(10,6), cmap=None):
#     """
#         labels: (None or array-like) label for each data point
#
#     """
#     if ax is None:
#         fig, ax = plt.subplots(figsize=figsize)
#         fig.suptitle(title, fontsize=15)
#     else:
#         fig = ax.get_figure()
#     ax.scatter(x=x, y=y, c=color, alpha=alpha, s=size, cmap=cmap)
#
#     # LABEL - each of the points
#     if labels is not None:
#         for xx, yy, label in zip(x, y, labels):
#             plt.annotate(label, xy=(xx, yy), xytext=(7, 0),
#                          textcoords='offset points',
#                          ha='left', va='center')
#     return fig, ax
#
#
#
# def plot_histogram(x, bins=20, title="distribution", logscale=False):
#     fig, ax = plt.subplots(figsize=(10, 6))
#     fig.suptitle(title, fontsize=15)
#     ax.hist(x, color="#307EC7",  label="", bins=bins)
#     ax.set_xlabel("x")
#     ax.set_ylabel("y")
#     if logscale:
#         ax.set_yscale('log')
#     return fig, ax


# def plotcurve(f, start, end, title=""):
#     x = np.linspace(start, end, num=100)
#     fig, ax = plt.subplots(figsize=(6, 4))
#     fig.suptitle(title, fontsize=15)
#     ax.plot(x, f(x), color="#307EC7",  label="")
#     ax.set_xlabel("x")
#     ax.set_ylabel("y")
#     plt.show()
