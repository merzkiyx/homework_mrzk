import telebot
from Config import keys, TOKEN
from testbot import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы введите команду: \n<имя валюты, цену которой хотите узнать> ' \
           '<имя валюты, в которой надо узнать цену первой валюты>  ' \
           '<количество первой валюты>\nПосмотреть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: ' + ', '.join(keys.keys())
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров! (Доступно 3 параметра: имя валюты 1, имя валюты 2, количество).')

        quote, base, amount = values

        total_base = CurrencyConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()