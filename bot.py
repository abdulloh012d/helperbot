import telebot
import requests
import random
from flask import Flask, request

BOT_TOKEN = "7206608966:AAGBbo4-PWPF_cqIM_QOLDUOFwY5a0zP4-4"
WEATHER_API_KEY = "7126126775ed37f9825f5bddca18c4a9"
EXCHANGE_API_KEY = "283fb41ef42d47be8ca704d2"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

uzbek_advices = [
    "Harakat – omad kaliti.",
    "Bugungi ishni ertaga qoldirma.",
    "Sabr – barcha muammolarning yechimi.",
    "Kitob o‘qish – aqlni o‘stiradi.",
    "Salomatlik – eng katta boylik.",
    "Do‘stni darda, dushmanni zarba bil.",
    "Xatodan qo‘rqma – undan saboq ol.",
    "Mehnat qilgan kishi hech qachon yutqazmaydi.",
    "Ko‘p tingla, kam gapir.",
    "Har bir kun – yangi imkoniyat.",
    "Shoshqaloqlik – pushaymonlik olib keladi.",
    "Ota-ona roziligi – Tangri roziligi.",
    "Maqsad bo‘lmasa, harakatda yo‘nalish yo‘q.",
    "Haqiqatni aytish – jasorat.",
    "Ilm – eng qudratli qurol.",
    "Tinchlik – eng oliy ne’mat."
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

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Assalomu alaykum! 🤖\n/help buyrug‘i orqali imkoniyatlarni bilib oling.")

@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.chat.id,
        "/weather [shahar] - Ob-havo ma'lumotlari\n"
        "/exchange - Valyuta kurslari\n"
        "/advice - Hayotiy maslahat")

@bot.message_handler(commands=['weather'])
def weather_handler(message):
    try:
        city = message.text.split(" ", 1)[1]
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=uz"
        data = requests.get(url).json()
        if data.get("cod") != 200:
            raise Exception("Shahar topilmadi.")
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        response = f"🌤 Ob-havo: {weather}\n🌡 Harorat: {temp}°C"
        bot.send_message(message.chat.id, response)
    except:
        bot.send_message(message.chat.id, "Shahar nomini to‘g‘ri kiriting. Masalan: /weather Tashkent")

@bot.message_handler(commands=['exchange'])
def exchange_handler(message):
    try:
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/USD"
        data = requests.get(url).json()
        uzs = data["conversion_rates"]["UZS"]
        eur = data["conversion_rates"]["EUR"]
        bot.send_message(message.chat.id,
            f"💱 Valyuta kurslari:\n1 USD = {uzs} UZS\n1 EUR = {eur} USD")
    except:
        bot.send_message(message.chat.id, "Valyuta kurslarini yuklashda xatolik yuz berdi.")

@bot.message_handler(commands=['advice'])
def advice_handler(message):
    advice = random.choice(uzbek_advices)
    bot.send_message(message.chat.id, f"📌 Maslahat: {advice}")

# Flask bilan webhookni sozlash (Render uchun)
@app.route('/')
def index():
    return "Bot ishlayapti!"

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK'

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/{BOT_TOKEN}")
    app.run(host='0.0.0.0', port=port)
