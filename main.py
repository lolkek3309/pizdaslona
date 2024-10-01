import telebot
import threading
import schedule
import time
from telebot import types
from datetime import datetime

# Вставьте ваш токен бота, который вы получили от BotFather
bot = telebot.TeleBot('7964280600:AAGYjlU4cdLF7rs-T2DpqZly-cahPsW6rkU')

# ID стикера (вы можете заменить этот ID на любой другой стикер)
STICKER_ID = 'CAACAgIAAxkBAAEIxn5m9U7rQ0WcromIRXZCAAHtRNSy6lQAAvUCAAKiivEHo-q55w_WPUk2BA'
STICKER_IDD = 'CAACAgIAAxkBAAEIz0tm9ybDA9PxASZPfJlZDEwGivzoyAACBj8AAiPM6EsryXCJK7c2GTYE'
# Пример расписания для двух видов недель
even_week_schedule = {
    'понедельник': '9:00 - Разговоры о важном 🔢\n11:00 - Вышмат 📐\n11:00 - Прикладная Электроника ⚡\n11:00 - Дискретная Математика 📊\n11:00 - Метрология, стандартизация и сертификация 📏\n11:00 - Метрология, стандартизация и сертификация 📏\n11:00 - Метрология, стандартизация и сертификация 📏\n11:00 - Цифровая схемотехника 💻\n11:00 - Цифровая схемотехника 💻',
    'вторник': '10:00 - Вышмат 📐\n12:00 - Микропроцессорные системы 🔬\n12:00 - Программирование микроконтроллеров 🔌\n12:00 - Микропроцессорные системы 🔬\n12:00 - Разработка приложений для цифровых устройств 📱\n12:00 - Разработка приложений для цифровых устройств 📱\n12:00 - Программирование микроконтроллеров 🔌\n12:00 - Микропроцессорные системы 🔬',
    'среда': '9:00 - _________\n11:00 - _________\n11:00 - _________\n11:00 - _________\n11:00 - Дискретная Математика 📚\n11:00 - Цифровая схемотехника 💡\n11:00 - Цифровая схемотехника 💡\n11:00 - Цифровая схемотехника 💡',
    'четверг': '9:00 - Дискретная Математика 📜\n11:00 - Цифровая схемотехника 🌍\n11:00 - Инновационные технологии 🚀\n11:00 - Инновационные технологии 🚀\n11:00 - Прикладная Электроника ⚡\n11:00 - Прикладная Электроника ⚡\n11:00 - Проектирование цифровых устройств ⚙️\n11:00 - Проектирование цифровых устройств ⚙️',
    'пятница': '9:00 - Физкультура 🏃‍♂️\n11:00 - Физкультура 🏋️‍♀️\n11:00 - Английский 🇬🇧\n11:00 - Проектирование цифровых устройств 📐\n11:00 - Проектирование цифровых устройств 📐\n11:00 - Проектирование цифровых устройств 📐\n11:00 - Проектирование цифровых устройств 📐\n11:00 - Проектирование цифровых устройств 📐',
}
odd_week_schedule = {
    'понедельник': '9:00 - Английский 🇬🇧\n11:00 - Математикаффф 🔢',
    'вторник': '10:00 - Информатика 💻\n12:00 - Физика 🧲',
    'среда': '9:00 - Биология 🧬\n11:00 - Литература 📚',
    'четверг': '9:00 - География 🌍\n11:00 - История 📜',
    'пятница': '9:00 - Физкультура 🏃‍♂️\n11:00 - Химия 🔬',

}       
# Укажите ID администратора для проверки прав доступа
ADMIN_CHAT_ID = 1510432017  # Убедитесь, что это число, а не строка

# Словарь для хранения информации о пользователях (ID, имя, ник)
users_info = {}
user_messages = {}  # Словарь для хранения сообщений от пользователей

# Функция для отправки расписания на текущий день
def send_daily_schedule(chat_id, is_even):
    current_day = time.strftime('%A').lower()
    day_mapping = {
        'monday': 'понедельник',
        'tuesday': 'вторник',
        'wednesday': 'среда',
        'thursday': 'четверг',
        'friday': 'пятница',
        'saturday': 'суббота',
        'sunday': 'воскресенье'
    }

    if current_day in day_mapping:
        day = day_mapping[current_day]
        if is_even:
            message = f"📅 Расписание на {day.capitalize()} (Чётная неделя):\n{even_week_schedule[day]}"
        else:
            message = f"📅 Расписание на {day.capitalize()} (Нечётная неделя):\n{odd_week_schedule[day]}"
        bot.send_message(chat_id, message)


# Планирование отправки расписания
def schedule_messages():
    schedule.every().day.at("08:30").do(send_daily_schedule, ADMIN_CHAT_ID, is_even_week())
    while True:
        schedule.run_pending()
        time.sleep(10)


# Функция для создания клавиатуры
def create_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text="🗓 Расписание", callback_data='choose_week'),
        types.InlineKeyboardButton(text="🌐 Перейти на сайт", url='https://academy.kp11.ru'),
        types.InlineKeyboardButton(text="👤 Админ панель", callback_data='admin_panel'),
        types.InlineKeyboardButton(text="📩 Сообщить администратору", callback_data='message_admin')
    )
    return keyboard


# Клавиатура для выбора недели
def create_week_choice_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text="🟢 Чётная неделя", callback_data='even_week'),
        types.InlineKeyboardButton(text="🔵 Нечётная неделя", callback_data='odd_week')
    )
    keyboard.add(types.InlineKeyboardButton(text="⬅️ Назад", callback_data='back_to_main'))
    return keyboard


# Создание клавиатуры с днями недели
def create_day_keyboard(is_even):
    keyboard = types.InlineKeyboardMarkup()
    days = [
        ("Понедельник", 'понедельник'),
        ("Вторник", 'вторник'),
        ("Среда", 'среда'),
        ("Четверг", 'четверг'),
        ("Пятница", 'пятница'),
    ]
    for day_name, day_code in days:
        callback_data = f'{day_code}_{is_even}'
        keyboard.add(types.InlineKeyboardButton(text=day_name, callback_data=callback_data))
    keyboard.add(types.InlineKeyboardButton(text="⬅️ Назад", callback_data='back_to_week_choice'))
    return keyboard


# Приветственное сообщение /start
@bot.message_handler(commands=['start'])
def start_message(message):
    # Добавляем пользователя в словарь с его именем и ником
    users_info[message.chat.id] = {
        'name': message.from_user.first_name,
        'username': message.from_user.username
    }

    welcome_message = f'Привет, {message.from_user.first_name}! 😊 Я бот для расписания. 📅 Выберите неделю, чтобы увидеть расписание. 📖'
    bot.send_message(message.chat.id, welcome_message, reply_markup=create_keyboard())


# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    if 'спасибо' in message.text.lower():
        bot.send_sticker(message.chat.id, STICKER_ID)



# Обработка нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'choose_week':
        bot.send_message(call.message.chat.id, 'Выберите неделю:', reply_markup=create_week_choice_keyboard())
    elif call.data == 'even_week':
        bot.send_message(call.message.chat.id, 'Выберите день недели (Чётная неделя):', reply_markup=create_day_keyboard(is_even=True))
    elif call.data == 'odd_week':
        bot.send_message(call.message.chat.id, 'Выберите день недели (Нечётная неделя):', reply_markup=create_day_keyboard(is_even=False))
    elif call.data.endswith('_True'):  # Для чётной недели
        day = call.data.split('_')[0]
        bot.send_message(call.message.chat.id, f"📅 Расписание на {day.capitalize()} (Чётная неделя):\n{even_week_schedule[day]}")
    elif call.data.endswith('_False'):  # Для нечётной недели
        day = call.data.split('_')[0]
        bot.send_message(call.message.chat.id, f"📅 Расписание на {day.capitalize()} (Нечётная неделя):\n{odd_week_schedule[day]}")
    elif call.data == 'back_to_week_choice':
        bot.send_message(call.message.chat.id, 'Выберите неделю:', reply_markup=create_week_choice_keyboard())
    elif call.data == 'back_to_main':
        start_message(call.message)
    elif call.data == 'admin_panel':
        if call.message.chat.id == ADMIN_CHAT_ID:  # Проверка на админа
            show_users(call.message)
            show_user_messages(call.message)  # Показать личные сообщения
        else:
            bot.send_message(call.message.chat.id, '⛔ У вас нет прав доступа к админ-панели.')
    elif call.data == 'message_admin':
        msg = bot.send_message(call.message.chat.id, '📝 Введите ваше сообщение для администратора:')
        bot.register_next_step_handler(msg, process_user_message)



# Функция для обработки сообщений от пользователей
def process_user_message(message):
    user_id = message.chat.id
    user_name = users_info[user_id]['name'] if user_id in users_info else "Пользователь"
    user_text = message.text

    # Сохраняем сообщение от пользователя для администратора
    user_messages[user_id] = user_text

    # Отправляем сообщение администратору
    bot.send_message(ADMIN_CHAT_ID, f"📝 Сообщение от {user_name} (@{users_info[user_id]['username']}):\n{user_text}")
    bot.send_message(user_id, "✅ Ваше сообщение отправлено администратору.")


# Функция для отображения пользователей в админ-панели
def show_users(message):
    if users_info:
        user_list = "📋 Список пользователей:\n\n"
        for user_id, user_data in users_info.items():
            user_list += f"👤 {user_data['name']} (@{user_data['username']})\n"
        bot.send_message(ADMIN_CHAT_ID, user_list)
    else:
        bot.send_message(ADMIN_CHAT_ID, "🔍 Нет зарегистрированных пользователей.")


# Функция для отображения сообщений пользователей
def show_user_messages(message):
    if user_messages:
        message_list = "📩 Сообщения от пользователей:\n\n"
        for user_id, user_text in user_messages.items():
            user_name = users_info[user_id]['name']
            message_list += f"👤 {user_name} (@{users_info[user_id]['username']}):\n{user_text}\n\n"
        bot.send_message(ADMIN_CHAT_ID, message_list)
    else:
        bot.send_message(ADMIN_CHAT_ID, "🔍 Нет новых сообщений.")


# Уведомление о запуске бота
def notify_bot_start():
    chat_id = ADMIN_CHAT_ID  # Вставьте сюда ID чата, куда бот будет отправлять уведомление
    bot.send_message(chat_id, 'Бот запущен и готов к работе! 🚀')


# Запуск бота с уведомлением о запуске
notify_bot_start()

bot.polling(none_stop=True)