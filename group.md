# **📚 Полное руководство по созданию Telegram-бота для групп на Python (библиотека `pyTelegramBotAPI`)**

Это пошаговое интерактивное руководство поможет вам создать бота для управления Telegram-группой. Мы разберём:
1. **Основы работы с TeleBot**
2. **Команды для модерации**
3. **Автоматические реакции на события**
4. **Дополнительные функции (вежливость, анти-спам и др.)**

---

## **🔧 1. Настройка окружения**
### **1.1 Установка библиотеки**
```bash
pip install pyTelegramBotAPI
```

### **1.2 Создание бота через BotFather**
1. Откройте Telegram, найдите **@BotFather**.
2. Используйте команду `/newbot`, следуйте инструкциям.
3. Получите **API-токен** (например, `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`).

---

## **🤖 2. Базовый код бота**
Создайте файл `bot.py` и добавьте минимальный код:

```python
import telebot
from telebot import types  # Для кнопок и других элементов

# Инициализация бота с вашим токеном
bot = telebot.TeleBot("ВАШ_ТОКЕН")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для управления группой. Используй /help для списка команд.")

# Запуск бота
print("Бот запущен...")
bot.polling()
```

### **🔍 Разбор кода:**
- `telebot.TeleBot("TOKEN")` — создаёт объект бота.
- `@bot.message_handler` — декоратор для обработки сообщений.
- `commands=['start']` — реагирует на команду `/start`.
- `bot.reply_to()` — отвечает на сообщение.
- `bot.polling()` — запускает бесконечный цикл опроса серверов Telegram.

---

## **🛠 3. Основные функции для групп**
### **3.1 Кик пользователя (команда /kick)**
```python
@bot.message_handler(commands=['kick'])
def kick_user(message):
    # Проверяем, что команду вызвал админ
    chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator']:
        bot.reply_to(message, "❌ Только админы могут кикать!")
        return

    # Проверяем, что это ответ на чьё-то сообщение
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответьте на сообщение пользователя, чтобы кикнуть его!")
        return

    user_to_kick = message.reply_to_message.from_user
    try:
        # Кикаем (с возможностью вернуться)
        bot.kick_chat_member(message.chat.id, user_to_kick.id)
        bot.unban_chat_member(message.chat.id, user_to_kick.id)  # Разбаниваем, чтобы можно было вернуться
        bot.reply_to(message, f"🚷 Пользователь {user_to_kick.first_name} был кикнут!")
    except Exception as e:
        bot.reply_to(message, f"⚠ Ошибка: {e}")
```

### **🔍 Разбор кода:**
- `bot.get_chat_member()` — проверяет статус пользователя (админ/обычный).
- `message.reply_to_message` — сообщение, на которое ответили.
- `bot.kick_chat_member()` — банит пользователя.
- `bot.unban_chat_member()` — снимает бан (чтобы пользователь мог вернуться по ссылке).

---

### **3.2 Автоматический бан за плохие слова**
```python
# Список запрещённых слов (можно расширить)
BAD_WORDS = ['мат', 'спам', 'оскорбление']

@bot.message_handler(func=lambda message: True)  # Обрабатывает ВСЕ сообщения
def check_bad_words(message):
    # Игнорируем сообщения от админов
    chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status in ['administrator', 'creator']:
        return

    # Проверяем на плохие слова
    if any(word in message.text.lower() for word in BAD_WORDS):
        try:
            bot.delete_message(message.chat.id, message.message_id)  # Удаляем сообщение
            bot.kick_chat_member(message.chat.id, message.from_user.id)  # Кикаем
            bot.send_message(
                message.chat.id,
                f"⚠ {message.from_user.first_name} был забанен за нарушение правил!"
            )
        except Exception as e:
            print(f"Ошибка: {e}")
```

### **🔍 Разбор кода:**
- `func=lambda message: True` — обрабатывает **все** сообщения.
- `any(word in message.text.lower()...)` — проверяет, есть ли плохие слова.
- `bot.delete_message()` — удаляет нарушающее правило сообщение.

---

## **📌 4. Дополнительные функции**
### **4.1 Приветствие новых участников**
```python
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for user in message.new_chat_members:
        welcome_text = (
            f"👋 Добро пожаловать, {user.first_name}!\n"
            "📌 Пожалуйста, ознакомьтесь с правилами группы."
        )
        bot.send_message(message.chat.id, welcome_text)
```

### **4.2 Удаление ссылок (кроме разрешённых)**
```python
@bot.message_handler(func=lambda m: 'http://' in m.text or 'https://' in m.text)
def delete_links(message):
    # Разрешённые домены (например, youtube.com)
    ALLOWED_DOMAINS = ['youtube.com', 'github.com']
    
    # Проверяем, что ссылка не из разрешённых
    if not any(domain in message.text for domain in ALLOWED_DOMAINS):
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(
            message.chat.id,
            f"❌ {message.from_user.first_name}, ссылки запрещены!"
        )
```

