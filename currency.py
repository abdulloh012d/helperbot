import requests
from config import EXCHANGE_API_KEY

def get_currency():
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/USD"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        if data['result'] != 'success':
            return "⚠ Valyuta ma'lumotlarini olishda xatolik yuz berdi."

        rates = data['conversion_rates']

        usd = 1 
        eur = rates.get('EUR')
        rub = rates.get('RUB')

        return (
            f"💵 USD: 1 USD (bazaviy valyuta)\n"
            f"💶 EUR: {eur} USD ga teng\n"
            f"🇷🇺 RUB: {rub} USD ga teng"
        )
    except requests.RequestException:
        return "⚠ Tarmoq xatosi yuz berdi."
    except ValueError:
        return "⚠ JSON ma'lumotlarini o'qishda xatolik yuz berdi."
