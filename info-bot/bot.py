import os
import telebot
from telebot import types

# Получаем токен бота из переменной окружения INFO_BOT_TOKEN
TOKEN = os.environ.get('INFO_BOT_TOKEN')
if not TOKEN:
    raise Exception("Не найден токен для info bot!")

bot = telebot.TeleBot(TOKEN)

# Простая база данных с информацией о городах и странах
info_data = {
    "Москва": {
        "тип": "город",
        "год основания": 1147,
        "количество улиц": 8000,
        "районы": 12,
    },
    "Париж": {
        "тип": "город",
        "год основания": 300,
        "количество улиц": 6000,
        "районы": 20,
    },
    "Россия": {
        "тип": "страна",
        "год основания": 862,
        "количество городов": 1117,
        "площадь": "17,1 млн км²",
    },
    "Франция": {
        "тип": "страна",
        "год основания": 843,
        "количество городов": 36000,
        "площадь": "551 тыс км²",
    }
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветствие и инструкция по использованию бота
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in info_data.keys():
        markup.add(types.KeyboardButton(name))
    markup.add(types.KeyboardButton('Добавить свою информацию'))
    bot.send_message(
        message.chat.id,
        "Привет! Выбери город или страну из меню, чтобы получить подробную информацию, или добавь свою.",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == 'Добавить свою информацию')
def ask_for_custom_info(message):
    """
    Запрашивает у пользователя название и описание для новой записи.
    """
    msg = bot.send_message(message.chat.id, 'Введи название города или страны:')
    bot.register_next_step_handler(msg, get_custom_name)

def get_custom_name(message):
    name = message.text.strip()
    msg = bot.send_message(message.chat.id, f'Введи описание или факты о "{name}":')
    bot.register_next_step_handler(msg, lambda m: save_custom_info(m, name))

def save_custom_info(message, name):
    """
    Сохраняет пользовательскую информацию в базу info_data.
    """
    info_data[name] = {'описание': message.text.strip()}
    bot.reply_to(message, f'Информация о "{name}" добавлена!')

@bot.message_handler(func=lambda m: m.text in info_data)
def send_info(message):
    """
    Отправляет подробную информацию о выбранном городе или стране.
    """
    details = info_data[message.text]
    if 'описание' in details:
        text = f'{message.text}: {details["описание"]}'
    else:
        text = f'{message.text}:\n' + '\n'.join([f'{k}: {v}' for k, v in details.items()])
    bot.reply_to(message, text)

if __name__ == '__main__':
    # Запуск бота в режиме polling
    bot.polling()
