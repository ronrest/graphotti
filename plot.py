from engines import enginemap

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
