# myapp.py

import logging
from random import random

import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import column, row, widgetbox
from bokeh.models import Button, Toggle
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure

# create a plot and style its properties
p1 = figure(x_range=(0, 100), y_range=(0, 100), toolbar_location=None)
p2 = figure(x_range=(100, 200), y_range=(100, 200), toolbar_location=None)

p1.border_fill_color = 'black'
p2.border_fill_color = 'yellow'

p1.background_fill_color = 'black'
p2.background_fill_color = 'green'

p1.outline_line_color = None
p2.outline_line_color = None

p1.grid.grid_line_color = None
p2.grid.grid_line_color = None

# Set up data
N = 200
x = np.linspace(0, 4 * np.pi, N)
y = np.sin(x)
source = ColumnDataSource(data=dict(x=x, y=y))

# Set up plot
plot = figure(plot_height=400, plot_width=400, title="my sine wave #1",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 4 * np.pi], y_range=[-2.5, 2.5])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

# Set up widgets
text = TextInput(title="this is sliders widget #1", value='my sine wave #1')
offset = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
amplitude = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0, step=0.1)
phase = Slider(title="phase", value=0.0, start=0.0, end=2 * np.pi)
freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)


# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value


text.on_change('value', update_title)


def update_data(attrname, old, new):
    # Get the current slider values
    a = amplitude.value
    b = offset.value
    w = phase.value
    k = freq.value

    # Generate the new curve
    x = np.linspace(0, 4 * np.pi, N)
    y = a * np.sin(k * x + w) + b

    source.data = dict(x=x, y=y)


for w in [offset, amplitude, phase, freq]:
    w.on_change('value', update_data)

# Set up layouts and add to document
inputs = widgetbox(text, offset, amplitude, phase, freq)
inputs.name = 'xyz'
logging.warn('inputs = ')
logging.warn(inputs.__dict__)

# add a text renderer to our plot (no data yet)
r1 = p1.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt", text_baseline="middle", text_align="center")

# add a text renderer to our plot (no data yet)
r2 = p2.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt", text_baseline="middle", text_align="center")

i = 0
y = 0

ds1 = r1.data_source
ds2 = r2.data_source


# create a callback that will add a number in a random location
def callback():
    global i

    # BEST PRACTICE --- update .data in one step with a new dict
    new_data = dict()
    new_data['x'] = ds1.data['x'] + [random() * 70 + 15]
    new_data['y'] = ds1.data['y'] + [random() * 70 + 15]
    new_data['text_color'] = ds1.data['text_color'] + [RdYlBu3[i % 3]]
    new_data['text'] = ds1.data['text'] + [str(i)]
    ds1.data = new_data

    i = i + 1


def callback2():
    global y

    # BEST PRACTICE --- update .data in one step with a new dict
    new_data = dict()
    new_data['x'] = ds2.data['x'] + [random() * 70 + 100]
    new_data['y'] = ds2.data['y'] + [random() * 70 + 100]
    new_data['text_color'] = ds2.data['text_color'] + [RdYlBu3[y % 3]]
    new_data['text'] = ds2.data['text'] + [str(y)]
    ds2.data = new_data

    y = y + 1


shown = False


def callback3():
    global shown

    if not shown:
        doc.add_root(secret_row_1)
        shown = True
        button3.label = "Hide Sliders Demo"

    else:
        doc.remove_root(secret_row_1)
        shown = False
        button3.label = "Display Sliders Demo"


# Set up data
N2 = 200
x2 = np.linspace(0, 4 * np.pi, N2)
y2 = np.sin(x2)
source2 = ColumnDataSource(data=dict(x=x2, y=y2))

# Set up plot
plot2 = figure(plot_height=400, plot_width=400, title="my sine wave #2",
               tools="crosshair,pan,reset,save,wheel_zoom",
               x_range=[0, 4 * np.pi], y_range=[-2.5, 2.5])

plot2.line('x', 'y', source=source2, line_width=3, line_alpha=0.6)

# Set up widgets
text2 = TextInput(title="this is sliders widget #1", value='my sine wave #2')
offset2 = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
amplitude2 = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0, step=0.1)
phase2 = Slider(title="phase", value=0.0, start=0.0, end=2 * np.pi)
freq2 = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)


# Set up callbacks
def update_title2(attrname, old, new):
    plot2.title.text = text2.value


text2.on_change('value', update_title2)


def update_data2(attrname, old, new):
    # Get the current slider values
    a = amplitude2.value
    b = offset2.value
    w = phase2.value
    k = freq2.value

    # Generate the new curve
    x = np.linspace(0, 4 * np.pi, N2)
    y = a * np.sin(k * x + w) + b

    source2.data = dict(x=x, y=y)


for w2 in [offset2, amplitude2, phase2, freq2]:
    w2.on_change('value', update_data2)

# Set up layouts and add to document
inputs2 = widgetbox(text2, offset2, amplitude2, phase2, freq2)

# add a button widget and configure with the call back
button = Button(label="Press Me")
button.on_click(callback)

# add a button widget and configure with the call back
button2 = Button(label="Press Me too!")
button2.on_click(callback2)

button3 = Button(label="Display Sliders Demo")
button3.on_click(callback3)

doc = curdoc()

button4 = Toggle(label="Settings", button_type="success")

# put the button and plot in a layout and add to the document
doc.add_root(row(column(button, p1), column(button2, p2)))
doc.add_root(row(column(button3)))
secret_row_1 = row(column(button4, inputs, plot, width=400))

child = secret_row_1.children[0].children.pop(1)


def callback4(toggled):
    global child
    if not toggled:
        secret_row_1.children[0].children.pop(1)
    else:
        secret_row_1.children[0].children.insert(1, child)


button4.on_click(callback4)

