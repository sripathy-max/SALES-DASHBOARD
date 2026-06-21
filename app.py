Skip to content
sripathy-max
SALES-DASHBOARD
Repository navigation
Code
Issues
Pull requests
Actions
Projects
Wiki
Security and quality
Insights
Settings
Files
Go to file
t
T
.gitignore
Procfile
README.md
app.py
requirements.txt
SALES-DASHBOARD
/
app.py
in
main

Edit

Preview
Indent mode

Spaces
Indent size

4
Line wrap mode

No wrap
Editing app.py file contents
  1
  2
  3
  4
  5
  6
  7
  8
  9
 10
 11
 12
 13
 14
 15
 16
 17
 18
 19
 20
 21
 22
 23
 24
 25
 26
 27
 28
 29
 30
 31
 32
 33
 34
 35
 36
import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from datetime import date

# --- Configuration ---
# Replace this URL if you need to point to a different CSV source
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSsJHa45XRLX8b4IgEcfpM2-xPuOlpnk6Q6yBquQDzDrKncYt6HhGFqUQ_kQRujGO_uf_MxlJ6CSG1i/pub?output=csv"

HQ_COL_MAP = {"DGM": "DGM", "ZBM": "State", "ABM": "ABM Name", "MR": "HQ Name"}

# Styling
STYLE_RED = {'backgroundColor': '#FF0000', 'color': 'white', 'border': 'none', 'borderRadius': '5px'}
STYLE_YEL = {'backgroundColor': '#FFFF00', 'color': 'black', 'border': 'none', 'borderRadius': '5px'}
STYLE_BLU = {'backgroundColor': '#0000FF', 'color': 'white', 'border': 'none', 'borderRadius': '5px'}
STYLE_GRN = {'backgroundColor': '#28a745', 'color': 'white', 'border': 'none', 'borderRadius': '5px'}

# --- Data Loading ---
def get_data(url):
    df = pd.read_csv(url)
    id_cols = ["ZBM Name", "ABM Name", "HQ Name", "Item Cd", "Item Name", "State", "Mother Brand", "DGM"]
    date_cols = [c for c in df.columns if c not in id_cols]
    df_long = df.melt(id_vars=id_cols, value_vars=date_cols, var_name="Date", value_name="Units")
    df_long['Date'] = pd.to_datetime(df_long['Date'], errors='coerce')
    df_long['Units'] = pd.to_numeric(df_long['Units'], errors='coerce').fillna(0)
    return df_long

# Initialize Data
df = get_data(CSV_URL)

# --- App Setup ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # REQUIRED for Render/Gunicorn

Use Control + Shift + m to toggle the tab key moving focus. Alternatively, use esc then tab to move to the next interactive element on the page.
