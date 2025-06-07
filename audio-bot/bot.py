import os
import telebot
from telebot import types

# Получаем токен бота из переменной окружения AUDIO_BOT_TOKEN
TOKEN = os.environ.get('AUDIO_BOT_TOKEN')
if not TOKEN:
    raise Exception("Не найден токен для audio bot!")

bot = telebot.TeleBot(TOKEN)

# Папка для хранения аудиофайлов
AUDIO_DIR = 'audios'
os.makedirs(AUDIO_DIR, exist_ok=True)

def list_audios():
    """
    Возвращает список файлов, сохранённых в папке аудио.
    """
    return os.listdir(AUDIO_DIR)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветствие и инструкция по использованию бота
    bot.reply_to(message, (
        "Привет! Я Audio Bot.\n"
        "Отправь мне аудиофайл, и я его сохраню.\n"
        "Команды:\n"
        "/list — список аудиофайлов\n"
        "/get — получить аудиофайл по номеру из списка"
    ))

@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    """
    Обработчик входящих аудиофайлов. Сохраняет файл в папку и подтверждает сохранение.
    """
    file_info = bot.get_file(message.audio.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = os.path.join(AUDIO_DIR, message.audio.file_name or f"audio_{message.audio.file_id}.mp3")
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)
    bot.reply_to(message, f'Аудиофайл "{os.path.basename(file_path)}" сохранён.')

@bot.message_handler(commands=['list'])
def send_audio_list(message):
    """
    Отправляет пользователю список всех сохранённых аудиофайлов.
    """
    audios = list_audios()
    if not audios:
        bot.reply_to(message, 'Аудиофайлов пока нет.')
        return
    text = '\n'.join([f'{i+1}. {name}' for i, name in enumerate(audios)])
    bot.reply_to(message, f'Список аудиофайлов:\n{text}\n\nЧтобы получить аудио, отправь /get и номер (например, /get 2)')

@bot.message_handler(commands=['get'])
def send_audio_by_number(message):
    """
    Отправляет пользователю аудиофайл по номеру из списка.
    """
    try:
        parts = message.text.split()
        if len(parts) != 2:
            raise ValueError
        num = int(parts[1])
        audios = list_audios()
        if num < 1 or num > len(audios):
            raise IndexError
        file_path = os.path.join(AUDIO_DIR, audios[num-1])
        with open(file_path, 'rb') as f:
            bot.send_audio(message.chat.id, f)
    except Exception:
        bot.reply_to(message, 'Используй: /get <номер аудиофайла> (например, /get 1)')

if __name__ == '__main__':
    # Запуск бота в режиме polling
    bot.polling()
