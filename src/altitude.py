import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import cache
import logging
import dash_daq as daq

app = dash.Dash()
fig = go.FigureWidget()
app.layout = html.Div(
    [
        html.H2('Catalyst-2', style={'color':"#CECECE"}),
        dcc.Graph(id="altitude", figure=fig),
        dcc.Interval(
            id='interval-component',
            interval=500, # in milliseconds
            n_intervals=0
        )
    ], style={'backgroundColor': '#111111', 'margin-top':'-20px', 'height':'2000px', 'width': '100%'}
)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#TODO use batch_update()
@app.callback(Output('altitude', 'figure'), 
        Input('interval-component', 'n_intervals'))
def updateAltitude(n):
    while(not inputCache.empty()):
        cache.cacheValue(inputCache.get())
    fig = go.Figure(
        data=[go.Scatter
            (x=cache.altitudeCache["time"], 
            y=cache.altitudeCache["altitude"])
        ],
        layout=go.Layout(
            title="Altitude",
            width=1000,
            height=500,
            template="plotly_dark",
            xaxis={'title': "Time"},
            yaxis={'title': "Altitude (m)", 'range': (min(cache.altitudeCache["altitude"]), max(cache.altitudeCache["altitude"]) + 10)},
        )
    )
    return fig

def startDash(dataQueue):
    global inputCache
    inputCache = dataQueue
    app.run_server(use_reloader=False, host='0.0.0.0')