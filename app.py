import dash
from dash import dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import requests
import io

# URL for the Key file
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSsJHa45XRLX8b4IgEcfpM2-xPuOlpnk6Q6yBquQDzDrKncYt6HhGFqUQ_kQRujGO_uf_MxlJ6CSG1i/pub?output=csv"

# Load Data
def get_data(url):
    response = requests.get(url).content
    df = pd.read_csv(io.StringIO(response.decode('utf-8')))
    # Clean up empty columns if necessary
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df

df = get_data(CSV_URL)

# App Setup
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Sales Key/Mapping Dashboard", className="text-center my-4"))
    ]),
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                page_size=20,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '5px'},
                style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'}
            )
        ])
    ])
], fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)
