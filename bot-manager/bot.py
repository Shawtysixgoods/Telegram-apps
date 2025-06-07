import os
import telebot
from telebot import types

# Получаем токен бота-менеджера из переменной окружения BOT_MANAGER_TOKEN
TOKEN = os.environ.get('BOT_MANAGER_TOKEN')
if not TOKEN:
    raise Exception("Не найден токен для bot-manager!")

bot = telebot.TeleBot(TOKEN)

# Папки для хранения файлов разных типов
DATA_DIR = 'bot_manager_data'
AUDIO_DIR = os.path.join(DATA_DIR, 'audios')
DOCS_DIR = os.path.join(DATA_DIR, 'documents')
IMG_DIR = os.path.join(DATA_DIR, 'images')
VIDEO_DIR = os.path.join(DATA_DIR, 'videos')
LOC_FILE = os.path.join(DATA_DIR, 'locations.txt')

for d in [AUDIO_DIR, DOCS_DIR, IMG_DIR, VIDEO_DIR]:
    os.makedirs(d, exist_ok=True)

# Вспомогательные функции для работы с файлами

def list_files(folder):
    """
    Возвращает список файлов в указанной папке.
    """
    return os.listdir(folder)

# Словарь для хранения последних координат пользователей
user_locations = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветствие и инструкция по использованию бота-менеджера
    bot.reply_to(message, (
        "Привет! Я Bot Manager.\n"
        "Я могу принимать и хранить документы, аудио, изображения, видео и геолокации.\n"
        "Команды:\n"
        "/list <тип> — список файлов (audio, document, image, video)\n"
        "/get <тип> <номер> — получить файл по номеру из списка\n"
        "/my_location — твоя последняя геолокация\n"
        "/all_locations — все геолокации пользователей\n"
        "Просто отправь файл или геолокацию!"
    ))

# Обработка документов
@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = os.path.join(DOCS_DIR, message.document.file_name)
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)
    bot.reply_to(message, f'Документ "{message.document.file_name}" сохранён.')

# Обработка аудиофайлов
@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    file_info = bot.get_file(message.audio.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = os.path.join(AUDIO_DIR, message.audio.file_name or f"audio_{message.audio.file_id}.mp3")
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)
    bot.reply_to(message, f'Аудиофайл "{os.path.basename(file_path)}" сохранён.')

# Обработка изображений
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = os.path.join(IMG_DIR, f"photo_{photo.file_id}.jpg")
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)
    bot.reply_to(message, f'Изображение сохранено как {os.path.basename(file_path)}.')

# Обработка видео
@bot.message_handler(content_types=['video'])
def handle_video(message):
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = os.path.join(VIDEO_DIR, message.video.file_name or f"video_{message.video.file_id}.mp4")
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)
    bot.reply_to(message, f'Видео "{os.path.basename(file_path)}" сохранено.')

# Обработка геолокаций
@bot.message_handler(content_types=['location'])
def handle_location(message):
    user_locations[message.from_user.id] = (message.location.latitude, message.location.longitude)
    # Сохраняем все локации в файл
    with open(LOC_FILE, 'a') as f:
        f.write(f'{message.from_user.id},{message.location.latitude},{message.location.longitude}\n')
    bot.reply_to(message, f'Геолокация сохранена: {message.location.latitude}, {message.location.longitude}')

# Список файлов по типу
@bot.message_handler(commands=['list'])
def send_file_list(message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            raise ValueError
        ftype = parts[1]
        folder = {'audio': AUDIO_DIR, 'document': DOCS_DIR, 'image': IMG_DIR, 'video': VIDEO_DIR}.get(ftype)
        if not folder:
            raise ValueError
        files = list_files(folder)
        if not files:
            bot.reply_to(message, f'Файлов типа {ftype} пока нет.')
            return
        text = '\n'.join([f'{i+1}. {name}' for i, name in enumerate(files)])
        bot.reply_to(message, f'Список файлов типа {ftype}:\n{text}\n\nЧтобы получить файл, отправь /get {ftype} <номер>')
    except Exception:
        bot.reply_to(message, 'Используй: /list <audio|document|image|video>')

# Получение файла по номеру
@bot.message_handler(commands=['get'])
def send_file_by_number(message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            raise ValueError
        ftype, num = parts[1], int(parts[2])
        folder = {'audio': AUDIO_DIR, 'document': DOCS_DIR, 'image': IMG_DIR, 'video': VIDEO_DIR}.get(ftype)
        if not folder:
            raise ValueError
        files = list_files(folder)
        if num < 1 or num > len(files):
            raise IndexError
        file_path = os.path.join(folder, files[num-1])
        with open(file_path, 'rb') as f:
            if ftype == 'audio':
                bot.send_audio(message.chat.id, f)
            elif ftype == 'document':
                bot.send_document(message.chat.id, f)
            elif ftype == 'image':
                bot.send_photo(message.chat.id, f)
            elif ftype == 'video':
                bot.send_video(message.chat.id, f)
    except Exception:
        bot.reply_to(message, 'Используй: /get <audio|document|image|video> <номер>')

# Моя последняя геолокация
@bot.message_handler(commands=['my_location'])
def send_my_location(message):
    loc = user_locations.get(message.from_user.id)
    if not loc:
        bot.reply_to(message, 'Геолокация не найдена. Отправь свою геолокацию!')
        return
    lat, lon = loc
    url = f'https://maps.google.com/?q={lat},{lon}'
    bot.reply_to(message, f'Твоя последняя геолокация: {lat}, {lon}\n{url}')

# Все геолокации
@bot.message_handler(commands=['all_locations'])
def send_all_locations(message):
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
