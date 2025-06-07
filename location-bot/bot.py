import os
import telebot
from telebot import types

# Получаем токен бота из переменной окружения LOCATION_BOT_TOKEN
TOKEN = os.environ.get('LOCATION_BOT_TOKEN')
if not TOKEN:
    raise Exception("Не найден токен для location bot!")

bot = telebot.TeleBot(TOKEN)

# Словарь для хранения последних координат пользователей
user_locations = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветствие и инструкция по использованию бота
    bot.reply_to(message, (
        "Привет! Я Location Bot.\n"
        "Отправь мне свою геолокацию, и я её сохраню.\n"
        "Команды:\n"
        "/my — показать твою последнюю сохранённую геолокацию\n"
        "/all — показать все сохранённые геолокации пользователей"
    ))

@bot.message_handler(content_types=['location'])
def handle_location(message):
    """
    Обработчик входящих геолокаций. Сохраняет координаты пользователя.
    """
    user_locations[message.from_user.id] = (message.location.latitude, message.location.longitude)
    bot.reply_to(message, f'Геолокация сохранена: {message.location.latitude}, {message.location.longitude}')

@bot.message_handler(commands=['my'])
def send_my_location(message):
    """
    Отправляет пользователю его последнюю сохранённую геолокацию (ссылкой на карту).
    """
    loc = user_locations.get(message.from_user.id)
    if not loc:
        bot.reply_to(message, 'Геолокация не найдена. Отправь свою геолокацию!')
        return
    lat, lon = loc
    url = f'https://maps.google.com/?q={lat},{lon}'
    bot.reply_to(message, f'Твоя последняя геолокация: {lat}, {lon}\n{url}')

@bot.message_handler(commands=['all'])
def send_all_locations(message):
    """
    Отправляет список всех сохранённых геолокаций пользователей.
    """
    if not user_locations:
        bot.reply_to(message, 'Геолокаций пока нет.')
        return
    text = '\n'.join([
        f'{user_id}: {lat}, {lon} — https://maps.google.com/?q={lat},{lon}'
        for user_id, (lat, lon) in user_locations.items()
    ])
    bot.reply_to(message, f'Все геолокации пользователей:\n{text}')

if __name__ == '__main__':
    # Запуск бота в режиме polling
    bot.polling()
