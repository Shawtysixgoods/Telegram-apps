import os
import telebot
from telebot import types

# Получаем токен бота из переменной окружения VIDEO_BOT_TOKEN
TOKEN = os.environ.get('VIDEO_BOT_TOKEN')
if not TOKEN:
    raise Exception("Не найден токен для video bot!")

bot = telebot.TeleBot(TOKEN)

# Папка для хранения видеофайлов
VIDEO_DIR = 'videos'
os.makedirs(VIDEO_DIR, exist_ok=True)

def list_videos():
    """
    Возвращает список файлов, сохранённых в папке видео.
    """
    return os.listdir(VIDEO_DIR)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветствие и инструкция по использованию бота
    bot.reply_to(message, (
        "Привет! Я Video Bot.\n"
        "Отправь мне видео, и я его сохраню.\n"
        "Команды:\n"
        "/list — список видео\n"
        "/get — получить видео по номеру из списка"
    ))

@bot.message_handler(content_types=['video'])
def handle_video(message):
    """
    Обработчик входящих видеофайлов. Сохраняет файл в папку и подтверждает сохранение.
    """
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = os.path.join(VIDEO_DIR, message.video.file_name or f"video_{message.video.file_id}.mp4")
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)
    bot.reply_to(message, f'Видео "{os.path.basename(file_path)}" сохранено.')

@bot.message_handler(commands=['list'])
def send_video_list(message):
    """
    Отправляет пользователю список всех сохранённых видеофайлов.
    """
    videos = list_videos()
    if not videos:
        bot.reply_to(message, 'Видео пока нет.')
        return
    text = '\n'.join([f'{i+1}. {name}' for i, name in enumerate(videos)])
    bot.reply_to(message, f'Список видео:\n{text}\n\nЧтобы получить видео, отправь /get и номер (например, /get 2)')

@bot.message_handler(commands=['get'])
def send_video_by_number(message):
    """
    Отправляет пользователю видео по номеру из списка.
    """
    try:
        parts = message.text.split()
        if len(parts) != 2:
            raise ValueError
        num = int(parts[1])
        videos = list_videos()
        if num < 1 or num > len(videos):
            raise IndexError
        file_path = os.path.join(VIDEO_DIR, videos[num-1])
        with open(file_path, 'rb') as f:
            bot.send_video(message.chat.id, f)
    except Exception:
        bot.reply_to(message, 'Используй: /get <номер видео> (например, /get 1)')

if __name__ == '__main__':
    # Запуск бота в режиме polling
    bot.polling()
