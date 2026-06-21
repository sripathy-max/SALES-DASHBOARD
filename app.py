import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from datetime import date

# URLs - Ensure these point to your correct CSV files
URL_26_27 = "YOUR_URL_FOR_26_27" 
URL_25_26 = "YOUR_URL_FOR_25_26"

HQ_COL_MAP = {"DGM": "DGM", "ZBM": "State", "ABM": "ABM Name", "MR": "HQ Name"}
STYLE_RED = {'backgroundColor': '#FF0000', 'color': 'white', 'border': 'none', 'borderRadius': '5px'}
STYLE_YEL = {'backgroundColor': '#FFFF00', 'color': 'black', 'border': 'none', 'borderRadius': '5px'}
STYLE_BLU = {'backgroundColor': '#0000FF', 'color': 'white', 'border': 'none', 'borderRadius': '5px'}
STYLE_GRN = {'backgroundColor': '#28a745', 'color': 'white', 'border': 'none', 'borderRadius': '5px'}

def get_data(url):
    df = pd.read_csv(url)
    id_cols = ["ZBM Name", "ABM Name", "HQ Name", "Item Cd", "Item Name", "State", "Mother Brand", "DGM"]
    date_cols = [c for c in df.columns if c not in id_cols]
    df_long = df.melt(id_vars=id_cols, value_vars=date_cols, var_name="Date", value_name="Units")
    df_long['Date'] = pd.to_datetime(df_long['Date'], errors='coerce')
    df_long['Units'] = pd.to_numeric(df_long['Units'], errors='coerce').fillna(0)
    return df_long

df_curr = get_data(URL_26_27)
df_prev = get_data(URL_25_26)

today = date.today()
month_start = date(today.year, today.month, 1)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Crucial for Gunicorn

app.layout = dbc.Container([
    # ... (Keep your layout exactly as you had it) ...
], fluid=True, style={'height': '100vh', 'padding': '15px'})

# ... (Keep your callbacks exactly as you had them) ...

# Remove the 'if __name__ == "__main__":' block entirely or replace with just the app
