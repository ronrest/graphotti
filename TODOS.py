# BUG: index error is thrown when using more than 2 plots, with independent y axes.
#      Seems to be an issue with the scaley list in the `create_figure()` function
#
#     Example:
#     a = gh.line([1,2,3,4,5,6,7])
#     b = gh.line([2,3,4,5,6,7,8])
#     c = gh.line([3,4,5,6,7,8,9])
#     g = a-b-c
#     g.plot("ply")
#

# TODO: interpret the scaly property in matplotlib engine
# TODO: for non-shared axes, have option to position the ticks and labels
#       on different sides of the plot.
#       Either:
#       1. Automatically alternate sides
#       2. Have a property in each individual plot or plotgroup that
#          allows you to manually set the side you want the ticks to be in.
