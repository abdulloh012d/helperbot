import os
import random
import requests
from flask import Flask, request
import telebot
from apscheduler.schedulers.background import BackgroundScheduler

# --- Konfiguratsiya ---
BOT_TOKEN = os.environ.get('7206608966:AAFm0bwzbimunNiWTe7N-RwpVAlTsHU490E')
WEATHER_API_KEY = "7126126775ed37f9825f5bddca18c4a9"
EXCHANGE_API_KEY = "283fb41ef42d47be8ca704d2"

# --- Bot va Flask ilovasi ---
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- Foydali maslahatlar ---
advices = [
    "Erta tur, kuning barakali bo'ladi.",
    "Reja tuz, kuningni boshqarish osonlashadi.",
    "Kichik maqsadlarga e’tibor ber, ular katta natijaga olib keladi.",
    "Yaxshi odatlarni shakllantir, ular seni yuksaltiradi.",
    "Muntazam tanaffus qil, bu samaradorlikni oshiradi.",
    "Tinch muhitda ishlashga harakat qil.",
    "Kundalik qilayotgan ishlaringni yozib bor.",
    "Yaxshi niyat bilan boshlagan ish barakali bo'ladi.",
    "Ilm izlashdan to‘xtama.",
    "Kitob o‘qish fikrlashni kengaytiradi.",
    "Yangi narsa o‘rganishga vaqt ajrat.",
    "Harakat qilish — muvaffaqiyat kaliti.",
    "Shaxsiy rivojlanishga vaqt ajrat.",
    "Salomatlikka e’tibor ber, u eng katta boylik.",
    "Yaxshi uxla, yaxshi dam olgan aql yaxshi ishlaydi.",
    "Kam gapir, ko‘p tingla.",
    "Har bir kunni qadrlashni o‘rgan.",
    "Ishni kechiktirma, kechikkan ish qiyin bo‘ladi.",
    "Kamida 10 daqiqa jismoniy mashq qil.",
    "Tashvishlarga emas, yechimlarga e’tibor ber.",
    "O’zingga ishongan holda harakat qil.",
    "Qanday bo‘lmasin, kuningdan minnatdor bo‘l.",
    "Yordam so‘rash — zaiflik emas, bu aqllilik.",
    "Doimo samimiy bo‘l.",
    "O‘rganayotganingni boshqalarga o‘rgat, bu mustahkamlashga yordam beradi.",
    "Do‘stlaring bilan vaqt o‘tkaz, lekin yolg‘izlikdan ham qo‘rqma.",
    "Ijobiy fikrlashni odat qil.",
    "Ishni boshlash — yarim muvaffaqiyatdir.",
    "Har kuni kamida 1 yangi so‘z o‘rgan.",
    "Suv ichishni esdan chiqarmang.",
    "Biror narsani bilmasang, izlan.",
    "O‘z-o‘zini tahlil qilish odatini rivojlantir.",
    "Hech qachon bahona qilma.",
    "Tezda emas, to‘g‘ri yondashish muhim.",
    "O‘z ustingda ishlashni to‘xtatma.",
    "Yomon odatlarni asta-sekin tark et.",
    "O‘zingni boshqalar bilan solishtirma, faqat o‘zing bilan solishtir.",
    "Ko‘proq tabassum qil, kayfiyatga ijobiy ta’sir qiladi.",
    "Kechirimli bo‘l, yuraging yengillashadi.",
    "Xatolar ustida ishlash — rivojlanishdir.",
    "Yaxshi niyat bilan harakat qil.",
    "Bugun qilgan kichik yutuqlaringni nishonla.",
    "Sabrli bo‘l, natijalar vaqt talab qiladi.",
    "Yolg‘on gapirmaslikni odat qil.",
    "Xursand bo‘lishga sabab top.",
    "Vaqtingni foydali ishga sarfla.",
    "Hech narsa qilmay o‘tirishdan ko‘ra, kichik ishni qilgan afzal.",
    "O‘zingga sodiq bo‘l.",
    "Yuqori maqsad qo‘y, unga yetish uchun reja tuz.",
    "Har bir kun — yangi imkoniyatdir.",
    "Harakat — eng yaxshi motivatsiya."
]


subscribed_users = set()

# --- Ob-havo funksiyasi ---
def get_weather(city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric&lang=uz"
    try:
        response = requests.get(url)
        response.raise_for_status()
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
    except Exception:
        return "⚠ Ob-havo ma'lumotini olishda xatolik yuz berdi."

# --- Valyuta kurslari ---
def get_currency():
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/USD"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        if data['result'] != 'success':
            return "⚠ Valyuta ma'lumotlarini olishda xatolik yuz berdi."

        rates = data['conversion_rates']
        eur = rates.get('EUR')
        rub = rates.get('RUB')

        return (
            f"💵 USD: 1 USD (bazaviy valyuta)\n"
            f"💶 EUR: {eur} USD ga teng\n"
            f"🇷🇺 RUB: {rub} USD ga teng"
        )
    except Exception:
        return "⚠ Valyuta kurslarini olishda tarmoq xatosi yuz berdi."

# --- Foydalanuvchini obuna qilish ---
def subscribe_user(chat_id: int):
    subscribed_users.add(chat_id)

# --- Maslahatlarni yuborish uchun scheduler ---
def start_scheduler(bot):
    scheduler = BackgroundScheduler()

    def send_advice():
        for chat_id in subscribed_users:
            advice = random.choice(advices)
            bot.send_message(chat_id, f"📌 Bugungi maslahat: {advice}")

    scheduler.add_job(send_advice, 'cron', hour=9, minute=0)
    scheduler.start()

# --- Bot buyruqlar ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        f"Assalomu alaykum, {message.from_user.first_name}!\n"
        f"Men sizga quyidagi xizmatlarni taklif qilaman:\n"
        f"/help yozib batafsil bilib oling."
    )
    subscribe_user(message.chat.id)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "/start - Botni ishga tushurish\n"
        "/help - Yordam\n"
        "/weather - Ob-havo\n"
        "/currency - Valyuta kurslari\n"
        "/advice - Foydali maslahat\n"
    )
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['weather'])
def weather_handler(message):
    msg = bot.send_message(message.chat.id, "Qaysi shahar ob-havo ma’lumotini bilmoqchisiz?")
    bot.register_next_step_handler(msg, send_weather)

def send_weather(message):
    city = message.text
    result = get_weather(city)
    bot.send_message(message.chat.id, result)

@bot.message_handler(commands=['currency'])
def currency_handler(message):
    bot.send_message(message.chat.id, get_currency())

@bot.message_handler(commands=['advice'])
def advice_handler(message):
    bot.send_message(message.chat.id, f"📌 Maslahat: {random.choice(advices)}")

@bot.message_handler(func=lambda m: True)
def unknown(message):
    bot.send_message(message.chat.id, "Kechirasiz, bu buyruqni tushunmadim. /help ni yozing.")

# --- Webhook route ---
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

# --- Ping route ---
@app.route('/')
def index():
    return 'Bot ishlayapti!', 200

# --- Asosiy ishga tushirish ---
if __name__ == '__main__':
    start_scheduler(bot)
    port = int(os.environ.get('PORT', 5000))
    bot.remove_webhook()
    bot.set_webhook(url=f"https://helperbot-gks4.onrender.com/{BOT_TOKEN}")
    app.run(host='0.0.0.0', port=port)
