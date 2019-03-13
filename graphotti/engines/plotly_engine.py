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
from plotly import tools


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

        fig = plt.create_figure(traces=traces, title=obj.title, xlabel=obj.xlabel, ylabel=obj.ylabel, scaley=obj.scaley)
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

        fig = plt.create_figure(traces=traces, title=group.title, xlabel=group.items[0].xlabel, ylabel=group.items[0].ylabel, sharey=group.sharey, scaley=group.scaley)
        return fig


    def compilegrid(self, grid_items):
        # TODO: maybe to properly share an axis, use  the anchor property
        #        https://plot.ly/python/subplots/
        """ Given a 2d Array/list of plot objects it creates a grid plot """
        # if group.type == "overlay":
        grid_items = grid_items.copy()
        traces = []

        for i in range(len(grid_items.items)):
            row = []
            for j in range(len(grid_items.items[i])):
                try:
                    item = grid_items.items[i][j]
                    if item.type == "lineplot":
                        trace = plt.lineplot(p=item, color=item.color)
                        row.append(trace)
                    elif item.type == "scatter":
                        trace = plt.scatter(p=item, color=item.color)
                        row.append(trace)
                    elif item.type == "step":
                        trace = plt.step(p=item, color=item.color)
                        row.append(trace)
                    else:
                        assert False, "invalid value for plot type"
                except:
                    print("plotting grid cell {}{} failed".format(i,j))
                    pass
            traces.append(row)

            fig = tools.make_subplots(rows=len(grid_items.items), cols=max([len(rr) for rr in grid_items.items]),
                                      shared_yaxes=False,
                                      shared_xaxes=grid_items.sharex,
                                      # subplot_titles=None,
                                      horizontal_spacing=0.05,
                                      vertical_spacing=0.1,
                                      )


            for i in range(len(traces)):
                for j in range(len(traces[i])):
                    try:
                        fig.append_trace(traces[i][j], i+1, j+1)
                    except:
                        print("something skipped")

        # fig = plt.create_figure(traces=traces, title=group.title, xlabel=group.items[0].xlabel, ylabel=group.items[0].ylabel, sharey=group.sharey)
        return fig
        # return traces

    def plotgrid(self, grid_items, file=None):
        fig = self.compilegrid(grid_items)
        if file is None:
            iplot(fig)
        else:
            plot(fig, filename=file)

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
