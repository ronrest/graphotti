# TODO: allow addition of more than 2 items
# TODO: overlload math operators for PlotGroup as well
# TODO: allow addition of PlotGroups with ProtoPlot objects
# TODO: allow addition PlotGroups

# TODO: i think that the `share` property might be better stored in the PlotGroup
#       object rather than the ProtoPlot object. This will allow for the individual
#       plots to be updatable, and not having to do new copies of the ProtoPlot
#       objects when set to share=False

import pandas as pd
from engines import enginemap
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

        self.xlabel = "x"
        self.ylabel = "y"
        self.zlabel = "z"

        self.xrot = 0
        self.yrot = 0
        self.zrot = 0

        self.color = color
        self.alpha = alpha
        self.size = size
        self.width = width

        self.title = title
        self.name = name
        self.ax = Ax()

        self.majorgrid = True
        self.minorgrid = True

        self.engine = "mpl"
        self.type = ptype # plot type
        self.share = True

    def compile(self, engine=None):
        if engine is None:
            engine = self.engine
        return enginemap[engine].compile(self)

    def plot(self, engine=None, file=None):
        if engine is None:
            engine = self.engine

        enginemap[engine].plot(self, file=file)


    def copy(self):
        return copy.copy(self)

    def __add__(self, other):
        return PlotGroup([self, other], type="overlay", engine=self.engine, share=True, legend=self.legend)

    def __sub__(self, other):
        return PlotGroup([self, -other], type="overlay", engine=self.engine, share=False, legend=self.legend)

    def __neg__(self):
        x = self.copy()
        x.share = False
        return x


class PlotGroup(object):
    def __init__(self, items=[], engine="mpl", type="overlay", share=True, legend="br"):
        # TODO: implement the use of share being passed as parameter
        self.items = items
        self.type = type
        self.engine = engine
        self.share = share
        self.legend = legend

    def compile(self, engine=None):
        if engine is None:
            engine = self.engine
        return enginemap[engine].compilegroup(self)

    def plot(self, engine=None, file=None):
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
        elif isinstance(other, ProtoPlot):
            new.items.append(other)
        return new

    def __sub__(self, other):
        # TODO: need to check if this is modifying the original `other` group,
        #       or applying share=False to a new object
        new = self.copy()
        if isinstance(other, PlotGroup):
            other_items = other.items
            other_items[0].share = False
            new.items.extend(other_items)
        elif isinstance(other, ProtoPlot):
            # TODO: this one is totally modifying the original object. Need to change this
            other_item = other
            other.share = False
            new.items.append(other_item)
        return new




# ##############################################################################
#                                        PLOT FUNCTIONS
# ##############################################################################
def lineplot(x, y=None,
    color=None, alpha=1.0, size=1, width=1,
    labels=None, title="plot", name="line",
    scalex="linear", scaley="linear",
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
                ptype="lineplot")
