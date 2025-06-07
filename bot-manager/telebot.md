# Полное руководство по Telebot для новичков

## Введение

**Telebot** — это популярная библиотека на Python для создания Telegram-ботов. Она проста в освоении, подходит для новичков и позволяет быстро реализовать любые идеи для ботов: от простых эхо-ботов до сложных менеджеров файлов и чатов.

---

## 1. Установка Telebot

1. Убедитесь, что у вас установлен Python 3.7+.
2. Установите библиотеку Telebot (pyTelegramBotAPI):

```bash
pip install pyTelegramBotAPI
```

---

## 2. Получение токена для бота

1. Откройте Telegram и найдите пользователя @BotFather.
2. Напишите ему команду `/newbot` и следуйте инструкциям.
3. Скопируйте выданный токен — он понадобится для запуска бота.

---

## 3. Базовая структура бота

```python
import telebot

TOKEN = 'ВАШ_ТОКЕН'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет! Я ваш бот.')

bot.polling()
```

- `@bot.message_handler(...)` — декоратор, который указывает, какие сообщения обрабатывать.
- `bot.reply_to(message, text)` — ответить на сообщение пользователя.
- `bot.polling()` — запуск бота (опрос сервера Telegram).

---

## 4. Обработка разных типов сообщений

### Текстовые сообщения
```python
@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.chat.id, f'Вы написали: {message.text}')
```

### Документы
```python
@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(message.document.file_name, 'wb') as f:
        f.write(downloaded_file)
    bot.reply_to(message, 'Документ сохранён!')
```

### Фото
```python
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'photo_{photo.file_id}.jpg', 'wb') as f:
        f.write(downloaded_file)
    bot.reply_to(message, 'Фото сохранено!')
```

### Аудио, видео, геолокация
- Для аудио: `content_types=['audio']`
- Для видео: `content_types=['video']`
- Для геолокации: `content_types=['location']`

---

## 5. Команды бота

Команды — это сообщения, начинающиеся с `/` (например, `/start`).

```python
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, 'Список команд: /start, /help, ...')
```

---

## 6. Клавиатуры и кнопки

### Обычная клавиатура
```python
from telebot import types

@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Кнопка 1'), types.KeyboardButton('Кнопка 2'))
    bot.send_message(message.chat.id, 'Выберите:', reply_markup=markup)
```

### Инлайн-кнопки
```python
@bot.message_handler(commands=['inline'])
def inline(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Google', url='https://google.com'))
    bot.send_message(message.chat.id, 'Ссылка:', reply_markup=markup)
```

---

## 7. Состояния и последовательные действия

Иногда нужно спросить у пользователя что-то и ждать ответа:

```python
def ask_name(message):
    msg = bot.send_message(message.chat.id, 'Как тебя зовут?')
    bot.register_next_step_handler(msg, save_name)

def save_name(message):
    bot.send_message(message.chat.id, f'Привет, {message.text}!')
```

---

## 8. Работа с файлами и папками

- Для хранения файлов создавайте отдельные папки (например, `documents/`, `images/`).
- Используйте `os.makedirs('папка', exist_ok=True)` для создания папки, если её нет.
- Для получения списка файлов: `os.listdir('папка')`.

---

## 9. Хранение данных пользователей

- Для простых задач можно использовать словари в памяти:
```python
user_data = {}
user_data[message.from_user.id] = 'значение'
```
- Для долговременного хранения используйте файлы (txt, json) или базы данных (например, SQLite).

---

## 10. Отправка файлов пользователю

```python
with open('путь_к_файлу', 'rb') as f:
    bot.send_document(message.chat.id, f)
```
- Для фото: `bot.send_photo(...)`
- Для аудио: `bot.send_audio(...)`
- Для видео: `bot.send_video(...)`

---

## 11. Обработка ошибок

```python
try:
    # Ваш код
except Exception as e:
    bot.reply_to(message, f'Ошибка: {e}')
```

---

## 12. Запуск бота на сервере

- Для постоянной работы используйте VPS или облако.
- Можно запускать через `screen`, `tmux` или как systemd-сервис.
- Не публикуйте токен в открытом доступе!

---

## 13. Полезные советы

- Всегда проверяйте тип сообщения (`content_types`).
- Добавляйте комментарии к коду.
- Не храните большие файлы в памяти — используйте временные файлы.
- Для сложных ботов используйте базы данных.
- Читайте официальную документацию: https://github.com/eternnoir/pyTelegramBotAPI

---

## 14. Примеры задач

- Эхо-бот: повторяет всё, что пишет пользователь.
- Бот для хранения файлов: принимает и выдаёт документы, фото, аудио, видео.
- Бот-опросник: создаёт опросы и собирает ответы.
- Бот-напоминалка: принимает текст и время, присылает напоминание.

---

## 15. Часто задаваемые вопросы

**Q:** Почему бот не отвечает?
- Проверьте токен.
- Проверьте интернет.
- Проверьте, что бот запущен (`bot.polling()`).

**Q:** Как узнать свой user_id?
- Добавьте в код: `bot.send_message(message.chat.id, message.from_user.id)`

**Q:** Как ограничить доступ к боту?
- Сравнивайте `message.from_user.id` с разрешёнными id.

---

## 16. Итоги

Telebot — отличный инструмент для старта в мире Telegram-ботов. Экспериментируйте, пробуйте разные типы сообщений, храните файлы, делайте опросы и учитесь на практике!

---

**Удачи в создании своих Telegram-ботов!**
