import requests
from twilio.rest import Client
# from dotenv import load_dotenv (only for local testing)
import os

# Load environment variables
# load_dotenv()(only for local testing)

# CONSTANTS

# OpenWeatherMap API key
api_key = os.environ.get("API_KEY")
# Your Account SID from twilio.com/console
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
# Your Auth Token from twilio.com/console
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
# Maracaibo coordinates
latitude = 10.642707
longitude = -71.612534


# API request for 5 days / 3 hour forecast data
response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}")
response.raise_for_status()
weather_data = response.json()

# Extracting data from the API response
# Create a list of the condition codes for the next 12 hours
next_12_hours_list = [weather_data["list"][i]["weather"][0]["id"] for i in range(4)]

# Send a message using Twilio if the weather id is under 700 in the next 12 hours
if any(int(weather_id) < 700 for weather_id in next_12_hours_list):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella! ☔️",
        from_=os.environ.get("SENDER_NUMBER"),
        to=os.environ.get("RECIPIENT_NUMBER")
    )