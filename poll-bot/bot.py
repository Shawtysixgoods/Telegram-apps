import os
import telebot
from telebot import types

# Получаем токен бота из переменной окружения POLL_BOT_TOKEN
TOKEN = os.environ.get('POLL_BOT_TOKEN')
if not TOKEN:
    raise Exception("Не найден токен для poll bot!")

bot = telebot.TeleBot(TOKEN)

# Словарь для хранения состояния создания опроса для каждого пользователя
user_poll_state = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветствие и инструкция по использованию бота
    bot.reply_to(message, (
        "Привет! Я бот для создания опросов.\n"
        "Команда /poll — создать свой опрос."
    ))

@bot.message_handler(commands=['poll'])
def start_poll(message):
    """
    Запускает процесс создания опроса: спрашивает вопрос.
    """
    msg = bot.send_message(message.chat.id, 'Введи вопрос для опроса:')
    bot.register_next_step_handler(msg, get_poll_question)

def get_poll_question(message):
    user_poll_state[message.from_user.id] = {'question': message.text, 'options': []}
    msg = bot.send_message(message.chat.id, 'Введи первый вариант ответа:')
    bot.register_next_step_handler(msg, get_poll_option)

def get_poll_option(message):
    state = user_poll_state[message.from_user.id]
    state['options'].append(message.text)
    if len(state['options']) < 2:
        # Нужно минимум 2 варианта
        msg = bot.send_message(message.chat.id, f'Введи ещё вариант ответа:')
        bot.register_next_step_handler(msg, get_poll_option)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Готово'))
        msg = bot.send_message(message.chat.id, 'Введи ещё вариант или нажми "Готово"', reply_markup=markup)
        bot.register_next_step_handler(msg, finish_poll_options)

def finish_poll_options(message):
    if message.text == 'Готово':
        state = user_poll_state[message.from_user.id]
        bot.send_poll(
            chat_id=message.chat.id,
            question=state['question'],
            options=state['options'],
            is_anonymous=False
        )
        user_poll_state.pop(message.from_user.id, None)
    else:
        get_poll_option(message)

if __name__ == '__main__':
    # Запуск бота в режиме polling
    bot.polling()
