import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import cache
import logging
import dash_daq as daq

app = dash.Dash()
#fig = go.FigureWidget()
app.layout = html.Div(
    [
        html.H2('Catalyst-2', style={'color':"#aaaaaa"}),
        dcc.Graph(id="altitude", figure=go.FigureWidget()),
        html.Div([
            html.H2('Current State: ', id = "flightState", style={'color':"#aaaaaa"})
        ]),
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
@app.callback(
        Output('altitude', 'figure'),
        Output('flightState', 'children'),
        Input('interval-component', 'n_intervals'))
def updateDashboard(n):
    while(not inputCache.empty()):
        cache.cacheValue(inputCache.get())
    altitudeFig = go.Figure(
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
    if(cache.flightState["ASCENDING"] != 0):
        altitudeFig.add_vline(x=cache.flightState["ASCENDING"].timestamp() * 1000, line_dash="dash", line_color="green", annotation_text="LAUNCH DETECTED", annotation_textangle=-90, annotation_position="top left")
    if(cache.flightState["DESCENDING"] != 0):
        altitudeFig.add_vline(x=cache.flightState["DESCENDING"].timestamp() * 1000, line_dash="dash", line_color="red", annotation_text="APOGEE DETECTED", annotation_textangle=-90, annotation_position="bottom left")
    if(cache.flightState["LANDED"] != 0):
        altitudeFig.add_vline(x=cache.flightState["LANDED"].timestamp() * 1000, line_dash="dash", line_color="orange", annotation_text="LANDING DETECTED", annotation_textangle=-90, annotation_position="top left")

    currentState = 'Current State: ' + cache.flightState["last"]

    return altitudeFig, currentState

def startDash(dataQueue):
    global inputCache
    inputCache = dataQueue
    app.run_server(use_reloader=False, host='0.0.0.0')