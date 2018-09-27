# Graphotti

This document describes the vision of what this library should try to accomplish. It is not a documenation of the current API, or a reflection of what the API will actually look like in the future. Things will likely evolve over time and look and behave differently from what is described here.

This is simple a document to provide a goal post to aim towards.

## Motivation

This project was born out of the following few frustrations of creating plots in python:
    - There is usually quite a fair bit of boilerplate code needed to get exploratory data analysis plots that allow customization of axes, and grids.
    - Combining plots together is a hassle.
    - In order to render the same plot using different plotting libraries involves writing everything from scratch, with more aditional over head, and the frustration of having to deal with the peculiarities of each library.

This project is therefore guided by the folloiwng principles:

- **Simple, intuitive, and consistent api**
    - An easy api for creating plots that also allow very simple customization of the x,y axes and grids.
- **Easy Plot Mashability**.
    - Often times you have several separate plots that you want to combine into a single plot, eg overlaying them, or stacking them on top of each other, or next to each other. But doing so is a hassle.
    - But it shouldnt be a hassle. It should be as easy as doing simple arithmetic to combine them.
    - It should be as easy as `a+b+c`, literally. One of the aims of this library is to make this arithmetic syntax have meaning for the plots, and combine them in different ways depending on the mathematical operator used.
- **Plotting Library Agnostic**
    - whether you plan on rendering the plots in matplotlib, plotly, or some other python plotting library, you should not have to write completely new code from scratch. Switch between different plotting libraries as easily as changing a single vairable value.
    - eg: `p1.plot(engine="mpl")` to plot in matplotlib and then using the same plot object to plot in plotly by using `p1.plot(engine="plotly")`
- **Explorability**
    - It should be easy for you to explore your data without being bogged down by syntax and boilerplate code.
- **Intuition Building**
    - It should be quick and easy to plot functions such as `sin` or `cos` or any other math functions easily, in order to get an intuition of what they do. Ideally it should be done by just writing a math formula in text, without having to manually create your own x and y arrays using math libraries.
    - eg: `funcplot("exp(x)/(1+exp(x))")`

The aim is not to be a highly customizable plotting library like matplotlib or plotly, but just customizable enough to be useful for the porposes of common exploratory data analysis tasks used by a data scientist, with minimal friction or overhead. It is designed to be streamlined so that data scientists can spend time exploring and less time writing code.

## Primitives

The library plans on including some primitive plots.

### scatterplot

TODO

### lineplot

TODO

### Timeline

**params**

- `starttime`
- `endtime`
- `resolution`
    - allows you to aggregate the data at particular resolution intervals
    - `None` (default) does not do any aggregation
- `stagger`
    - `True` if eg you set resolution to daily, but your first data point is at 3:30 pm, then it aggregates data at 3:30 each day.
    - `False` if set to eg daily, then it uses midnight 00:00:00 as the cutoff point for each aggregated day.
- `stagger_point`
    - some kind of datetime delta type object, or string that can be conveted to such, that tells you what the cutoff point is for the cutoff point at which to perform stagggering.
    - eg: if you chose daily resolution, and want to stagger, but want to set a different point than the first data point, you may eg select the cutoff point to be 5:50 each day.
    -
- `agg` aggregation function


### heatmap

TODO

### corrplot

correlatin matrix plot


### bar plot

TODO

### bar distribution plot

TODO


### density plot

TODO

### whisker plot

TODO

## Combining plots

- `overlay(p1,p2,p3)`
- `vstack(p1,p2,p3)`
- `hstack(p1,p2,p3)`
- `grid([[p1,p2],[p3, p4], [p5, p6]])`
- `grid(p1,p2,p3,p4,p5,p6, shape=[3,2])`

## Plot arithmetic

Combining plots together should be as easy as `a+b+c`. The following are how the  mathematical operators are planned to be interpreted by this library.

- `p1+p2+p3` overlay plots (sharing y axis)
- `p1+(-p2)+(-p3)` overlay plots (with independent y axis)

- `p1/p2/p3` Stack the plots one below the other (sharing x axis)
- `p1/(-p2)/(-p3)` Stack the plots one below the other (independent x axis)

- `p1*p2*p3` Stack the plots side by side (sharing y axis)
- `p1*(-p2)*(-p3)` Stack the plots side by side (independent y axis)

- `(p1 * p2)/(p3* p4)/(p5* p6)` Create a 3x2 grid of plots. TODO: create a null plot object for when you want a place holder for blank cells.

## Render

You should be able to render the same plot using different plotting libraries easily, such as:


```py
p1.plot(engine="mpl")
p1.plot(engine="plotly")
```


## Plot conversions

Instead of having to specify the data of an object all over again to visualize things differently, you should be able to just do a conversion.

eg: if `p1` is a lineplot, but you want to convert it to a scatterplot just do :

`p1.to("scatterplot")`


## Export

Should be able to export the plot data into formats such as:

- `json`
-
