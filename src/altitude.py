import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import cache
import logging
import dash_daq as daq

app = dash.Dash()
fig = go.FigureWidget()
app.layout = html.Div([
    html.H3('Catalyst-2'),
    dcc.Graph(id="altitude", figure=fig),
    dcc.Interval(
        id='interval-component',
        interval=100, # in milliseconds
        n_intervals=0
    )
])

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#TODO use batch_update()
@app.callback(Output('altitude', 'figure'), 
        Input('interval-component', 'n_intervals'))
def updateAltitude(n):
    while(not inputCache.empty()):
        cache.cacheValue(inputCache.get())
    fig = go.Figure(data=[go.Scatter(x=cache.altitudeCache["time"], y=cache.altitudeCache["altitude"])],
        layout=go.Layout(
            title="Altitude",
            width=1000,
            height=500,
            template="plotly_dark"
        )
    )
    return fig

def startDash(dataQueue):
    global inputCache
    inputCache = dataQueue
    app.run_server(use_reloader=False)