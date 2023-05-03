import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import cache
import logging
import numpy as np
from datetime import timedelta

app = dash.Dash()

#arrangment of dashboard using HTML
app.layout = html.Div(
    [
        html.H2('Catalyst-2', style={'color':"#aaaaaa"}),
        html.Div([
            dcc.Graph(id="altitude", figure=go.FigureWidget()),
        ], style={"width": "65%", "height": "50%", "display": "inline-block"}),
        html.H2('Current State: ', id = "flightState", style={'color':"#aaaaaa"}),
        dcc.Interval(
            id='interval-component',
            interval=500, # in milliseconds
            n_intervals=0
        ),
        html.Div([
            dcc.Graph(id="LocationMap", figure=go.FigureWidget())
        ], style={"width": "50%", "height": "30%"})
    ], style={'backgroundColor': '#111111', 'margin-top':'-20px', 'height':'1200px', 'width': '100%'}
)

#removes log spam from incoming connections
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#this will run every time the "interval" timer is up
@app.callback(
        Output('altitude', 'figure'),
        Output('flightState', 'children'),
        Output('LocationMap','figure'),
        Input('interval-component', 'n_intervals'))
def updateDashboard(n):
    while(not inputCache.empty()):
        cache.cacheValue(inputCache.get())
    altitudeFig = updateAltitude()
    currentState = updateFlightState()
    mapFig = updateMap()
    return altitudeFig, currentState, mapFig

#start Dashboard with above configuration
def startDash(dataQueue):
    global inputCache
    inputCache = dataQueue
    app.run_server(use_reloader=False, host='0.0.0.0')

#update Altitude Graph
def updateAltitude():

    altitudeTime = np.asarray(cache.altitudeCache["time"])
    altitudeData = np.asarray(cache.altitudeCache["altitude"])

    if(cache.flightState["ASCENDING"] != 0):
        #check to see if launch detected

        timeBeforeLaunch = altitudeTime > cache.flightState["ASCENDING"] - timedelta(seconds=10) #select the data from T-10 from launch and beyond

        altitudeData = np.extract(timeBeforeLaunch, altitudeData)
        altitudeTime = np.extract(timeBeforeLaunch, altitudeTime)

    elif len(altitudeData):
        #before launch, maintain the last 10 seconds of altitude data on the graph

        timeWindow = altitudeTime > altitudeTime[-1] - timedelta(seconds=10)

        altitudeData = np.extract(timeWindow, altitudeData)
        altitudeTime = np.extract(timeWindow, altitudeTime)

    if(cache.flightState["last"] == "LANDED" and cache.altitudeCache["time"][-1].timestamp() * 1000 >= (cache.flightState["LANDED"].timestamp() * 1000 + 5000)):
        #check to see if the time on the data is 5 seconds after the landing

        timeAfterLanding =  altitudeTime < cache.flightState["LANDED"] + timedelta(seconds=5) #select the data up to T+5 from landing

        altitudeData = np.extract(timeAfterLanding, altitudeData)
        altitudeTime = np.extract(timeAfterLanding, altitudeTime)

    yRangeMin = min(altitudeData) if len(altitudeData) else 0
    yRangeMax = max(altitudeData) * 1.01 + 10 if len(altitudeData) else 10

    fig = go.Figure(
        data=[go.Scatter
            (x=altitudeTime, 
            y=altitudeData)
        ],
        layout=go.Layout(
            title="Altitude",
            width=1000,
            height=500,
            template="plotly_dark",
            xaxis={'title': "Time"},
            yaxis={'title': "Altitude (m)", 'range': (yRangeMin, yRangeMax)},
        )
    )
    if(cache.flightState["ASCENDING"] != 0):
        fig.add_vline(x=cache.flightState["ASCENDING"].timestamp() * 1000, line_dash="dash", line_color="orange", annotation_text="LAUNCH DETECTED", annotation_textangle=-90, annotation_position="top left")
    if(cache.flightState["DESCENDING"] != 0):
        fig.add_vline(x=cache.flightState["DESCENDING"].timestamp() * 1000, line_dash="dash", line_color="orange", annotation_text="APOGEE DETECTED", annotation_textangle=-90, annotation_position="bottom left")
    if(cache.flightState["LANDED"] != 0):
        fig.add_vline(x=cache.flightState["LANDED"].timestamp() * 1000, line_dash="dash", line_color="orange", annotation_text="LANDING DETECTED", annotation_textangle=-90, annotation_position="top left")
    return fig

#update flight state
def updateFlightState():
    currentState = 'Current State: ' + cache.flightState["last"]
    return currentState

def updateMap():

    lat = cache.locationCache["latitude"]
    lon = cache.locationCache["longitude"]

    fig = go.Figure(go.Scattermapbox(lat=lat, lon = lon, mode = "markers+lines", line = dict(width = 1, color = 'blue'), marker = dict(size = 5, color = "blue")))

    fig.update_layout(
    hovermode='closest',
    mapbox=dict(
        style = "open-street-map",
        center = dict(
            lat = lat[-1] if len(lat) else 0, 
            lon = lon[-1] if len(lon) else 0, 
        ),
        zoom = 15
        ),
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    uirevision="Don't change" #this is not a keyword, as long as this text doesnt change then the mapbox will not reset
    )
    return fig