import os  # импорт модуля для работы с переменными окружения
import telebot  # импорт библиотеки для работы с Telegram Bot API

# Получаем токен бота из переменной окружения DOCUMENT_BOT_TOKEN
TOKEN = ""
if not TOKEN:
    raise Exception("Не найден токен для document bot!")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветствуем пользователя и объясняем функциональность бота
    bot.reply_to(message, "Привет! Я Document Bot. Отправь /document, чтобы получить документ.")

@bot.message_handler(commands=['document'])
def send_document(message):
    # Отправляем документ по URL (пример PDF документа)
    document_url = "https://evil-teacher.on.fleek.co/books/tp/Cormen_Algorithms.pdf"
    bot.send_document(message.chat.id, document_url)

if __name__ == '__main__':
    bot.polling()
