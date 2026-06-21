import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import sys

# --- Configuration ---
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSsJHa45XRLX8b4IgEcfpM2-xPuOlpnk6Q6yBquQDzDrKncYt6HhGFqUQ_kQRujGO_uf_MxlJ6CSG1i/pub?output=csv"

# --- Data Loading ---
def get_data(url):
    print("Attempting to load CSV...")
    try:
        df = pd.read_csv(url)
        print(f"Columns found in CSV: {list(df.columns)}") # <--- THIS WILL FIX YOUR GUESSWORK
        
        id_cols = ["ZBM Name", "ABM Name", "HQ Name", "Item Cd", "Item Name", "State", "Mother Brand", "DGM"]
        
        # Verify columns exist
        missing = [c for c in id_cols if c not in df.columns]
        if missing:
            print(f"CRITICAL ERROR: Columns missing: {missing}")
            sys.exit(1) # Stops the app if columns are wrong

        date_cols = [c for c in df.columns if c not in id_cols]
        df_long = df.melt(id_vars=id_cols, value_vars=date_cols, var_name="Date", value_name="Units")
        df_long['Date'] = pd.to_datetime(df_long['Date'], errors='coerce')
        df_long['Units'] = pd.to_numeric(df_long['Units'], errors='coerce').fillna(0)
        return df_long
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)

# Initialize Data
df = get_data(CSV_URL)

# --- App Setup ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server 

# [Continue with your layout and callbacks here...]
