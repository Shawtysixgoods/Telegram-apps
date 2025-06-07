import os
import telebot
from telebot import types

# Получаем токен бота из переменной окружения BOT_TOKEN
TOKEN = os.environ.get('ECHO_BOT_TOKEN')
if not TOKEN:
    raise Exception("Не найден токен для echo bot!")

bot = telebot.TeleBot(TOKEN)

# Словарь для хранения статистики по типам сообщений
user_stats = {}

def update_stats(user_id, msg_type):
    """
    Увеличивает счётчик сообщений определённого типа для пользователя.
    """
    if user_id not in user_stats:
        user_stats[user_id] = {'text': 0, 'photo': 0, 'document': 0, 'audio': 0, 'video': 0}
    user_stats[user_id][msg_type] += 1

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветствие и инструкция по использованию бота
    bot.reply_to(message, (
        "Привет! Я эхо-бот.\n"
        "Отправь мне текст, фото, документ, аудио или видео — я верну их тебе обратно!\n"
        "Команда /stats — твоя статистика по типам сообщений."
    ))

@bot.message_handler(commands=['stats'])
def send_stats(message):
    """
    Отправляет пользователю статистику по типам отправленных сообщений.
    """
    stats = user_stats.get(message.from_user.id)
    if not stats:
        bot.reply_to(message, 'Статистика пуста. Отправь мне что-нибудь!')
        return
    text = '\n'.join([f'{k}: {v}' for k, v in stats.items()])
    bot.reply_to(message, f'Твоя статистика:\n{text}')

@bot.message_handler(content_types=['text'])
def echo_text(message):
    """
    Эхо-ответ на текстовое сообщение.
    """
    update_stats(message.from_user.id, 'text')
    bot.reply_to(message, f'Вы сказали: {message.text}')

@bot.message_handler(content_types=['photo'])
def echo_photo(message):
    """
    Эхо-ответ на фото: возвращает то же фото.
    """
    update_stats(message.from_user.id, 'photo')
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    bot.send_photo(message.chat.id, downloaded_file)

@bot.message_handler(content_types=['document'])
def echo_document(message):
    """
    Эхо-ответ на документ: возвращает тот же документ.
    """
    update_stats(message.from_user.id, 'document')
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    bot.send_document(message.chat.id, downloaded_file, caption='Ваш документ')

@bot.message_handler(content_types=['audio'])
def echo_audio(message):
    """
    Эхо-ответ на аудиофайл: возвращает тот же аудиофайл.
    """
    update_stats(message.from_user.id, 'audio')
    file_info = bot.get_file(message.audio.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    bot.send_audio(message.chat.id, downloaded_file)

@bot.message_handler(content_types=['video'])
def echo_video(message):
    """
    Эхо-ответ на видео: возвращает то же видео.
    """
    update_stats(message.from_user.id, 'video')
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    bot.send_video(message.chat.id, downloaded_file)

if __name__ == '__main__':
    # Запуск бота в режиме polling
    bot.polling()