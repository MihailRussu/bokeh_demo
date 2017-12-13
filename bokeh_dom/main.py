# myapp.py

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
plot = figure(
    plot_height=400, plot_width=400, title="my sine wave #1", tools="crosshair,pan,reset,save,wheel_zoom",
    x_range=[0, 4 * np.pi], y_range=[-2.5, 2.5]
)
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
inputs = widgetbox(text, offset, amplitude, phase, freq, css_classes=['demo_controls'])

# add a text renderer to our plot (no data yet)
r1 = p1.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt", text_baseline="middle", text_align="center")

# add a text renderer to our plot (no data yet)
r2 = p2.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt", text_baseline="middle", text_align="center")

i = 0
y = 0

ds1 = r1.data_source
ds2 = r2.data_source


# create a callback_add_number_1 that will add a number in a random location
def callback_add_number_1():
    global i

    # BEST PRACTICE --- update .data in one step with a new dict
    new_data = dict()
    new_data['x'] = ds1.data['x'] + [random() * 70 + 15]
    new_data['y'] = ds1.data['y'] + [random() * 70 + 15]
    new_data['text_color'] = ds1.data['text_color'] + [RdYlBu3[i % 3]]
    new_data['text'] = ds1.data['text'] + [str(i)]
    ds1.data = new_data
    i += 1


def callback_add_number_2():
    global y

    # BEST PRACTICE --- update .data in one step with a new dict
    new_data = dict()
    new_data['x'] = ds2.data['x'] + [random() * 70 + 100]
    new_data['y'] = ds2.data['y'] + [random() * 70 + 100]
    new_data['text_color'] = ds2.data['text_color'] + [RdYlBu3[y % 3]]
    new_data['text'] = ds2.data['text'] + [str(y)]
    ds2.data = new_data
    y += 1


# add a btn_press_1 widget and configure with the call back
btn_press_1 = Button(label="Press Me")
btn_press_1.on_click(callback_add_number_1)

# add a btn_press_2 widget and configure with the call back
btn_press_2 = Button(label="Press Me too!")
btn_press_2.on_click(callback_add_number_2)

document = curdoc()

# put the btn_press_1 and plot in a layout and add to the document
document.add_root(row(column(btn_press_1, p1), column(btn_press_2, p2)))
document.add_root(
    row(
        column(
            inputs, plot, width=400, height=500, css_classes=["plot_demo"]
        )
    )
)

