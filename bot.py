import telebot
import requests
from flask import Flask, request

# Tokenlar
BOT_TOKEN = "7206608966:AAGBbo4-PWPF_cqIM_QOLDUOFwY5a0zP4-4"
WEATHER_TOKEN = "7126126775ed37f9825f5bddca18c4a9"
EXCHANGE_TOKEN = "283fb41ef42d47be8ca704d2"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# /start komandasi
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Assalomu alaykum! Quyidagi komandalarni sinab ko‘ring:\n"
                                      "/weather <shahar nomi>\n"
                                      "/exchange <valyuta kodi>\n"
                                      "/advice")

# /weather <shahar>
@bot.message_handler(commands=['weather'])
def weather_handler(message):
    try:
        city = message.text.split(" ", 1)[1]
        url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_TOKEN}&q={city}"
        res = requests.get(url).json()

        if "error" in res:
            bot.send_message(message.chat.id, "Shahar topilmadi.")
            return

        temp = res["current"]["temp_c"]
        condition = res["current"]["condition"]["text"]
        bot.send_message(message.chat.id, f"{city} shahrida hozirgi harorat: {temp}°C, {condition.lower()}.")
    except:
        bot.send_message(message.chat.id, "Iltimos, shahar nomini kiriting: /weather Toshkent")

# /exchange <valyuta>
@bot.message_handler(commands=['exchange'])
def exchange_handler(message):
    try:
        currency = message.text.split(" ", 1)[1].upper()
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_TOKEN}/latest/USD"
        res = requests.get(url).json()

        if res["result"] != "success":
            bot.send_message(message.chat.id, "Valyuta ma'lumotlarini olishda xatolik yuz berdi.")
            return

        rate = res["conversion_rates"].get(currency)
        if rate:
            bot.send_message(message.chat.id, f"1 USD = {rate} {currency}")
        else:
            bot.send_message(message.chat.id, f"{currency} valyutasi topilmadi.")
    except:
        bot.send_message(message.chat.id, "Iltimos, valyuta kodini kiriting: /exchange EUR")

# ✅ /advice komandasi
@bot.message_handler(commands=['advice'])
def advice_handler(message):
    try:
        res = requests.get("https://api.adviceslip.com/advice").json()
        advice = res['slip']['advice']
        bot.send_message(message.chat.id, f"📌 Maslahat: {advice}")
    except:
        bot.send_message(message.chat.id, "Maslahat olishda xatolik yuz berdi. Keyinroq urinib ko‘ring.")

# Webhook
@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return '', 200
    else:
        return "Bot ishlayapti!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
