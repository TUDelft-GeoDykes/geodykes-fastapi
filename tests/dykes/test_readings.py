import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_readings(client: AsyncClient):
    response = client.get("/api/readings/")
    assert response.status_code == 200
    assert "readings" in response.json()

@pytest.mark.asyncio
async def test_post_reading(client: AsyncClient):
    payload_example = {
        "crossection": "Crossection 4-2",
        "sensor_id": 2,
        "sensor_name": "Sensor 2",
        "sensor_is_active": True,
        "location_in_topology": [
            25.742971005268636,
            39.978211040045174
        ],
        "unit": "Unit 1",
        "value": 61,
        "time": "2024-08-03T11:48:14.460881"
    }

    response = client.post("/api/readings/", json=payload_example)

    assert response.status_code == 201  # Expecting a 201 Created status code
    data = response.json()
    assert data["crossection"] == payload_example["crossection"]
    assert data["value"] == payload_example["value"]
