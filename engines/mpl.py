"""
MATPLOTLIB ENGINE
"""
from . import mpl_funcs as plt

class MPLEngine(object):
    def __init__(self):
        pass

    def plot(self, compiled):
        raise NotImplementedError

    def compile(self, obj):
        """ determines the type of plot to compile to and returns the
            compiled object.
        """
        if obj.type == "lineplot":
            return plt.lineplot(obj)
        else:
            assert False, "invalid value for plot type"

    def compilegroup(self, group):
        if group.type == "overlay":
            # Assume for the time being that ALL the items in the group are
            # low level plot objects of type lineplot
            for i, obj in enumerate(group.items):
                if i == 0:
                    fig, ax = plt.lineplot(p=obj, ax=None, figsize=(10,6))
                else:
                    fig, ax = plt.lineplot(p=obj, ax=ax)
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
