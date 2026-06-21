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

today = date.today()
month_start = date(today.year, today.month, 1)

# --- Layout ---
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.Label("Brand"), dcc.Dropdown(id='brand-dropdown', options=[{'label': b, 'value': b} for b in sorted(df['Mother Brand'].unique())], value='SHY NM')], width=4),
        dbc.Col([html.Label("HQ"), dcc.Dropdown(id='hq-dropdown', options=['DGM', 'ZBM', 'ABM', 'MR'], placeholder="Select HQ", searchable=False)], width=3),
        dbc.Col([
            html.Div([html.Label("ZBM / ABM / HQ"), html.Span(id='multi-status', style={'color': 'red', 'marginLeft': '10px', 'fontSize': '12px', 'fontWeight': 'bold'})]),
            dcc.Dropdown(id='filter-dropdown', placeholder="Select...", multi=True)
        ], width=5),
    ], className="mb-2"),

    dbc.Row([
        dbc.Col([html.Label("Start Date"), dcc.DatePickerSingle(id='start-date', date=month_start, style={'width': '100%'})], width=3),
        dbc.Col([html.Label("End Date"), dcc.DatePickerSingle(id='end-date', date=today, style={'width': '100%'})], width=3),
    ], className="mb-3", align="end"),

    dbc.Row([dbc.Col([dcc.Graph(id='line-chart', style={'height': '400px'})], width=12)]),
    dbc.Row([dbc.Col([html.Div(id='table-container')], width=12)]),

    dbc.Row([
        dbc.Col(dbc.Button("Trend (off)", id="btn-trend", style=STYLE_RED, className="w-100"), width=2),
        dbc.Col(dbc.Button("Concern", id="btn-concern", style=STYLE_RED, className="w-100"), width=2),
        dbc.Col(dbc.Button("Tgt vs Ach", id="btn-tgt", style=STYLE_RED, className="w-100"), width=2),
        dbc.Col(dbc.Button("Other", id="btn-other", style=STYLE_RED, className="w-100"), width=2),
        dbc.Col(dbc.Button("Send Message", id="btn-send", style=STYLE_GRN, className="w-100"), width=2),
    ], className="mt-3 g-3", justify="center")
], fluid=True, style={'height': '100vh', 'padding': '15px'})

# --- Callbacks ---
@app.callback(
    [Output('filter-dropdown', 'options'), Output('multi-status', 'children')],
    [Input('hq-dropdown', 'value'), Input('filter-dropdown', 'value')]
)
def update_filter_dropdown(selected_hq, selected_filters):
    col_name = HQ_COL_MAP.get(selected_hq)
    options = []
    if col_name and col_name in df.columns:
        opts = df[col_name].dropna().unique()
        options = [{'label': str(i), 'value': i} for i in sorted(opts)]
    status = "*Multiple selected" if selected_filters and len(selected_filters) > 1 else ""
    return options, status

@app.callback(
    [Output('line-chart', 'figure'), Output('table-container', 'children')],
    [Input('brand-dropdown', 'value'), Input('hq-dropdown', 'value'), 
     Input('filter-dropdown', 'value'), Input('start-date', 'date'), Input('end-date', 'date')]
)
def update_graph_and_table(brand, hq, filters, start, end):
    col_name = HQ_COL_MAP.get(hq)
    mask = (df['Mother Brand'] == brand) & (df['Date'] >= start) & (df['Date'] <= end)
    if filters and col_name: mask &= df[col_name].isin(filters)

    filtered_df = df.loc[mask].groupby('Date')['Units'].sum().reset_index().sort_values('Date')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Units'], mode='lines+markers', name='Units'))
    fig.update_layout(hovermode="x unified", margin=dict(l=20, r=20, t=30, b=20))

    table = None
    if (pd.to_datetime(end) - pd.to_datetime(start)).days <= 31:
        pivot_data = filtered_df.copy()
        pivot_data['Date_Str'] = pivot_data['Date'].dt.strftime('%d-%m')
        table = dash_table.DataTable(
            data=[dict(zip(pivot_data['Date_Str'], pivot_data['Units']))],
            columns=[{"name": col, "id": col} for col in pivot_data['Date_Str']],
            style_table={'overflowX': 'auto', 'marginTop': '20px'},
            style_cell={'textAlign': 'center', 'minWidth': '40px', 'fontSize': '12px'}
        )
    
    return fig, table

# Main
if __name__ == '__main__':
    app.run_server(debug=False)
