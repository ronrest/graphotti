# TODO: allow addition of more than 2 items
# TODO: overlload math operators for PlotGroup as well
# TODO: allow addition of PlotGroups with ProtoPlot objects
# TODO: allow addition PlotGroups
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

        self.xangle = 0
        self.yangle = 0
        self.zangle = 0


class ProtoPlot(object):
    # TODO: Implement slicing operators.
    #        p1[start: end]
    #
    # TODO: Implement mathematical arithemtic operators for combining plots
    #       p1+p2+p3

    def __init__(self, x, y=None, z=None,
                color=None, opacity=1.0,
                size=1, width=1,
                labels=None,
                title="plot", name="plot",
                scalex="linear", scaley="linear", scalez="linear",
                ptype="scatter",
                start=None, end=None
                ):
        self.x = x
        self.y = y
        self.z = z
        self.labels = labels

        self.start = start
        self.end = end

        self.scalex = scalex
        self.scaley = scaley
        self.scaley = scalez

        self.color = color
        self.opacity = opacity
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
        raise NotImplementedError
        if engine is None:
            engine = self.engine
        compiled = self.compile(engine=engine)

        if file is not None:
            # Either save the plot to file, or show it.
            pass
        # TODO: handle of showing the plot differently depending on the engine

    def copy(self):
        return copy.copy(self)

    def __add__(self, other):
        return PlotGroup([self, other], type="overlay", engine=self.engine)

    def __neg__(self):
        x = self.copy()
        x.share = False
        return x

class PlotGroup(object):
    def __init__(self, items=[], engine="mpl", type="overlay", share=True):
        # TODO: implement the use of share being passed as parameter
        self.items = items
        self.type = type
        self.engine = engine
        self.share = share

    def compile(self, engine=None):
        if engine is None:
            engine = self.engine
        return enginemap[engine].compilegroup(self)

    def plot(self, engine=None, file=None):
        raise NotImplementedError


# ##############################################################################
#                                        PLOT FUNCTIONS
# ##############################################################################
def lineplot(x, y=None,
    color=None, opacity=1.0, size=1, width=1,
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
                color=color, opacity=opacity,
                size=size, width=width,
                labels=labels,
                title=title, name=name,
                scalex=scalex, scaley=scaley,
                ptype="lineplot")
