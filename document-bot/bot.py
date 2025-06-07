import os
import telebot
from telebot import types

# Получаем токен бота из переменной окружения DOCUMENT_BOT_TOKEN
TOKEN = os.environ.get('DOCUMENT_BOT_TOKEN')
if not TOKEN:
    raise Exception("Не найден токен для document bot!")

bot = telebot.TeleBot(TOKEN)

# Папка для хранения документов
DOCS_DIR = 'documents'
os.makedirs(DOCS_DIR, exist_ok=True)

def list_documents():
    """
    Возвращает список файлов, сохранённых в папке документов.
    """
    return os.listdir(DOCS_DIR)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветствие и инструкция по использованию бота
    bot.reply_to(message, (
        "Привет! Я Document Bot.\n"
        "Отправь мне документ, и я его сохраню.\n"
        "Команды:\n"
        "/list — список документов\n"
        "/get — получить документ по номеру из списка"
    ))

@bot.message_handler(content_types=['document'])
def handle_document(message):
    """
    Обработчик входящих документов. Сохраняет файл в папку и подтверждает сохранение.
    """
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = os.path.join(DOCS_DIR, message.document.file_name)
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)
    bot.reply_to(message, f'Документ "{message.document.file_name}" сохранён.')

@bot.message_handler(commands=['list'])
def send_doc_list(message):
    """
    Отправляет пользователю список всех сохранённых документов.
    """
    docs = list_documents()
    if not docs:
        bot.reply_to(message, 'Документов пока нет.')
        return
    text = '\n'.join([f'{i+1}. {name}' for i, name in enumerate(docs)])
    bot.reply_to(message, f'Список документов:\n{text}\n\nЧтобы получить документ, отправь /get и номер (например, /get 2)')

@bot.message_handler(commands=['get'])
def send_document_by_number(message):
    """
    Отправляет пользователю документ по номеру из списка.
    """
    try:
        parts = message.text.split()
        if len(parts) != 2:
            raise ValueError
        num = int(parts[1])
        docs = list_documents()
        if num < 1 or num > len(docs):
            raise IndexError
        file_path = os.path.join(DOCS_DIR, docs[num-1])
        with open(file_path, 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception:
        bot.reply_to(message, 'Используй: /get <номер документа> (например, /get 1)')

if __name__ == '__main__':
    # Запуск бота в режиме polling
    bot.polling()
