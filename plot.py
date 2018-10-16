# TODO: allow addition of more than 2 items
# TODO: overlload math operators for PlotGroup as well
# TODO: allow addition of PlotGroups with ProtoPlot objects
# TODO: allow addition PlotGroups

# TODO: i think that the `share` property might be better stored in the PlotGroup
#       object rather than the ProtoPlot object. This will allow for the individual
#       plots to be updatable, and not having to do new copies of the ProtoPlot
#       objects when set to share=False

import pandas as pd
from . engines import enginemap
import copy

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
        self.scaley = scalez

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

        self.engine = "mpl"
        self.type = ptype # plot type
        # self.share = True

    def compile(self, engine=None):
        if engine is None:
            engine = self.engine
        return enginemap[engine].compile(self)

    def plot(self, engine=None, file=None, title=None):
        # overrride plot title
        if title is not None:
            self.title = title

        if engine is None:
            engine = self.engine

        enginemap[engine].plot(self, file=file)


    def copy(self):
        return copy.copy(self)

    def __add__(self, other):
        return PlotGroup([self, other], type="overlay", engine=self.engine, sharey=[True, True], legend=self.legend)

    def __sub__(self, other):
        return PlotGroup([self, other], type="overlay", engine=self.engine, sharey=[True, False], legend=self.legend)

    # def __neg__(self):
    #     x = self.copy()
    #     x.share = False
    #     return x

    def __getitem__(self, sliced):
        new = self.copy()
        new.x = new.x[sliced]
        new.y = new.y[sliced]
        new.z = new.z if new.z is None else new.z[sliced]
        new.labels = new.labels if new.labels is None else new.labels[sliced]
        return new


class PlotGroup(object):
    def __init__(self, items=[], engine="mpl", type="overlay", sharex=None, sharey=None, legend="br", title="Plot"):
        # TODO: implement the use of share being passed as parameter
        self.items = items
        self.sharex = [True for item in items]if sharex is None else sharex
        self.sharey = [True for item in items]if sharey is None else sharey
        self.type = type
        self.engine = engine
        #self.share = share
        self.legend = legend
        self.title = title

    def compile(self, engine=None):
        if engine is None:
            engine = self.engine
        return enginemap[engine].compilegroup(self)

    def plot(self, engine=None, file=None, title=None):
        # overrride plot title
        if title is not None:
            self.title = title
        if engine is None:
            engine = self.engine
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
        elif isinstance(other, ProtoPlot):
            new.items.append(other)
            new.sharex.append(True)
            new.sharey.append(True)
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

        elif isinstance(other, ProtoPlot):
            # TODO: this one is totally modifying the original object. Need to change this
            other_item = other
            # other.share = False
            new.items.append(other)
            new.sharex.append(True)
            new.sharey.append(False)
        return new

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
