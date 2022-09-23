import requests
from twilio.rest import Client
import config


twilio_account_sid = config.TWILIO_ACCOUNT_SID
twilio_auth_token = config.TWILIO_AUTH_TOKEN
twilio_phone_num = config.TWILIO_PHONE_NUM
num_text_to = config.NUM_TEXT_TO

WEATHER_OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
WEATHER_API_KEY = config.WEATHER_API_KEY
MY_LAT = 51.0501
MY_LON = -114.0853

weather_params = {
    "lat": MY_LAT,
    "lon": MY_LON,
    "exclude": "current,minutely,daily",
    "appid": WEATHER_API_KEY
}

response = requests.get(url=WEATHER_OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

weather_slice = weather_data["hourly"][0:12]
weather_codes_for_12hours = [hour_data["weather"][0]["id"] for hour_data in weather_slice]

will_rain = False
for code in weather_codes_for_12hours:
    if int(code) < 600:
        will_rain = True

if will_rain:
    client = Client(twilio_account_sid, twilio_auth_token)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☔️",
        from_=twilio_phone_num,
        to=num_text_to
    )
    print(message.status)
    print(message.sid)