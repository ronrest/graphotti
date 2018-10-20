"""
POTLY ENGINE
"""
from . import plotly_funcs as plt

COLORS = [
    "#4286f4", # blue
    "#f49a41", # orange
    "#7cbf5b", # green
    "#a578ed", # lavender
    "#ed7d78", # guava
    "#fce06f", # yellow
    "#7be5ce", # aqua
    "#e87df2", # pink
    "#42874e", # dark green
    "#8c7646", # honey brown
    "#314b6d", # dark blue
    "#70767f", # grey
    "#683d3b", # terracota
    "#50335b", # dark purple
    ]


from plotly.offline import plot, iplot

class PlotlyEngine(object):
    def __init__(self):
        pass

    def plot(self, obj, file=None):
        fig = self.compile(obj)
        if file is None:
            iplot(fig)
        else:
            plot(fig, filename=file)

    def plotgroup(self, group, file=None):
        fig = self.compilegroup(group)
        if file is None:
            iplot(fig)
        else:
            plot(fig, filename=file)


    def compile(self, obj):
        """ determines the type of plot to compile to and returns the
            compiled object.
        """
        traces = []
        if obj.type == "lineplot":
            trace = plt.lineplot(p=obj, color=obj.color)
            traces.append(trace)
        elif obj.type == "scatter":
            trace = plt.scatter(p=obj, color=obj.color)
            traces.append(trace)
        elif obj.type == "step":
            trace = plt.step(p=obj, color=obj.color)
            traces.append(trace)
        else:
            assert False, "invalid value for plot type"

        fig = plt.create_figure(traces=traces, title=obj.title, xlabel=obj.xlabel, ylabel=obj.ylabel)
        return fig

    def compilegroup(self, group):
        # if group.type == "overlay":
        traces = []
        for item in group.items:
            if item.type == "lineplot":
                trace = plt.lineplot(p=item, color=item.color)
                traces.append(trace)
            elif item.type == "scatter":
                trace = plt.scatter(p=item, color=item.color)
                traces.append(trace)
            elif item.type == "step":
                trace = plt.step(p=item, color=item.color)
                traces.append(trace)
            else:
                assert False, "invalid value for plot type"

        fig = plt.create_figure(traces=traces, title=group.title, xlabel=group.items[0].xlabel, ylabel=group.items[0].ylabel, sharey=group.sharey)
        return fig


    def scatter(self, obj):
        raise NotImplementedError

    def lineplot(self, obj):
        return plt.lineplot(p=obj, ax=None, figsize=(10,6))

    def timelineplot(self, obj):
        raise NotImplementedError

    def barplot(self, obj):
        raise NotImplementedError

    def bardist(self, obj):
        """ bar distribution plot """
        raise NotImplementedError

    def densityplot(self, obj):
        raise NotImplementedError

    def densityplot(self, obj):
        raise NotImplementedError
