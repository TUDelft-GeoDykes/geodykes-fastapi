import dash
import dash_table
import dash_bootstrap_components as dbc
import requests

# Define your FastAPI endpoint
API_BASE_URL = "http://localhost:8000/api/readings"

# Fetch the data from the FastAPI endpoint
def fetch_readings():
    response = requests.get(API_BASE_URL, timeout=10)  
    response.raise_for_status()
    return response.json()["items"]

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Fetch readings data
readings_data = fetch_readings()

# Process readings data
for item in readings_data:
    item['location_x'], item['location_y'] = item['location_in_topology']
    del item['location_in_topology']
    del item['id']

# Layout of the Dash app
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dash.html.H1("Sensor Readings Table", className="text-center"),
                width=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                dash_table.DataTable(
                    id="readings-table",
                    columns=[{"name": i, "id": i} for i in readings_data[0].keys()],
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
