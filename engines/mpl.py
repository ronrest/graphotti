"""
MATPLOTLIB ENGINE
"""
from . import mpl_funcs as plt

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

class MPLEngine(object):
    def __init__(self):
        pass

    def plot(self, obj):
        fig, ax = self.compile(obj)
        fig.show()

    def plotgroup(self, group):
        fig, ax = self.compilegroup(group)
        fig.show()

    def compile(self, obj):
        """ determines the type of plot to compile to and returns the
            compiled object.
        """
        if obj.type == "lineplot":
            return plt.lineplot(p=obj, ax=None, figsize=(10,6))
        else:
            assert False, "invalid value for plot type"

    def compilegroup(self, group):
        if group.type == "overlay":
            n_items = len(group.items)
            ncolors = len(COLORS)
            # Assume for the time being that ALL the items in the group are
            # low level plot objects of type lineplot
            for i, obj in enumerate(group.items):
                showlegend = group.legend if i == (n_items -1) else None
                # color = COLORS[i%ncolors] if obj.color is None else obj.color
                color = COLORS[i%ncolors]
                if i == 0:
                    fig, ax = plt.lineplot(p=obj, ax=None, figsize=(10,6), legend=showlegend, color=color)
                else:
                    fig, ax = plt.lineplot(p=obj, ax=ax, legend=showlegend, color=color)
            return fig, ax
        else:
            assert False, "This group type {} is not implemented yet".format(group.type)

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
