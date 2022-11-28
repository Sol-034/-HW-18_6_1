import requests
import json
from config import keys

class ConversionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту - {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту - {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'Не удалось обработать количество - {amount}')

        if quote == base:
            raise ConversionException(f'Не удалось конвертировать валюту "{base}" в "{quote}"')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = json.loads(r.content)[quote_ticker] * amount

        return total_base

    @staticmethod
    def сhange_endings(currency: str, amount: float):
        int_amount = int(amount)
        change_currency = currency

        if currency == "доллар":
            if int_amount % 10 == 1:
                change_currency = "доллар"
            elif 11 <= int_amount <= 14:
                change_currency = "долларов"
            elif 2 <= int_amount % 10 <= 4:
                change_currency = "доллара"
            else:
                change_currency = "долларов"

        elif currency == "рубль":
            if int_amount % 10 == 1:
                change_currency = "рубль"
            elif 11 <= int_amount <= 14:
                change_currency = "рублей"
            elif 2 <= int_amount % 10 <= 4:
                change_currency = "рубля"
            else:
                change_currency = "рублей"

        return change_currency
