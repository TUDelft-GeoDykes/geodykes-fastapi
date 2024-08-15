import dash
from dash import dash_table, html
import json
import dash_bootstrap_components as dbc
import requests
from services.manager import data_fetcher


# Fetch readings data
client = data_fetcher.api_client
fetch_readings = data_fetcher.fetch_readings
readings_data = fetch_readings(api_client=client)
readings_data = readings_data.readings
readings_data = [reading.to_dict() for reading in readings_data]

# Process readings data
for item in readings_data:
    item['location_x'], item['location_y'] = item['location_in_topology']
    item['sensor_location'] = f"{item['sensor_location'][0]}, {item['sensor_location'][1]}"  # Convert list to string
    del item['location_in_topology']
    del item['id']

# Get column names for the DataTable
column_names = readings_data[0].keys() if readings_data else []

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
                    columns=[{"name": col_name, "id": col_name} for col_name in column_names],
                    data=readings_data,
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
