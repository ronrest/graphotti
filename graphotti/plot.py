# TODO: allow addition of more than 2 items
# TODO: overlload math operators for PlotGroup as well
# TODO: allow addition of PlotGroups with ProtoPlot objects
# TODO: allow addition PlotGroups

# TODO: i think that the `share` property might be better stored in the PlotGroup
#       object rather than the ProtoPlot object. This will allow for the individual
#       plots to be updatable, and not having to do new copies of the ProtoPlot
#       objects when set to share=False

from functools import reduce
import operator

import pandas as pd
from . engines import enginemap
import copy

DEFAULT_ENGINE = "mpl"


def set_default_engine(engine):
    global DEFAULT_ENGINE
    DEFAULT_ENGINE = engine


class Ax(object):
    def __init__(self):
        self.xmin = None
        self.ymin = None
        self.zmin = None

        self.xmax = None
        self.ymax = None
        self.zmax = None

        # the following are superceded b xrot, yrot, zrot
        # self.xangle = 0
        # self.yangle = 0
        # self.zangle = 0


class ProtoPlot(object):
    # TODO: Implement slicing operators.
    #        p1[start: end]
    #
    # TODO: Implement mathematical arithemtic operators for combining plots
    #       p1+p2+p3

    def __init__(self, x, y=None, z=None,
                color=None, alpha=1.0,
                size=1, width=1,
                labels=None,
                title="plot", name="plot",
                xlabel="x", ylabel="y", zlabel="z",
                scalex="linear", scaley="linear", scalez="linear",
                legend="br",
                ptype="scatter",
                start=None, end=None
                ):
        self.x = x
        self.y = y
        self.z = z
        self.labels = labels
        self.legend = legend

        self.start = start
        self.end = end

        self.scalex = scalex
        self.scaley = scaley
        self.scalez = scalez

        self.xlabel = xlabel
        self.ylabel = ylabel
        self.zlabel = zlabel

        self.xrot = 0
        self.yrot = 0
        self.zrot = 0

        self.color = color
        self.alpha = alpha
        self.size = size
        self.width = width
        self.points = False # whether to draw points or not

        self.title = title
        self.name = name
        self.ax = Ax()

        self.majorgrid = True
        self.minorgrid = True

        self.engine = None
        self.type = ptype # plot type
        # self.share = True

    def compile(self, engine=None, title=None, showlegend=True):
        # overrride plot title
        if title is not None:
            self.title = title
        self.showlegend = showlegend

        if engine is None:
            engine = self.get_engine()
        return enginemap[engine].compile(self)

    def get_engine(self):
        return DEFAULT_ENGINE if self.engine is None else self.engine

    def plot(self, engine=None, file=None, title=None, showlegend=True):
        # overrride plot title
        if title is not None:
            self.title = title
        self.showlegend = showlegend

        if engine is None:
            engine = self.get_engine()
        enginemap[engine].plot(self, file=file)


    def copy(self):
        return copy.copy(self)

    def __add__(self, other):
        return PlotGroup([self, other], type="overlay", engine=self.engine, sharey=[True, True], legend=self.legend)

    def __sub__(self, other):
        return PlotGroup([self, other], type="overlay", engine=self.engine, sharey=[True, False], legend=self.legend)

    def __truediv__(self, other):
        return PlotGrid([self, other], type="vertical", engine=self.engine, sharey=False, sharex=True, legend=self.legend)

    def __floordiv__(self, other):
        return PlotGrid([self, other], type="vertical", engine=self.engine, sharey=False, sharex=False, legend=self.legend)


    # def __neg__(self):
    #     x = self.copy()
    #     x.share = False
    #     return x

    def __getitem__(self, sliced):
        new = self.copy()

        # OLD SLICING METHOD
        # new.x = new.x[sliced]
        # new.y = new.y[sliced]
        # new.z = new.z if new.z is None else new.z[sliced]
        # new.labels = new.labels if new.labels is None else new.labels[sliced]

        # NEW SLICING METHOD
        df = pd.DataFrame(dict(y=new.y), index=new.x)
        if new.z is not None:
            df["z"] = new.z
        if new.labels is not None:
            df["labels"] = new.labels

        df = df[sliced]
        new.x = list(df.index)
        new.y  = df.y
        if new.z is not None:
            new.z = df.z
        if new.labels is not None:
            new.labels = df.labels

        return new


class PlotGroup(object):
    def __init__(self, items=[], engine="mpl", type="overlay", sharex=None, sharey=None, legend="br", title="Plot"):
        # TODO: implement the use of share being passed as parameter
        self.items = items
        self.sharex = [True for item in items]if sharex is None else sharex
        self.sharey = [True for item in items]if sharey is None else sharey
        self.scaley = [item.scaley for item in items]
        self.type = type
        self.engine = None
        #self.share = share
        self.legend = legend
        self.title = title

    def get_engine(self):
        return DEFAULT_ENGINE if self.engine is None else self.engine

    def compile(self, engine=None, title=None, showlegend=True):
        # overrride plot title
        if title is not None:
            self.title = title
        if engine is None:
            engine = self.get_engine()
        self.showlegend = showlegend
        return enginemap[engine].compilegroup(self)

    def plot(self, engine=None, file=None, title=None, showlegend=True):
        # overrride plot title
        if title is not None:
            self.title = title
        if engine is None:
            engine = self.get_engine()
        self.showlegend = showlegend
        return enginemap[engine].plotgroup(self, file=file)

    def copy(self):
        # TODO: see if this is a proper copy
        return copy.copy(self)

    def __add__(self, other):
        new = self.copy()
        if isinstance(other, PlotGroup):
            new.items.extend(other.items)
            new.sharex.extend(other.sharex)
            new.sharey.extend(other.sharey)
            new.scaley.extend(other.scaley)
        elif isinstance(other, ProtoPlot):
            new.items.append(other)
            new.sharex.append(True)
            new.sharey.append(True)
            new.scaley.append(other.scaley)
        return new

    def __sub__(self, other):
        # TODO: need to check if this is modifying the original `other` group,
        #       or applying share=False to a new object
        new = self.copy()
        if isinstance(other, PlotGroup):
            new.items.extend(other.items)
            new.sharex.extend(other.sharex)

            other_sharey = other.sharey.copy()
            other_sharey[0] = False
            new.sharey.extend(other_sharey)
            new.scaley.extend(other.scaley)
        elif isinstance(other, ProtoPlot):
            # TODO: this one is totally modifying the original object. Need to change this
            other_item = other
            # other.share = False
            new.items.append(other)
            new.sharex.append(True)
            new.sharey.append(False)
            new.scaley.append(other.scaley)
        return new

    def __getitem__(self, sliced):
        # BUG: it is modifying the data in place, it should return a copy
        #      leaving the original data unsliced
        new = self.copy()
        for i, item in enumerate(self.items):
            new.items[i] = item[sliced]
        return new



class PlotGrid(object):
    def __init__(self, items=[], engine="mpl", type="vertical", sharex=True, sharey=False, legend="br", title="Plot"):
        self.items = [[item] if not isinstance(item, list) else item for item in items]
        # self.items = items
        self.sharex = sharex
        self.sharey = sharey
        self.type = type
        self.engine = engine
        #self.share = share
        self.legend = legend
        self.title = title

    def compile(self, engine=None, title=None):
        # overrride plot title
        if title is not None:
            self.title = title
        if engine is None:
            engine = self.engine
        return enginemap[engine].compilegrid(self)

    def plot(self, engine=None, file=None, title=None):
        # overrride plot title
        if title is not None:
            self.title = title
        if engine is None:
            engine = self.engine
        return enginemap[engine].plotgrid(self, file=file)

    def copy(self):
        # TODO: see if this is a proper copy
        return copy.copy(self)

    def __div__(self, other):
        print("division on grid object")
    #     new = self.copy()
    #     if isinstance(other, PlotGroup):
    #         new.items.extend(other.items)
    #         new.sharex.extend(other.sharex)
    #         new.sharey.extend(other.sharey)
    #     elif isinstance(other, ProtoPlot):
    #         new.items.append(other)
    #         new.sharex.append(True)
    #         new.sharey.append(True)
    #     return new

    # def __sub__(self, other):
    #     # TODO: need to check if this is modifying the original `other` group,
    #     #       or applying share=False to a new object
    #     new = self.copy()
    #     if isinstance(other, PlotGroup):
    #         new.items.extend(other.items)
    #         new.sharex.extend(other.sharex)
    #
    #         other_sharey = other.sharey.copy()
    #         other_sharey[0] = False
    #         new.sharey.extend(other_sharey)
        #
        # elif isinstance(other, ProtoPlot):
        #     # TODO: this one is totally modifying the original object. Need to change this
        #     other_item = other
        #     # other.share = False
        #     new.items.append(other)
        #     new.sharex.append(True)
        #     new.sharey.append(False)
        # return new

    def __getitem__(self, sliced):
        # BUG: it is modifying the data in place, it should return a copy
        #      leaving the original data unsliced
        new = self.copy()
        for i, item in enumerate(self.items):
            new.items[i] = item[sliced]
        return new



# ##############################################################################
#                                        PLOT FUNCTIONS
# ##############################################################################
def lineplot(x, y=None,
    color=None, alpha=1.0, size=1, width=1,
    points=False,
    labels=None, title="plot", name="line",
    scalex="linear", scaley="linear",
    **kwargs
    ):
    """ Creates a lineplot object
    Args:
        points: (bool) should it also draw the points as markers?
    """
    n = len(x)
    if y is None:
        y = x
        if isinstance(y, pd.Series):
            x = list(y.index)
        else:
            x = list(range(n))

    obj = ProtoPlot(x=x, y=y,
                color=color, alpha=alpha,
                size=size, width=width,
                labels=labels,
                title=title, name=name,
                scalex=scalex, scaley=scaley,
                ptype="lineplot",
                **kwargs
                )

    obj.points = points
    return obj

# alias for lineplot
line = lineplot


def scatter(x, y=None,
    color=None, alpha=0.5, size=10, width=1,
    labels=None, title="plot", name="line",
    scalex="linear", scaley="linear",
    **kwargs
    ):
    """ Creates a lineplot object """
    n = len(x)
    if y is None:
        y = x
        if isinstance(y, pd.Series):
            x = list(y.index)
        else:
            x = list(range(n))

    return ProtoPlot(x=x, y=y,
                color=color, alpha=alpha,
                size=size, width=width,
                labels=labels,
                title=title, name=name,
                scalex=scalex, scaley=scaley,
                ptype="scatter",
                **kwargs
                )

def step(x, y=None,
    color=None, alpha=1.0, size=1, width=2,
    points=False,
    labels=None, title="plot", name="steps",
    scalex="linear", scaley="linear",
    **kwargs
    ):
    """ Creates a step plot object
    Args:
        points: (bool) should it also draw the points as markers?
    """
    n = len(x)
    if y is None:
        y = x
        if isinstance(y, pd.Series):
            x = list(y.index)
        else:
            x = list(range(n))

    obj = ProtoPlot(x=x, y=y,
                color=color, alpha=alpha,
                size=size, width=width,
                labels=labels,
                title=title, name=name,
                scalex=scalex, scaley=scaley,
                ptype="step",
                **kwargs
                )

    obj.points = points
    return obj



# ##############################################################################
#                           DATAFRAME PLOTS
# ##############################################################################
# Overriding the `sum()` function because for some reason the native one does
# not work properly from inside of this module.
#     It would throw an error about adding an integer to a ProtoPlot
#     object.
def sum(x):
    """ Iteratively add a list of items """
    return reduce(operator.__add__, x)

def subtract(x):
    """ Iteratively subtract a list of items, similarly to the sum() function """
    return reduce(operator.__sub__, x)


def dfplot(df, kind="line", sharey=True, **kwargs):
    """ Given a dataframe, it creates a group plot object, using the data
        from each of the columns. Can specify the plot kind, and
        whether to share y axis.

    Args:
        df:     (pandas dataframe)
        kind:   (str) one of "line", "step", "scatter"
        sharey: (bool) whether the plots should share the y axis
        **kwargs: aditional keyword arguments passed to the plot kind function
    """
    # Establish the kind of plot to use
    plotfuncs = dict(line=lineplot, step=step, scatter=scatter)
    assert kind in plotfuncs.keys(), "Only accepts the following plot kinds: {}".format(plotfunc.keys())
    plotfunc = plotfuncs[kind]

    # Group the columns together as plot objects
    group = [plotfunc(df[col], name=str(col)) for col in df.columns]
    if sharey:
        group = sum(group)
    else:
        group = subtract(group)
    return group
