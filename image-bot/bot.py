import os
import telebot
from telebot import types

# Получаем токен бота из переменной окружения IMAGE_BOT_TOKEN
TOKEN = os.environ.get('IMAGE_BOT_TOKEN')
if not TOKEN:
    raise Exception("Не найден токен для image bot!")

bot = telebot.TeleBot(TOKEN)

# Папка для хранения изображений
IMG_DIR = 'images'
os.makedirs(IMG_DIR, exist_ok=True)

def list_images():
    """
    Возвращает список файлов, сохранённых в папке изображений.
    """
    return os.listdir(IMG_DIR)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветствие и инструкция по использованию бота
    bot.reply_to(message, (
        "Привет! Я Image Bot.\n"
        "Отправь мне изображение, и я его сохраню.\n"
        "Команды:\n"
        "/list — список изображений\n"
        "/get — получить изображение по номеру из списка"
    ))

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    """
    Обработчик входящих изображений. Сохраняет файл в папку и подтверждает сохранение.
    """
    # Получаем наибольшее по размеру фото
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = os.path.join(IMG_DIR, f"photo_{photo.file_id}.jpg")
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)
    bot.reply_to(message, f'Изображение сохранено как {os.path.basename(file_path)}.')

@bot.message_handler(commands=['list'])
def send_image_list(message):
    """
    Отправляет пользователю список всех сохранённых изображений.
    """
    images = list_images()
    if not images:
        bot.reply_to(message, 'Изображений пока нет.')
        return
    text = '\n'.join([f'{i+1}. {name}' for i, name in enumerate(images)])
    bot.reply_to(message, f'Список изображений:\n{text}\n\nЧтобы получить изображение, отправь /get и номер (например, /get 2)')

@bot.message_handler(commands=['get'])
def send_image_by_number(message):
    """
    Отправляет пользователю изображение по номеру из списка.
    """
    try:
        parts = message.text.split()
        if len(parts) != 2:
            raise ValueError
        num = int(parts[1])
        images = list_images()
        if num < 1 or num > len(images):
            raise IndexError
        file_path = os.path.join(IMG_DIR, images[num-1])
        with open(file_path, 'rb') as f:
            bot.send_photo(message.chat.id, f)
    except Exception:
        bot.reply_to(message, 'Используй: /get <номер изображения> (например, /get 1)')

if __name__ == '__main__':
    # Запуск бота в режиме polling
    bot.polling()
