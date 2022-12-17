# here are the classes used in program:
# Классы для программы:

import requests
import json

import config


class ConversionException(Exception):
    pass


class ConversionFunc:
    @staticmethod
    def convert_the_input(source_currency: str, target_currency: str, amount_of_source: str):
        if source_currency == target_currency:
            raise ConversionException("Неверно - обе валюты одинаковые!")
        try:
            source_ticker = config.currency_ticker_dict[source_currency][0]
        except:
            raise ConversionException(f"Валюта {source_currency} недоступна для конверсии.\n Список валют - /list")
        try:
            target_ticker = config.currency_ticker_dict[target_currency][0]
        except:
            raise ConversionException(f"Валюта {source_currency} недоступна для конверсии.\n Список валют - /list")
        try:
            amount_of_source = float(amount_of_source)
        except:
            raise ConversionException(f"Количество валюты должно быть числом!")

        data_request = requests.get(f'{config.URL_BASE}fsym={source_ticker}&tsyms={target_ticker}&api_key={config.API_KEY}')
        total_sum = json.loads(data_request.content)[config.currency_ticker_dict[target_currency][0]]
        total_sum *=amount_of_source
        return total_sum

