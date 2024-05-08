import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# CONSTANTS

# OpenWeatherMap API key
api_key = os.getenv("API_KEY")
# Your Account SID from twilio.com/console
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
# Your Auth Token from twilio.com/console
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
# Graz coordinates
latitude = 47.070713
longitude = 15.439504


# API request for 5 days / 3 hour forecast data
response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}")
response.raise_for_status()
weather_data = response.json()

# Extracting data
# Print out the weather code for the first 3 hour period
print(weather_data["list"][0]["weather"][0]["id"])

# Create a list of the condition codes for the next 12 hours
next_12_hours_list = [weather_data["list"][i]["weather"][0]["id"] for i in range(4)]
print(next_12_hours_list)

# Print a message if the weather id is under 700 in the next 12 hours
if any(int(weather_id) < 700 for weather_id in next_12_hours_list):
    # Send a message using Twilio
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella! ☔️",
        from_=os.getenv("SENDER_NUMBER"),
        to=os.getenv("RECIPIENT_NUMBER")
    )

    print(message.status)
else:
    print("Enjoy the day with free hands!")