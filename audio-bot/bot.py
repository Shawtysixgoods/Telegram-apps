import os  # импорт модуля для работы с переменными окружения
import telebot  # импорт библиотеки для работы с Telegram Bot API

# Получаем токен бота из переменной окружения AUDIO_BOT_TOKEN
TOKEN = os.environ.get('AUDIO_BOT_TOKEN')
if not TOKEN:
    raise Exception("Не найден токен для audio bot!")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветствуем пользователя и объясняем функциональность бота
    bot.reply_to(message, "Привет! Я Audio Bot. Отправь /audio, чтобы получить аудиофайл.")

@bot.message_handler(commands=['audio'])
def send_audio(message):
    # Отправляем аудиофайл через Telegram (используется URL аудио)
    audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    bot.send_audio(message.chat.id, audio_url)

if __name__ == '__main__':
    bot.polling()
