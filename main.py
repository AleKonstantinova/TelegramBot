import telebot

from config import keys, TOKEN
from extensions import ConvertException, CriptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Для начала работы необходимо ввести команду в формате:\n<наименование валюты>\
    <в какую валюту перевести> \
    <количество валюты>'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertException('Неверно введены параметры.')

        base, quote, amount = values
        total_base = CriptoConverter.convert(base, quote, amount)

        text = f'Цена {amount} {base} в {quote} - {total_base}'
        bot.send_message(message.chat.id, text)

    except ConvertException as err:
        bot.send_message(message.chat.id, str(err))
    except Exception:
        bot.send_message(message.chat.id, 'Ошибка сервера.')


bot.polling()
