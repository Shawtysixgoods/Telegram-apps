import os  # импорт модуля для работы с переменными окружения
import telebot  # импорт библиотеки для работы с Telegram Bot API

# Получаем токен бота из переменной окружения VIDEO_BOT_TOKEN
TOKEN = os.environ.get('VIDEO_BOT_TOKEN')
if not TOKEN:
    raise Exception("Не найден токен для video bot!")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветствуем пользователя и объясняем функциональность бота
    bot.reply_to(message, "Привет! Я Video Bot. Отправь /video, чтобы получить видео.")

@bot.message_handler(commands=['video'])
def send_video(message):
    # Отправляем видео через Telegram (используется URL видео)
    video_url = "http://techslides.com/demos/sample-videos/small.mp4"
    bot.send_video(message.chat.id, video_url)

if __name__ == '__main__':
    bot.polling()
