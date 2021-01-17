import dash
import dash_bootstrap_components as dbc

dash_app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
dash_app.title = "Strategy"
app = dash_app.server 