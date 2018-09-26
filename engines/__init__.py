
enginemap = dict(
    mpl = mplengine,
    plotly=plotlyengine,
    )


class ProtoEngine(object):
    def __init__():
        pass

    def plot(self, compiled):
        raise NotImplementedError

    def compile(self, obj):
        """ determines the type of plot to compile to and returns the
            compiled object.
        """
        raise NotImplem entedError


    def scatter(self, obj):
        raise NotImplementedError

    def lineplot(self, obj):
        raise NotImplementedError

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
