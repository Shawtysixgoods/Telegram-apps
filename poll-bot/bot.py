import os  # импортируем модуль для работы с переменными окружения
import telebot  # импортируем библиотеку для работы с Telegram Bot API

# Получаем токен бота из переменной окружения BOT_TOKEN
TOKEN = ""
if not TOKEN:
    raise Exception("Не найден токен бота!")

# Инициализируем объект бота с полученным токеном
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start: приветствует пользователя и объясняет функциональность бота
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Отправляем приветственное сообщение и объясняем, что бот умеет создавать опросы
    bot.reply_to(message, "Привет! Я бот для создания опросов. Используй команду /poll, чтобы запустить опрос.")

# Обработчик команды /poll: создаёт опрос и отправляет пользователю
@bot.message_handler(commands=['poll'])
def send_poll(message):
    # Определяем вопрос для опроса
    poll_question = "Какой язык программирования вы предпочитаете?"
    # Определяем варианты ответов
    poll_options = ["Python", "JavaScript", "Java", "C++"]
    # Отправляем опрос в чат с подробным объяснением (неанонимный опрос)
    bot.send_poll(
        chat_id=message.chat.id,
        question=poll_question,
        options=poll_options,
        is_anonymous=False,  # опрос не является анонимным
        explanation="Голосуйте за ваш любимый язык программирования"  # объяснение опроса
    )

# Запускаем бота в режиме polling для обработки входящих сообщений
if __name__ == '__main__':
    bot.polling()  # бот начинает опрос Telegram сервера на новые сообщения
