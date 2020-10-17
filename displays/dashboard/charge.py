import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from application import dash_app, app

graph1 = dbc.Col([
    dbc.Card([
        dbc.CardBody([
            html.H5("Percentage vs. Distance Travelled", className="card-title"),
            dcc.Graph()
        ])
    ], className='pretty_container')
])

graph2 = dbc.Col([
    dbc.Card([
        dbc.CardBody([
            html.H5("Remaining Kilometers at Current Average Speed", className="card-title"),
        ])
    ], className='pretty_container')
])

layout = dbc.Row([graph1, graph2], no_gutters=True)