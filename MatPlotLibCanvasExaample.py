#!/usr/bin/env python
# -*- noplot -*-

import matplotlib as mpl
import numpy as np
import tkinter as tk
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg

# from ClearSpectrum2
from matplotlib.pyplot import *
from mpl_toolkits.axes_grid1.axes_rgb import make_rgb_axes, RGBAxes


def draw_figure(canvas, figure, loc=(0, 0)):
    """ Draw a matplotlib figure onto a Tk canvas

    loc: location of top-left corner of figure on canvas in pixels.

    Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
    """
    figure_canvas_agg = FigureCanvasAgg(figure)
    figure_canvas_agg.draw()
    figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
    figure_w, figure_h = int(figure_w), int(figure_h)
    photo = tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)

    # Position: convert from top-left anchor to center anchor
    canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)

    # Unfortunatly, there's no accessor for the pointer to the native renderer
    tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

    # Return a handle which contains a reference to the photo object
    # which must be kept live or else the picture disappears
    return photo

# Create a canvas
w, h = 800, 400
window = tk.Tk()
window.title("A figure in a canvas")
canvas = tk.Canvas(window, width=w, height=h)


canvas.pack()


# Generate some example data

X = np.linspace(0, 2.0*3.14, 50)
Y = np.sin(X)

# Create the figure we desire to add to an existing canvas



test_fig = mpl.figure.Figure(figsize=(1, 1))
ff = test_fig.get_dpi()
print(ff)
widthToSet = (w/ff)/2
print(widthToSet)
heightToSet = (h/ff)/2
print(heightToSet)
fig = mpl.figure.Figure(figsize=(widthToSet, heightToSet))
#fig = mpl.figure.Figure(figsize=(1, 1))

ax = fig.add_axes([0, 0, 1, 1])
ax.plot(X, Y)
fig.show()

# Keep this handle alive, or else figure will disappear
fig_x, fig_y = 100, 100

anotherFigure = figure(1, figsize=(3,2))
xx = anotherFigure.add_axes([0, 0, .5, .5])
xx.plot(X,Y)
anotherFigure.show()

fig_photo = draw_figure(canvas, anotherFigure, loc=(fig_x, fig_y))
fig_w, fig_h = fig_photo.width(), fig_photo.height()

# Add more elements to the canvas, potentially on top of the figure
canvas.create_line(200, 50, fig_x + fig_w / 2, fig_y + fig_h / 2)
canvas.create_text(200, 50, text="Zero-crossing", anchor="s")

# Let Tk take over
tk.mainloop()
