import dash
import dash_bootstrap_components as dbc
import dash_table
import requests
import os

# Define the base URL for the FastAPI endpoint
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")  # Default to localhost for local development
print(f"API_BASE_URL: {API_BASE_URL}")

BASE_PATH = os.getenv("BASE_PATH", "/dashboard/")

try:
    response = requests.get(f"{API_BASE_URL}/api/readings")
    readings_data = response.json()  # Or handle appropriately
except requests.exceptions.RequestException as e:
    print(f"Error fetching readings: {e}")
    readings_data = None

# Fetch the data from the FastAPI endpoint
def fetch_readings():
    try:
        response = requests.get(f"{API_BASE_URL}/api/readings", timeout=10)
        response.raise_for_status()
        data = response.json()

        # Check if "readings" exists in the response and is not empty
        if "readings" not in data or not data["readings"]:
            raise ValueError("No readings available in the response.")

        return data["readings"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching readings: {e}")
        return None
    except ValueError as e:
        print(f"Error: {e}")
        return None

# Initialize the Dash app
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                requests_pathname_prefix=BASE_PATH)

# Fetch readings data
readings_data = fetch_readings()

# Process readings data
for item in readings_data:
    item["location_x"], item["location_y"] = item["location_in_topology"]
    del item["location_in_topology"]
    del item["id"]

# Layout of the Dash app
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dash.html.H1("Sensor Readings Table", className="text-center"),
                width=12,
            ),
        ),
        dbc.Row(
            dbc.Col(
                dash_table.DataTable(
                    id="readings-table",
                    columns=[{"name": i, "id": i} for i in readings_data[0]],
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
            ),
        ),
    ],
    fluid=True,
)

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)

