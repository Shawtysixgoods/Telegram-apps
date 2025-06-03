import os  # импорт модуля для работы с переменными окружения
import telebot  # импорт библиотеки для работы с Telegram Bot API

# Получаем токен бота из переменной окружения INFO_BOT_TOKEN
TOKEN = ""
if not TOKEN:
    raise Exception("Не найден токен для info bot!")

# Инициализируем бота
bot = telebot.TeleBot(TOKEN)

# Простая база данных с информацией о городах и странах
info_data = {
    "Москва": {
        "тип": "город",
        "год основания": 1147,
        "количество улиц": 8000,
        "районы": 12,
    },
    "Париж": {
        "тип": "город",
        "год основания": 300,  # приблизительно
        "количество улиц": 6000,
        "районы": 20,
    },
    "Россия": {
        "тип": "страна",
        "год основания": 862,
        "количество городов": 1117,
        "площадь": "17,1 млн км²",
    },
    "Франция": {
        "тип": "страна",
        "год основания": 843,  # по Верденскому договору
        "количество городов": 36000,
        "площадь": "551 тыс км²",
    }
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветствие пользователя и инструкция по использованию бота
    bot.reply_to(message, "Привет! Отправь название города или страны, чтобы получить подробную информацию.")

@bot.message_handler(func=lambda message: True)
def send_info(message):
    query = message.text.strip()
    # Ищем информацию о переданном значении
    details = info_data.get(query)
    if details:
        response = f"Информация о {query}:\n"
        for key, value in details.items():
            response += f"{key}: {value}\n"
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, f"Информация о {query} не найдена. Попробуйте другой запрос.")

if __name__ == '__main__':
    # Запускаем бота в режиме polling для обработки входящих сообщений
    bot.polling()
