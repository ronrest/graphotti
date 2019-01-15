import matplotlib

def rescale(x, range, newrange=(0,1)):
    mina, maxa = range
    minb, maxb = newrange
    return ((x-mina)/(maxa-mina) * (maxb-minb)) + minb


def rgb2hex(x, alpha=False):
    """
    Takes a tuple of rgb values as either:
    - floats in the range 0-1
    - ints in the range 0-255

    and returns a Hex formatted RGB string, eg `"#FF0088"`
    """
    if isinstance(x[0], float):
        multiplier = 255
    else:
        multiplier = 1
    r = "{:02x}".format(int(x[0]*multiplier))
    g = "{:02x}".format(int(x[1]*multiplier))
    b = "{:02x}".format(int(x[2]*multiplier))
    return ("#"+r+g+b).upper()


# # COLOR RANGE
def color_range(n, cmap="YlOrRd"):
    """ takes a matplotlib colormap name and returns a list of n RGB values
        interpolated alond that colormap
    """
    cmap = matplotlib.cm.get_cmap(cmap)
    c = [rgb2hex(cmap(x)) for x in np.linspace(0,1,n)]
    return c

