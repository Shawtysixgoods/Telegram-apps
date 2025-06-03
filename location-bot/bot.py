import os  # импорт модуля для работы с переменными окружения
import telebot  # импорт библиотеки для работы с Telegram Bot API

# Получаем токен бота из переменной окружения LOCATION_BOT_TOKEN
TOKEN = ""
if not TOKEN:
    raise Exception("Не найден токен для location bot!")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветствуем пользователя и объясняем функциональность бота
    bot.reply_to(message, "Привет! Я Location Bot. Отправь /location, чтобы получить координаты.")

@bot.message_handler(commands=['location'])
def send_location(message):
    # Отправляем геолокацию: пример координат (например, Нью-Йорк)
    latitude = 40.7128
    longitude = -74.0060
    bot.send_location(message.chat.id, latitude, longitude)

if __name__ == '__main__':
    bot.polling()
