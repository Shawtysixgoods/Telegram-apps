# ПОЛНОЕ РУКОВОДСТВО ПО TELEBOT ДЛЯ НОВИЧКОВ

---

## 0. Что такое Telebot? Зачем он нужен?

**Telebot** — это библиотека на Python для создания Telegram-ботов. Она позволяет писать программы, которые могут:
- Автоматически отвечать на сообщения
- Принимать и отправлять файлы, фото, видео, аудио
- Делать опросы, напоминания, игры, рассылки
- Хранить и обрабатывать данные пользователей

**Бот** — это виртуальный собеседник, который работает 24/7 и может выполнять любые задачи, которые вы ему запрограммируете.

**Где применяется?**
- Автоматизация бизнеса (приём заказов, поддержка)
- Учебные проекты и игры
- Личные помощники (напоминания, заметки)
- Информационные сервисы (погода, новости)

---

## 1. Как установить Telebot? (Очень просто!)

1. **Проверьте Python:**
   Откройте терминал и напишите:
   ```bash
   python --version
   ```
   Если увидели версию (например, 3.10.0) — всё хорошо!
   Если нет — скачайте Python с https://python.org

2. **Установите Telebot:**
   ```bash
   pip install pyTelegramBotAPI
   ```
   - **pip** — менеджер пакетов Python, устанавливает библиотеки.
   - **pyTelegramBotAPI** — официальное название Telebot.

3. **Проверьте установку:**
   Введите в Python:
   ```python
   import telebot
   print(telebot.__version__)
   ```
   Если ошибок нет — всё готово!

---

## 2. Как получить токен для бота? (Без токена бот не работает)

1. Откройте Telegram, найдите **@BotFather** — это официальный бот для создания других ботов.
2. Напишите ему `/newbot` и следуйте инструкциям:
   - Придумайте имя (любое)
   - Придумайте username (должен заканчиваться на `bot`, например, `mytestbot`)
3. BotFather даст вам токен — длинную строку вида:
   ```
   123456789:AAE...xyz
   ```
   Это ваш ключ! Никому не показывайте его.

4. **Проверьте токен:**
   Вставьте его в код и попробуйте запустить простейший бот (см. ниже).

---

## 3. Самый простой бот (Пример для самых маленьких)

```python
import telebot  # импортируем библиотеку Telebot
TOKEN = 'ВАШ_ТОКЕН'  # сюда вставьте свой токен
bot = telebot.TeleBot(TOKEN)  # создаём объект бота

@bot.message_handler(commands=['start'])  # обработчик команды /start
def start(message):
    bot.reply_to(message, 'Привет! Я твой первый бот!')  # отвечаем на команду /start

bot.polling()  # запускает бота, чтобы он слушал новые сообщения
```

**Что тут происходит?**
- `import telebot` — подключаем библиотеку Telebot, чтобы использовать её функции.
- `telebot.TeleBot(TOKEN)` — создаём объект бота, который будет общаться с Telegram.
- `@bot.message_handler(commands=['start'])` — декоратор, который говорит: "Если пришла команда /start — вызови функцию ниже".
- `def start(message): ...` — функция, которая будет вызвана при команде /start. Аргумент `message` — это объект, в котором лежит вся информация о сообщении пользователя.
- `bot.reply_to(message, ...)` — бот отвечает на то сообщение, которое получил.
- `bot.polling()` — запускает бесконечный цикл, чтобы бот всегда был на связи и реагировал на новые сообщения.

**Практика:**
- Попробуйте изменить текст ответа.
- Добавьте ещё одну команду, например `/help`.

---

## 4. Как бот понимает, что ему пишут? (Обработчики)

**Обработчик** — это функция, которая срабатывает, когда приходит определённый тип сообщения.

### 4.1. Текстовые сообщения
```python
@bot.message_handler(content_types=['text'])  # ловим все текстовые сообщения
def echo(message):
    bot.send_message(message.chat.id, f'Ты написал: {message.text}')  # отправляем обратно текст пользователя
```
- `@bot.message_handler(content_types=['text'])` — ловит все текстовые сообщения.
- `bot.send_message(chat_id, text)` — отправляет сообщение в чат с указанным chat_id.
- `message.chat.id` — идентификатор чата, куда нужно отправить ответ.
- `message.text` — текст, который написал пользователь.

**Теория:**
- Каждый обработчик ловит только свой тип сообщений.
- Можно сделать несколько обработчиков для разных типов (текст, фото, документы и т.д.).

**Практика:**
- Попробуйте отправить боту текстовое сообщение и посмотрите, как он ответит.

### 4.2. Документы
```python
@bot.message_handler(content_types=['document'])  # ловим документы
def handle_doc(message):
    file_info = bot.get_file(message.document.file_id)  # получаем информацию о файле
    downloaded = bot.download_file(file_info.file_path)  # скачиваем файл
    with open(message.document.file_name, 'wb') as f:  # открываем файл для записи
        f.write(downloaded)  # сохраняем файл на диск
    bot.reply_to(message, 'Документ сохранён!')  # подтверждаем сохранение
```
- `message.document.file_id` — уникальный идентификатор файла в Telegram.
- `bot.get_file(file_id)` — получает путь к файлу на серверах Telegram.
- `bot.download_file(file_path)` — скачивает файл по этому пути.
- `with open(..., 'wb') as f:` — открывает файл для записи в бинарном режиме.
- `f.write(downloaded)` — записывает скачанные данные в файл.

**Практика:**
- Попробуйте отправить себе документ и убедитесь, что он сохранился в папке с ботом.

### 4.3. Фото
```python
@bot.message_handler(content_types=['photo'])  # ловим фото
def handle_photo(message):
    photo = message.photo[-1]  # берём самое большое фото (лучшее качество)
    file_info = bot.get_file(photo.file_id)  # получаем информацию о фото
    downloaded = bot.download_file(file_info.file_path)  # скачиваем фото
    with open(f'photo_{photo.file_id}.jpg', 'wb') as f:  # открываем файл для записи
        f.write(downloaded)  # сохраняем фото на диск
    bot.reply_to(message, 'Фото сохранено!')  # подтверждаем сохранение
```
- `message.photo` — список разных размеров фото, берём последнее (самое большое).

**Теория:**
- Telegram всегда присылает несколько размеров фото. Обычно нужно брать последнее (самое большое).

**Практика:**
- Попробуйте отправить боту фото и посмотрите, как он его сохранит.

### 4.4. Аудио, видео, геолокация
- Для аудио: `content_types=['audio']`
- Для видео: `content_types=['video']`
- Для геолокации: `content_types=['location']`

**Пример для аудио:**
```python
@bot.message_handler(content_types=['audio'])  # ловим аудиофайлы
def handle_audio(message):
    file_info = bot.get_file(message.audio.file_id)  # получаем информацию об аудио
    downloaded = bot.download_file(file_info.file_path)  # скачиваем аудио
    with open('audio.mp3', 'wb') as f:  # открываем файл для записи
        f.write(downloaded)  # сохраняем аудио на диск
    bot.reply_to(message, 'Аудио сохранено!')  # подтверждаем сохранение
```
- `message.audio.file_id` — идентификатор аудиофайла.

**Практика:**
- Попробуйте отправить боту аудиофайл, видео или свою геолокацию.

---

## 5. Команды бота (Что такое команда?)

**Команда** — это сообщение, которое начинается с `/` (например, `/start`, `/help`).

```python
@bot.message_handler(commands=['help'])  # ловим команду /help
def help_cmd(message):
    bot.send_message(message.chat.id, 'Я умею: /start, /help, /echo ...')  # отправляем список команд
```
- `commands=['help']` — список команд, которые ловит этот обработчик.
- `bot.send_message(...)` — отправляет сообщение в чат.

**Как получить аргумент команды?**
```python
@bot.message_handler(commands=['say'])  # ловим команду /say
def say(message):
    text = message.text.partition(' ')[2]  # берём всё, что после команды
    bot.send_message(message.chat.id, f'Ты сказал: {text}')  # повторяем текст
```
- `message.text` — вся строка сообщения, включая команду.
- `.partition(' ')[2]` — берём всё, что после первого пробела (аргумент команды).

**Теория:**
- Команды — это основной способ взаимодействия с ботом.
- Можно делать команды с аргументами (например, `/remind купить хлеб`).

**Практика:**
- Добавьте команду `/echo`, которая повторяет всё, что напишет пользователь после команды.

---

## 6. Клавиатуры и кнопки (Чтобы было удобно!)

### 6.1. Обычная клавиатура (ReplyKeyboard)
```python
from telebot import types  # импортируем types для клавиатур
@bot.message_handler(commands=['menu'])  # ловим команду /menu
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создаём клавиатуру
    markup.add(types.KeyboardButton('Кнопка 1'), types.KeyboardButton('Кнопка 2'))  # добавляем кнопки
    bot.send_message(message.chat.id, 'Выберите:', reply_markup=markup)  # отправляем клавиатуру
```
- **ReplyKeyboardMarkup** — создаёт обычную клавиатуру, которая появляется вместо поля ввода.
- **KeyboardButton** — кнопка на клавиатуре.
- `resize_keyboard=True` — клавиатура подстраивается под размер экрана.

**Теория:**
- Обычная клавиатура удобна для часто используемых команд.

**Практика:**
- Попробуйте добавить больше кнопок, сделать несколько строк.

### 6.2. Инлайн-кнопки (InlineKeyboard)
```python
@bot.message_handler(commands=['inline'])  # ловим команду /inline
def inline(message):
    markup = types.InlineKeyboardMarkup()  # создаём инлайн-клавиатуру
    markup.add(types.InlineKeyboardButton('Google', url='https://google.com'))  # добавляем кнопку-ссылку
    bot.send_message(message.chat.id, 'Ссылка:', reply_markup=markup)  # отправляем клавиатуру
```
- **InlineKeyboardMarkup** — кнопки прямо под сообщением.
- **InlineKeyboardButton** — кнопка, может быть ссылкой или вызывать callback.

**Теория:**
- Инлайн-кнопки часто используют для опросов, меню, ссылок.

**Практика:**
- Сделайте инлайн-кнопку, которая отправляет callback (см. документацию Telebot).

---

## 7. Состояния и диалоги (Пошаговые сценарии)

**Иногда нужно спросить у пользователя что-то и дождаться ответа.**

```python
def ask_name(message):
    msg = bot.send_message(message.chat.id, 'Как тебя зовут?')  # спрашиваем имя
    bot.register_next_step_handler(msg, save_name)  # ждём следующий ответ

def save_name(message):
    bot.send_message(message.chat.id, f'Привет, {message.text}!')  # приветствуем по имени
```
- **register_next_step_handler** — регистрирует функцию, которая обработает следующий ответ пользователя.

**Теория:**
- Это удобно для создания анкет, опросов, пошаговых меню.

**Практика:**
- Сделайте бота, который спрашивает имя, возраст и выводит анкету.

---

## 8. Работа с файлами и папками (Где хранить файлы?)

- Для хранения файлов создавайте отдельные папки:
  ```python
  import os  # импортируем os для работы с файлами и папками
  os.makedirs('documents', exist_ok=True)  # создаём папку для документов
  os.makedirs('images', exist_ok=True)  # создаём папку для картинок
  ```
- Чтобы узнать, какие файлы уже есть:
  ```python
  files = os.listdir('documents')  # получаем список файлов
  for name in files:
      print(name)  # выводим имена файлов
  ```
- Чтобы удалить файл:
  ```python
  os.remove('documents/имя_файла.pdf')  # удаляем файл
  ```

**Теория:**
- Хранить файлы в отдельных папках — удобно для порядка.
- Для больших проектов используйте базы данных или облачные хранилища.

**Практика:**
- Сделайте бота, который сохраняет все документы в папку и по команде выводит их список.

---

## 9. Хранение данных пользователей (Память, файлы, база)

- **В памяти:**
  ```python
  user_data = {}  # создаём словарь для хранения данных пользователей
  user_data[message.from_user.id] = 'значение'  # сохраняем данные по user_id
  ```
  - Просто, но данные исчезнут после перезапуска бота.
- **В файле (txt, json):**
  ```python
  import json  # импортируем json для работы с файлами
  with open('users.json', 'w') as f:
      json.dump(user_data, f)  # сохраняем словарь в файл
  ```
  - Данные сохраняются между перезапусками.
- **В базе данных (SQLite):**
  ```python
  import sqlite3  # импортируем sqlite3 для работы с базой данных
  conn = sqlite3.connect('users.db')  # подключаемся к базе
  c = conn.cursor()  # создаём курсор
  c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)')  # создаём таблицу
  c.execute('INSERT INTO users VALUES (?, ?)', (message.from_user.id, 'Имя'))  # добавляем пользователя
  conn.commit()  # сохраняем изменения
  conn.close()  # закрываем соединение
  ```
  - Для больших и серьёзных проектов.

**Теория:**
- Для простых ботов хватит словаря.
- Для долговременного хранения — файлы или базы данных.

**Практика:**
- Сделайте бота, который запоминает имя пользователя и приветствует его по имени при следующем запуске.

---

## 10. Как отправить файл пользователю?

- **Документ:**
  ```python
  with open('documents/файл.pdf', 'rb') as f:  # открываем документ для чтения
      bot.send_document(message.chat.id, f)  # отправляем документ
  ```
- **Фото:**
  ```python
  with open('images/фото.jpg', 'rb') as f:  # открываем фото для чтения
      bot.send_photo(message.chat.id, f)  # отправляем фото
  ```
- **Аудио:**
  ```python
  with open('audios/трек.mp3', 'rb') as f:  # открываем аудио для чтения
      bot.send_audio(message.chat.id, f)  # отправляем аудио
  ```
- **Видео:**
  ```python
  with open('videos/видео.mp4', 'rb') as f:  # открываем видео для чтения
      bot.send_video(message.chat.id, f)  # отправляем видео
  ```

**Теория:**
- Для отправки файлов используйте соответствующие методы: `send_document`, `send_photo`, `send_audio`, `send_video`.
- Всегда открывайте файлы в режиме `'rb'` (чтение в бинарном режиме).

**Практика:**
- Сделайте команду `/getdoc`, которая отправляет пользователю случайный документ из папки.

---

## 11. Обработка ошибок (Чтобы бот не падал)

```python
try:
    # Ваш код  # здесь пишите свой код
except Exception as e:
    bot.reply_to(message, f'Ошибка: {e}')  # бот напишет об ошибке
```
- Если что-то пошло не так, бот не упадёт, а напишет об ошибке.

**Теория:**
- Ошибки бывают всегда: неправильный ввод, проблемы с сетью, файлы не найдены.
- Обработка ошибок делает бота надёжнее.

**Практика:**
- Добавьте обработку ошибок во все функции, которые работают с файлами или сетью.

---

## 12. Как запустить бота на сервере (чтобы работал всегда)

- Для постоянной работы используйте VPS или облако.
- Можно запускать через screen, tmux или как systemd-сервис.
- Не публикуйте токен в открытом доступе!
- Для автозапуска используйте systemd:
  ```ini
  [Unit]
  Description=My Telegram Bot
  [Service]
  ExecStart=/usr/bin/python3 /path/to/bot.py
  Restart=always
  [Install]
  WantedBy=multi-user.target
  ```

**Теория:**
- VPS — это виртуальный сервер, который работает круглосуточно.
- systemd — стандартный способ автозапуска программ в Linux.

**Практика:**
- Попробуйте запустить бота на бесплатном сервере (например, PythonAnywhere, Heroku, Railway).

---

## 13. Полезные советы и лайфхаки

- Проверяйте тип сообщения через `content_types`.
- Добавляйте комментарии к коду (чтобы не забыть, что делает каждая часть).
- Не храните большие файлы в памяти — используйте временные файлы.
- Для сложных ботов используйте базы данных.
- Читайте официальную документацию: https://github.com/eternnoir/pyTelegramBotAPI
- Для тестирования используйте отдельный Telegram-аккаунт.
- Не забывайте про обработку ошибок!
- Используйте виртуальное окружение Python (`python -m venv venv`), чтобы не засорять систему.

---

## 14. Примеры задач (развёрнуто)

### 14.1. Эхо-бот (бот-попугай)
```python
@bot.message_handler(content_types=['text'])  # ловим все текстовые сообщения
def echo(message):
    bot.send_message(message.chat.id, message.text)  # повторяет текст пользователя
```
- Всё, что напишет пользователь, бот повторит.

### 14.2. Бот для хранения файлов (документов)
```python
@bot.message_handler(content_types=['document'])  # ловим документы
def save_doc(message):
    file_info = bot.get_file(message.document.file_id)  # получаем информацию о файле
    downloaded = bot.download_file(file_info.file_path)  # скачиваем файл
    with open('documents/' + message.document.file_name, 'wb') as f:  # открываем файл для записи
        f.write(downloaded)  # сохраняем файл на диск
    bot.reply_to(message, 'Документ сохранён!')  # подтверждаем сохранение

@bot.message_handler(commands=['list'])  # ловим команду /list
def list_docs(message):
    files = os.listdir('documents')  # получаем список файлов
    text = '\n'.join(files)  # объединяем в строку
    bot.send_message(message.chat.id, f'Документы:\n{text}')  # отправляем список документов
```
- Бот сохраняет документы, а по команде `/list` показывает их список.

### 14.3. Бот-опросник (бот для голосований)
```python
@bot.message_handler(commands=['poll'])  # ловим команду /poll
def poll(message):
    bot.send_poll(message.chat.id, 'Ваш любимый язык?', ['Python', 'JS', 'C++'])  # создаёт опрос
```
- Бот создаёт опрос прямо в чате.

### 14.4. Бот-напоминалка (очень просто)
```python
import threading  # импортируем threading для работы с потоками
@bot.message_handler(commands=['remind'])  # ловим команду /remind
def remind(message):
    text = message.text.partition(' ')[2]  # берём текст напоминания
    def send_later():
        import time; time.sleep(10)  # ждём 10 секунд
        bot.send_message(message.chat.id, f'Напоминание: {text}')  # отправляем напоминание
    threading.Thread(target=send_later).start()  # запускаем в отдельном потоке
```
- Бот примет текст, подождёт 10 секунд и напомнит вам о нём.

---

## 15. Часто задаваемые вопросы (FAQ)

**Q:** Почему бот не отвечает?
- Проверьте токен.
- Проверьте интернет.
- Проверьте, что бот запущен (`bot.polling()`).

**Q:** Как узнать свой user_id?
- Добавьте в код: `bot.send_message(message.chat.id, message.from_user.id)`

**Q:** Как ограничить доступ к боту?
- Сравнивайте `message.from_user.id` с разрешёнными id.

**Q:** Как сделать бота только для себя?
```python
ALLOWED = [123456789]  # ваш user_id
@bot.message_handler(func=lambda m: m.from_user.id in ALLOWED)  # разрешаем только определённым пользователям
def private(message):
    ...  # здесь ваш код для приватного доступа
```

---

## 17. Ещё больше примеров и идей для функционала

### 17.1. Как сохранить любой файл от пользователя (универсальный обработчик)

```python
@bot.message_handler(content_types=['document', 'photo', 'audio', 'video'])  # ловим все типы файлов
def save_any_file(message):
    if message.content_type == 'document':  # если это документ
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        with open('documents/' + message.document.file_name, 'wb') as f:
            f.write(downloaded)
        bot.reply_to(message, 'Документ сохранён!')
    elif message.content_type == 'photo':  # если это фото
        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        downloaded = bot.download_file(file_info.file_path)
        with open(f'images/photo_{photo.file_id}.jpg', 'wb') as f:
            f.write(downloaded)
        bot.reply_to(message, 'Фото сохранено!')
    elif message.content_type == 'audio':  # если это аудио
        file_info = bot.get_file(message.audio.file_id)
        downloaded = bot.download_file(file_info.file_path)
        with open('audios/' + (message.audio.file_name or f'audio_{message.audio.file_id}.mp3'), 'wb') as f:
            f.write(downloaded)
        bot.reply_to(message, 'Аудио сохранено!')
    elif message.content_type == 'video':  # если это видео
        file_info = bot.get_file(message.video.file_id)
        downloaded = bot.download_file(file_info.file_path)
        with open('videos/' + (message.video.file_name or f'video_{message.video.file_id}.mp4'), 'wb') as f:
            f.write(downloaded)
        bot.reply_to(message, 'Видео сохранено!')
```
- Такой обработчик позволяет принимать любые типы файлов и сохранять их в разные папки.
- Подробнее о типах сообщений: [Документация Telebot: content_types](https://github.com/eternnoir/pyTelegramBotAPI#message-handlers)

### 17.2. Как отправить пользователю список всех файлов определённого типа

```python
import os  # ...existing code...
@bot.message_handler(commands=['listfiles'])  # команда /listfiles <тип>
def list_files(message):
    parts = message.text.split()
    if len(parts) != 2:
        bot.reply_to(message, 'Используй: /listfiles <document|photo|audio|video>')
        return
    ftype = parts[1]
    folder = {'document': 'documents', 'photo': 'images', 'audio': 'audios', 'video': 'videos'}.get(ftype)
    if not folder:
        bot.reply_to(message, 'Неизвестный тип файла!')
        return
    files = os.listdir(folder)
    if not files:
        bot.reply_to(message, f'Файлов типа {ftype} нет.')
        return
    text = '\n'.join(files)
    bot.send_message(message.chat.id, f'Файлы типа {ftype}:\n{text}')
```
- Такой подход позволяет пользователю самому выбирать, какие файлы он хочет посмотреть.
- Подробнее: [Документация Telebot: send_message](https://github.com/eternnoir/pyTelegramBotAPI#telebottelebot)

### 17.3. Как отправить пользователю файл по имени

```python
@bot.message_handler(commands=['getfile'])  # команда /getfile <тип> <имя>
def get_file(message):
    parts = message.text.split(maxsplit=2)
    if len(parts) != 3:
        bot.reply_to(message, 'Используй: /getfile <document|photo|audio|video> <имя_файла>')
        return
    ftype, fname = parts[1], parts[2]
    folder = {'document': 'documents', 'photo': 'images', 'audio': 'audios', 'video': 'videos'}.get(ftype)
    if not folder:
        bot.reply_to(message, 'Неизвестный тип файла!')
        return
    path = os.path.join(folder, fname)
    try:
        with open(path, 'rb') as f:
            if ftype == 'document':
                bot.send_document(message.chat.id, f)
            elif ftype == 'photo':
                bot.send_photo(message.chat.id, f)
            elif ftype == 'audio':
                bot.send_audio(message.chat.id, f)
            elif ftype == 'video':
                bot.send_video(message.chat.id, f)
    except Exception as e:
        bot.reply_to(message, f'Ошибка: {e}')
```
- Такой способ позволяет пользователю получить любой файл по имени.
- Подробнее: [Документация Telebot: отправка файлов](https://github.com/eternnoir/pyTelegramBotAPI#sending-files)

### 17.4. Как ограничить размер загружаемых файлов

```python
MAX_SIZE = 10 * 1024 * 1024  # 10 МБ
@bot.message_handler(content_types=['document'])
def save_doc_with_limit(message):
    if message.document.file_size > MAX_SIZE:
        bot.reply_to(message, 'Файл слишком большой! Максимум 10 МБ.')
        return
    file_info = bot.get_file(message.document.file_id)
    downloaded = bot.download_file(file_info.file_path)
    with open('documents/' + message.document.file_name, 'wb') as f:
        f.write(downloaded)
    bot.reply_to(message, 'Документ сохранён!')
```
- Проверяйте размер файла перед сохранением, чтобы не переполнить диск.
- Подробнее: [Документация Telebot: message.document](https://github.com/eternnoir/pyTelegramBotAPI#message)

### 17.5. Как сделать бота, который принимает ZIP-архивы и распаковывает их

```python
import zipfile
@bot.message_handler(content_types=['document'])
def handle_zip(message):
    if message.document.mime_type == 'application/zip':  # проверяем тип файла
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        zip_path = 'documents/' + message.document.file_name
        with open(zip_path, 'wb') as f:
            f.write(downloaded)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('documents/unzipped/')  # распаковываем архив
        bot.reply_to(message, 'Архив распакован!')
```
- Такой бот может принимать архивы и автоматически их распаковывать.
- Подробнее: [Документация Python: zipfile](https://docs.python.org/3/library/zipfile.html)

---

## 18. Полезные ссылки

- [Официальная документация Telebot (pyTelegramBotAPI)](https://github.com/eternnoir/pyTelegramBotAPI)
- [Документация по типам сообщений](https://core.telegram.org/bots/api#message)
- [Документация по методам отправки файлов](https://core.telegram.org/bots/api#sending-files)
- [Документация Python: работа с файлами](https://docs.python.org/3/tutorial/inputoutput.html)
- [Документация Python: os](https://docs.python.org/3/library/os.html)
- [Документация Python: zipfile](https://docs.python.org/3/library/zipfile.html)
