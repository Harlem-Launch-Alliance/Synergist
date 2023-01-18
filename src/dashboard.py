import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import cache
import logging
import dash_vtk
from dash_vtk.utils import to_volume_state
import vtk
from dash_vtk.utils import to_mesh_state
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
import os
import numpy as np
from datetime import timedelta

app = dash.Dash()


rocketObjPath = r"./assets/SR2.obj"
rocketMtlPath = r"./assets/SR2.mtl"

# importer = vtk.vtkOBJImporter()
# importer.SetFileName(rocketObjPath)
# importer.SetFileNameMTL(rocketMtlPath)
# importer.SetTexturePath(os.path.dirname(rocketObjPath))
# importer.Read()
# window = importer.GetRenderWindow()
# renderer = window.GetRenderers().GetItemAsObject(0)
# actors = renderer.GetActors()
# actors = [actors.GetItemAsObject(i) for i in range(actors.GetNumberOfItems())]
# meshes = [a.GetMapper().GetInput() for a in actors]

reader = vtk.vtkOBJReader()
reader.SetFileName(rocketObjPath)
reader.Update()

dataset = reader.GetOutput()

mesh_state = to_mesh_state(dataset)

#arrangment of dashboard using HTML
app.layout = html.Div(
    [
        html.H2('Catalyst-2', style={'color':"#aaaaaa"}),
        html.Div(
            style={"width": "30%", "height": "50%", "display": "inline-block"},
            children=[
                dash_vtk.View([
                    dash_vtk.GeometryRepresentation(
                        [dash_vtk.Mesh(state=mesh_state)]
                    )],
                    cameraViewUp=[0.1,0.2,1.8],
                    #cameraPosition=[1, 1, 0],
                    id="orientation"
                )
            ],
        ),
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
        Output('orientation', 'cameraViewUp'),
        Output('LocationMap','figure'),
        Input('interval-component', 'n_intervals'))
def updateDashboard(n):
    while(not inputCache.empty()):
        cache.cacheValue(inputCache.get())
    altitudeFig = updateAltitude()
    currentState = updateFlightState()
    orientation = updateOrientation()
    mapFig = updateMap()
    return altitudeFig, currentState, orientation, mapFig

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

    if(cache.flightState["last"] == "LANDED" and cache.altitudeCache["time"][-1].timestamp() * 1000 >= (cache.flightState["LANDED"].timestamp() * 1000 + 5000)):
        #check to see if the time on the data is 5 seconds after the landing

        timeAfterLanding =  altitudeTime < cache.flightState["LANDED"] + timedelta(seconds=5) #select the data up to T+5 from landing

        altitudeData = np.extract(timeAfterLanding, altitudeData)
        altitudeTime = np.extract(timeAfterLanding, altitudeTime)

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
            yaxis={'title': "Altitude (m)", 'range': (min(altitudeData), max(altitudeData) * 1.01 + 10)},
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

def updateOrientation():
    return [0,1,0]

def updateMap():

    lat = cache.locationCache["latitude"]
    lon = cache.locationCache["longitude"]

    fig = go.Figure(go.Scattermapbox(lat=lat, lon = lon, mode = "markers+lines", line = dict(width = 1, color = 'blue'), marker = dict(size = 5, color = "blue")))

    fig.update_layout(
    hovermode='closest',
    mapbox=dict(
        style = "open-street-map",
        center = dict(lat = lat[-1], lon = lon[-1]),
        zoom = 15
        ),
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    uirevision="Don't change" #this is not a keyword, as long as this text doesnt change then the mapbox will not reset
    )
    return fig