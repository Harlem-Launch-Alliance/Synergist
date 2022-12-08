from datetime import datetime
import dash
from dash import dcc, html
import plotly.graph_objects as go
import cache

def handleAltitude(dataArray):
    altitude = dataArray[3]
    print(f"Altitude (m): {altitude}")
    currentTime = datetime.now()
    print(f"Current time: {currentTime}")

def startDash():
    app = dash.Dash()
    fig = go.FigureWidget()
    fig.add_scatter(y=[0], x=[0])
    scatter = fig.data[0]
    app.layout = html.Div([dcc.Graph(id="altitude", figure=fig)])

    app.run_server(use_reloader=False)