import dash
from dash.dependencies import Output
import dash_leaflet as dl
import pandas
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np

csv = pandas.read_csv('./ASC2021_draft.csv', names=[0,1])
csv_list = csv.values.tolist()
markers = [dl.Marker(position=pos, id="marker{}".format(i), draggable=True) for i, pos in enumerate(csv_list)]
app = dash.Dash()


app.layout = html.Div([
    html.Div(dl.Map([dl.TileLayer(), dl.LayerGroup(id="layer"), *markers],
                             zoom=4, center=(csv_list[0][0], csv_list[0][1])),
                      style={'width': '60%', 'height': '50vh', 'margin': "auto", "display": "block"}),
    html.Div(id='clickdata')
])

@app.callback(Output("layer", "children"),
            [Input(marker.id, "position") for marker in markers])
def marker_click(*args):
    a = np.asarray(args)
    np.savetxt("./output.csv", a, delimiter=',')
    return [dl.Polyline(positions=args)]


if __name__ == '__main__':
    app.run_server()