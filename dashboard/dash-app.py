# sensor_dashboard/frontend/dashboard.py

import dash
import dash_table
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import requests
from dash.dash_table.Format import Group

# Define your FastAPI endpoint
API_BASE_URL = "http://localhost:8000/api/readings"

# Fetch the data from the FastAPI endpoint
def fetch_readings():
    response = requests.get(API_BASE_URL)
    response.raise_for_status()
    return response.json()["items"]

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Fetch readings data
readings_data = fetch_readings()

# Convert to DataFrame for easier manipulation
df = pd.DataFrame(readings_data)

# Assuming df is your DataFrame
df[['location_x', 'location_y']] = pd.DataFrame(df['location_in_topology'].tolist(), index=df.index)

# Drop the original location_in_topology column if it's no longer needed
df.drop('location_in_topology', axis=1, inplace=True)

df.drop('id', axis=1, inplace=True)

# Layout of the Dash app
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Sensor Readings Table", className="text-center"),
                width=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                dash_table.DataTable(
                    id="readings-table",
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict("records"),
                    style_table={"overflowX": "auto"},
                    style_cell={
                        "height": "auto",
                        "minWidth": "150px",
                        "width": "150px",
                        "maxWidth": "150px",
                        "whiteSpace": "normal",
                    },
                    style_header={
                        "backgroundColor": "rgb(230, 230, 230)",
                        "fontWeight": "bold",
                    },
                ),
                width=12,
            )
        ),
    ],
    fluid=True,
)

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
