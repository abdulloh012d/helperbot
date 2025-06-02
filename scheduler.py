from apscheduler.schedulers.background import BackgroundScheduler
from telebot import TeleBot
import random

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

def start_scheduler(bot: TeleBot):
    scheduler = BackgroundScheduler()

    def send_advice():
        for chat_id in subscribed_users:
            advice = random.choice(advices)
            bot.send_message(chat_id, f"📌 Bugungi maslahat: {advice}")

    scheduler.add_job(send_advice, 'cron', hour=9, minute=0)
    scheduler.start()

def subscribe_user(chat_id: int):
    subscribed_users.add(chat_id)
