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
                title="plot", name="plot",
                scalex="linear", scaley="linear", scalez="linear",
                ptype="scatter",
                ):
        self.x = []
        self.y = []
        self.z = []
        self.labels = []

        self.scalex = "linear"
        self.scaley = "linear"
        self.scaley = "linear"

        self.title = "plot"
        self.name = "plot"
        self.ax = Ax()
        self.engine = "mpl"
        self.type = ptype

    def compile(self, engine=None):
        raise NotImplementedError
        if engine is None:
            engine = self.engine

    def plot(self, engine=None, file=None):
        raise NotImplementedError
        if engine is None:
            engine = self.engine
        compiled = self.compile(engine=engine)

        if file is not None:
            # Either save the plot to file, or show it.
            pass
        # TODO: handle of showing the plot differently depending on the engine
