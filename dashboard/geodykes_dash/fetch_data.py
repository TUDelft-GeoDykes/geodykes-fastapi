'''
API client requests
'''
import httpx
import asyncio
import os

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000/api")

async def fetch_readings(start_date:str, end_date: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/readings/",
            params={
                "startDate": start_date,
                "endDate": end_date,
                # "sensorId": sensorId
            }
        )
        return response