from flask import Flask, render_template, jsonify, request
#from bokeh.resources import INLINE
from bokeh.models.sources import AjaxDataSource, ColumnDataSource
from flask import render_template
from bokeh.plotting import figure
from bokeh.embed import components
from flask import Flask, request
import numpy as np
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/query')
def query_plot():
    x = request.args.get("x")
    y = request.args.get("y")
    X = x.split(",") if "," in x else [x]
    Y = y.split(",") if "," in y else [y]

    X = [float(x) for x in X]
    Y = [float(y) for y in Y]
    jsn = {"x": X, "y": Y}
    
    plots = []
    plots.append(make_ajax_query_plot(jsn))

    return render_template('dashboard.html', plots=plots)

@app.route('/dashboard/')
def show_dashboard():
    plots = []
    plots.append(make_plot())

    return render_template('dashboard.html', plots=plots)

@app.route('/stream')
def show_stream():
    plots = []
    plots.append(make_ajax_plot())

    return render_template('dashboard.html', plots=plots)


x = 0
@app.route('/data/', methods=['POST'])
def data():
    global x
    x += 0.1
    y = np.sin(x)
    return jsonify(x=[x], y=[y])

def make_plot():
    plot = figure(plot_height=300, sizing_mode='scale_width')

    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = [2**v for v in x]

    plot.line(x, y, line_width=4)

    script, div = components(plot)
    return script, div


def make_ajax_plot():
    source = AjaxDataSource(data_url=request.url_root + 'data/',
                            polling_interval=300, max_size=100, mode='append')

    source.data = dict(x=[], y=[])

    plot = figure(plot_height=300, sizing_mode='scale_width')
    plot.line('x', 'y', source=source, line_width=4)
    
    script, div = components(plot)
    return script, div

def make_ajax_query_plot(data):
    source_query = ColumnDataSource()
    source_query.data = data
    
    plot = figure(plot_height=300, sizing_mode='scale_width')
    plot.line('x', 'y', source=source_query, line_width=4)
    plot.circle('x', 'y', source=source_query,size=8, fill_color="white", color="red")

    script, div = components(plot)
    return script, div

