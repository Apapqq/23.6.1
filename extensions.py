import requests
import json
from config import keys

class ConvException(Exception):
    pass


class CriptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):


        if base == quote:
            raise ConvException(f'Не возможное действие для одинаковых валют {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvException(f'Не удалось обработать валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total = json.loads(r.content)[keys[quote]]

        return total 
