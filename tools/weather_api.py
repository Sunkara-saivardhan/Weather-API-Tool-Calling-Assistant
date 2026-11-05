import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key= os.getenv("WEATHER_API")

def get_weather(city:str):
    if not api_key:
        return {"error":"api key is messing"}
    
    url="https://api.openweathermap.org/data/2.5/weather"
    
    params={
        "q":city,
        "appid":api_key,
        "units": "metric"
    }
    
    try:
        response=requests.get(url,params=params, timeout=10)
        data=response.json()
        
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        }
    except requests.RequestException as error:
        return {"error": str(error)}