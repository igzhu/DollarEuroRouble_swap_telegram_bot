# Telegram Currency-Converter-Bot main app file
# исполняемый файл всей программы

import requests
import json
import telebot

from config import TOKEN, currency_ticker_dict
from conversion_classes import ConversionException, ConversionFunc

convert_currency_bot = telebot.TeleBot(TOKEN)

@convert_currency_bot.message_handler(commands=["start", "help"])
def help_message(message: telebot.types.Message):
    response_text = " Введите данные (через пробел) в виде:\n \
<из валюты> <в валюту> <сумма>:\nДля конвертации доступны валюты /list."
    convert_currency_bot.reply_to(message, response_text)

@convert_currency_bot.message_handler(commands=["list"])
def list_of_currencies(message: telebot.types.Message):
    response_text = "Для конвертации доступны:\n------------------------------------------"
    for currency in currency_ticker_dict.keys():
        response_text = "\n".join((response_text, currency))
    convert_currency_bot.reply_to(message, response_text)

@convert_currency_bot.message_handler(content_types=["text",])
def convert(message: telebot.types.Message):
    try:
        user_input = message.text.split()
        if len(user_input) != 3:
            raise ConversionException("Требуется указать три параметра!")
        source_currency, target_currency, amount_of_source = user_input
        response_to_user = ConversionFunc.convert_the_input(source_currency, target_currency, amount_of_source)
    except ConversionException as e:
        convert_currency_bot.reply_to(message, f'Неверный запрос. \n{e}')
    except Exception as e:
        convert_currency_bot.reply_to(message, f'Сбой в работе. \n{e}')
    else:
        response_text = f'{currency_ticker_dict[source_currency][1]}{amount_of_source} равно \
{currency_ticker_dict[target_currency][1]}{response_to_user:.4f}'
        convert_currency_bot.send_message(message.chat.id, response_text)


convert_currency_bot.polling(none_stop=True)
