import numpy as np

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


def lineplot(p, ax=None, figsize=(10,6)):
    """
    p: graphotti plot object
    # sharey: share the yaxis (for when overlaying)
    """
    n = len(p.x)

    # Plot into existing axis, otherwise create a new figure
    if ax is None:
        is_new_fig = True
        fig, ax = plt.subplots(figsize=figsize)
        fig.suptitle(p.title, fontsize=15)
    else:
        is_new_fig = False
        fig = ax.get_figure()
        if ~p.share:
            ax = ax.twinx() # plot that shares only the x axis, but not y

    # Plot it!
    ax.plot(p.x, p.y, color=p.color,  label=p.name, linewidth=p.width)
    if is_new_fig:
        plt.xticks(rotation=-30, ha="left")
        ax.set_xlabel("TODO")
        ax.set_ylabel("TODO")
        # ax.set_xlabel(p.ax.xlabel)
        # ax.set_ylabel(p.ax.ylabel)
        setgrid(ax, major=p.majorgrid, minor=p.minorgrid)
        # ax.xaxis.set_major_formatter(mpldates.DateFormatter(dateformat))
        # ax.xaxis.set_minor_formatter(mpldates.DateFormatter(dateformat))
    ax.legend(loc="lower right", title="", frameon=False,  fontsize=8)
    return fig, ax


