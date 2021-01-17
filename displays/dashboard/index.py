import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from application import dash_app, app
import charge
import route
import other

navbar = dbc.Navbar([
    html.Img(src=dash_app.get_asset_url('logo.png'), className='index-logo')
], color='white', className='index-navbar')

tabs = dcc.Tabs(
    id='index-tabs', 
    mobile_breakpoint=2000,
    vertical=True, 
    value='index-tab-charge',
    children=[

        dcc.Tab(
            label='Current State of Charge', value='index-tab-charge', 
            className='index-tab',
            selected_className='index-tab--selected'
        ),

        dcc.Tab(
            label='Route Map', value='index-tab-route',
            className='index-tab',
            selected_className='index-tab--selected'
        ),

        dcc.Tab(
            label='Other', value='index-tab-other',
            className='index-tab',
            selected_className='index-tab--selected'
        ),
    ]
)

dash_app.layout = html.Div([
    navbar, 
    dbc.Row([
        dbc.Col([tabs], width=2, className='index-tabs'),
        dbc.Col([html.Div(id='content', style={'margin-right': '30px'})], width=10)
    ], no_gutters=True)
])

@dash_app.callback(
    Output('content', 'children'),
    [Input('index-tabs', 'value')]
)
def render_content(tab):
    # purpose: direct to other files depending on the tab
    # params: tab (str) - the selected tab   
    # returns the layout of that tab    

    if tab == 'index-tab-charge':
        return charge.layout
    elif tab == 'index-tab-route':
        return route.layout
    elif tab == 'index-tab-other':
        return other.layout


if __name__ == '__main__':
    dash_app.run_server(debug=True, use_reloader=False)