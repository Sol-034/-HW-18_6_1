import telebot
from config import TOKEN, keys
from extensions import CryptoConverter, ConversionException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def echo_test(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите 3 значения через пробел в следующем формате: \n <имя валюты> \
<имя валюты в которой надо узнать цену первой валюты> \
<количество первой валюты> \nНапример, если хотите узнать, сколько будет 25 долларов в рублях, то введите следующую строку:\nдоллар рубль 25\n\n/values - список доступных валют'
    bot.reply_to(message,text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def get_get(message: telebot.types.Message):
    try:
        #получение строк от пользователя и преобразование их нижний регистр
        values = list(map(str.lower,message.text.split(" ")))

        #проверка правильного количества параметров
        if len(values) != 3:
            raise ConversionException('Введено неверное количество параметров')

        base, quote, amount = values

        #дополнительные проверки на ошибки пользовательского ввода
        total_quote = CryptoConverter.get_price(base, quote, amount)

    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        # установка "правильных" окончаний в названии валют
        base = CryptoConverter.сhange_endings(base, amount)
        quote = CryptoConverter.сhange_endings(quote,total_quote)

        # формирование ответа
        answer = f"{amount} {base} стоит {round(total_quote,2)} {quote}"
        bot.reply_to(message, answer)

bot.polling(none_stop=True)
