import os  # импорт модуля для работы с переменными окружения
import telebot  # импорт библиотеки для работы с Telegram Bot API

# Получаем токен бота из переменной окружения IMAGE_BOT_TOKEN
TOKEN = ""
if not TOKEN:
    raise Exception("Не найден токен для image bot!")

# Инициализируем объект бота с полученным токеном
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветствуем пользователя и объясняем функциональность бота
    bot.reply_to(message, "Привет! Я Image Bot. Отправь /image, чтобы увидеть изображение.")

@bot.message_handler(commands=['image'])
def send_image(message):
    # Отправляем изображение через Telegram (используется URL изображения)
    image_url = "https://via.placeholder.com/300.png"
    bot.send_photo(message.chat.id, image_url)

if __name__ == '__main__':
    # Запускаем бота с использованием polling
    bot.polling()
