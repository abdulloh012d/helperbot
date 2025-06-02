import requests
from config import WEATHER_API_KEY

def get_weather(city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric&lang=uz"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        feels = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        return (
            f"🌤 Ob-havo: {desc.capitalize()}\n"
            f"🌡 Harorat: {temp}°C (his qilinadi: {feels}°C)\n"
            f"💧 Namlik: {humidity}%\n"
            f"💨 Shamol tezligi: {wind} m/s"
        )
    else:
        return "⚠ Ob-havo ma'lumotini olishda xatolik yuz berdi."
