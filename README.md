# Graphotti

This is a library for creating plots in python that is guided by the following principles:

- **Simple, intuitive, and consistent api**
    - Creating plots should have an easy api that also allow very simple customization of the x,y axes and grids.
- **Easy Plot Mashability**.
    - Often times you have several separate plots that you want to combine into a single plot, eg overlaying them, or stacking them on top of each other, or next to each other. But doing so can be a hassle.
    - But it shouldnt be a hassle. It should be as easy as doing simple arithmetic to combine them.
    - It should be as easy as `a+b+c`, literally. One of the aims of this library is to make this arithmetic syntax have meaning for the plots, and combine them in different ways depending on the mathematical operator used.
- **Plotting Library Agnostic**
    - whether you plan on rendering the plots in matplotlib, plotly, or some other python plotting library, you should not have to write completely new code from scratch. Switch between different plotting libraries as easily as changing a single vairable value.
    - eg: `p1.plot(engine="mpl")` to plot in matplotlib and then using the same plot object to plot in plotly by using `p1.plot(engine="plotly")`


Read the [white paper](white_paper.md) for more information about the ambitions of this project.

## Installing and Setting up

TODO

## Simple Introduction for creating plots

TODO

## Contributing

See the [contributing.md](contributing.md) file for details on how to contribute to this project. 
