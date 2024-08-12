import json
import pytest
from fastapi import status
from httpx import AsyncClient

from app.apps.dykes import models

# Test get readings
async def test_get_readings(client: AsyncClient):
    response = await client.get(f"/api/readings/")
    assert response.status_code == status.HTTP_200_OK
    content = json.loads(response.read())
    assert content['readings'] is not None 

async def test_filter_readings_by_dates(client:AsyncClient):
    """
    Example of http query url:
    http://127.0.0.1:8000/api/readings/?startDate=2024-08-01&endDate=2024-08-31&sensorId=1

    """
    from dashboard.geodykes_dash.data import fetch_readings
    end_date = "2024-08-06"
    start_date="2024-07-10"

    response = await fetch_readings(start_date=start_date, end_date=end_date)
    assert response.status_code == status.HTTP_200_OK
    
async def test_filter_by_sensor_name(client:AsyncClient):
    pass