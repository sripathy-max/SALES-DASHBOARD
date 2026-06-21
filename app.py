import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import sys

# Configuration
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSsJHa45XRLX8b4IgEcfpM2-xPuOlpnk6Q6yBquQDzDrKncYt6HhGFqUQ_kQRujGO_uf_MxlJ6CSG1i/pub?output=csv"

HQ_COL_MAP = {"DGM": "DGM", "ZBM": "State", "ABM": "ABM Name", "MR": "HQ Name"}

def get_data(url):
    try:
        df = pd.read_csv(url)
        print("CSV loaded successfully.")
        print("Columns found in CSV:", list(df.columns)) # THIS WILL SHOW IN RENDER LOGS
        
        # We need these columns to exist
        required_cols = ["ZBM Name", "ABM Name", "HQ Name", "Item Cd", "Item Name", "State", "Mother Brand", "DGM"]
        
        # Check if any required columns are missing
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            print(f"CRITICAL ERROR: The following columns are missing in your CSV: {missing}")
            sys.exit(1) # This forces the app to stop so you see the error in logs

        date_cols = [c for c in df.columns if c not in required_cols]
        df_long = df.melt(id_vars=required_cols, value_vars=date_cols, var_name="Date", value_name="Units")
        df_long['Date'] = pd.to_datetime(df_long['Date'], errors='coerce')
        df_long['Units'] = pd.to_numeric(df_long['Units'], errors='coerce').fillna(0)
        return df_long
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)

print("Starting Data Load...")
# Note: Since you are using the same link for both, we load it twice
df_curr = get_data(URL)
df_prev = get_data(URL)
print("Data load complete. Launching app...")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# ... (Keep your existing layout and callbacks here) ...
# (Ensure your layout and callbacks are pasted below this point)
