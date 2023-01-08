import json

import requests

from config import keys


class ConvertException(Exception):
    pass


class MyApi:
    @staticmethod
    def get_price(base, quote, amount):
        result = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}')

        return json.loads(result.content)[quote] * amount


class CriptoConverter:
    @staticmethod
    def convert(base: str, quote: str, amount: str):

        if base == quote:
            raise ConvertException(f'Невозможно конвертировать.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту {quote}.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f'Не удалось обработать количество {amount}.')

        current = MyApi.get_price(base_ticker, quote_ticker, amount)

        return current
