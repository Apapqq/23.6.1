import telebot
from config import keys, TOKEN
from extensions import ConvException, CriptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])     # команда старт
def start(message: telebot.types.Message):
    txt = '''Привет, я бот для конвертации валют и я умею:
Показать список доступных валют через команду /values
Выполнить конвертацию валюты через команду
<имя валюты> <в какую валюту перевести> <количество переводимой валюты>
Напомнить, что я могу через команду /help'''
    bot.reply_to(message, txt)
        
@bot.message_handler(commands=['help'])        # команда хэлп
def help(message: telebot.types.Message):
    txt = '''Что бы начать работу с Ботом введите валюты которые хотите конвертировать.
Введите команду в следующем формате, через пробел:
<название валюты из которой надо конвертировать>
<название валюты в которую надо конвертировать>
<количество которое необходимо конвертировать>
Для просмотра всех доступных валют введите команду или нажмите /values.'''
    bot.reply_to(message, txt)

@bot.message_handler(commands=['values'])           # команда валюты
def values(message: telebot.types.Message):
    txt = 'Доступные валюты:'
    for key in keys.keys():
        txt = '\n'.join((txt, key))
    bot.reply_to(message, txt)

@bot.message_handler(content_types =['text'])       # глобальный обработчик
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvException('Количество параметров не совпадает. Используйте формат:\n<название валюты> \n'
               '<в какую валюту надо перевести> \n<количество переводимой валюты> \n')

        base, quote, amount = values
        total = CriptoConverter.get_price(base, quote, amount)
    except ConvException as e:
        bot.reply_to(message, f'Ошибка пользователя \n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n {e}')
    
    else:
        total_2 = float(amount) * total             # умножение 1 у.е. на количество введенное пользователем
        text = f'Цена {amount} {base} в {quote} = {total_2}'
        bot.send_message(message.chat.id, text)

bot.polling()
