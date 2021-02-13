import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import pandas as pd

import dash_leaflet as dl
import sys
import os.path
sys.path.append(os.path.dirname(__file__))
ELEVATIONS_FILE = os.path.join(sys.path[0], 'assets', 'wsc_elevation.csv')

from application import dash_app, app

TEST_DATA = pd.read_csv(ELEVATIONS_FILE, usecols=['Distance', 'Elevation (m)'], index_col='Distance', squeeze=True)

map = dbc.Col([
    dbc.Card([
        dbc.CardBody([
            dl.Map(
                center=[39, -98],       
                zoom = 4,
                children = [dl.TileLayer(), dl.Marker(position=[39, -98])],
            style={'width': '100%', 'height': '500px'})
        ])
    ], className='pretty_container')
])

graph1 = dbc.Col([
    dbc.Card([
        dbc.CardBody([
            html.H5("Sun Incidence", className="card-title"),
            dcc.Graph()
        ])
    ], className='pretty_container')
])

graph2 = dbc.Col([
    dbc.Card([
        dbc.CardBody([
            html.H5("Weather", className="card-title"),
            dcc.Graph()
        ])
    ], className='pretty_container')
])

graph3 = dbc.Col([
    dbc.Card([
        dbc.CardBody([
            dcc.Graph(
                figure= {
                    'data': [{'x': TEST_DATA.index, 'y': TEST_DATA.values}],
                    'layout': {
                        'title': 'Upcoming Elevation', 
                        'xaxis': {'title': {'text': 'Distance'}},
                        'yaxis': {'title': {'text': 'Elevation (m)'}}
                    }
                }
            )
        ])
    ], className='pretty_container')
])

layout = html.Div([
    dbc.Row([map], no_gutters=True),
    dbc.Row([graph1, graph2], no_gutters=True),
    dbc.Row([graph3], no_gutters=True)
])