import telebot
from flask import Flask, request
from config import BOT_TOKEN
from weather import get_weather
from currency import get_currency
from scheduler import start_scheduler, subscribe_user, advices
import random
import os

bot = telebot.TeleBot(BOT_TOKEN)
start_scheduler(bot)

app = Flask(__name__)

# === BOT HANDLERS ===
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Assalomu alaykum, {message.from_user.first_name}!\n"
                                      f"Men sizga quyidagi xizmatlarni taklif qilaman:\n"
                                      f"/help yozib batafsil bilib oling.")
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

# === WEBHOOK ROUTE ===
@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

# === PING ROUTE (ixtiyoriy) ===
@app.route('/')
def index():
    return 'Bot ishlayapti!', 200

# === START APP ===
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    bot.remove_webhook()
    bot.set_webhook(url=f"https://helperbot-gks4.onrender.com/{BOT_TOKEN}")
    app.run(host='0.0.0.0', port=port)
