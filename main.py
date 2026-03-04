import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Токен моего бота
bot = telebot.TeleBot('8553675239:AAFZH-jmYRp7wToM-RcNAMdhVxCizd9UBUg')

# Словарь для хранения идентификаторов сообщений
message_ids = {}


# Функция для удаления предыдущих сообщений
def delete_previous_messages(chat_id):
    if chat_id in message_ids:
        for msg_id in message_ids[chat_id]:
            try:
                bot.delete_message(chat_id, msg_id)
            except telebot.apihelper.ApiTelegramException:
                pass
        message_ids[chat_id] = []


# Сокращённые идентификаторы для callback_data (русские названия для отображения)
category_ids = {
    'Высокобюджетные маршруты': 'high',
    'Малобюджетные маршруты': 'low'
}

# Обратные соответствия
id_to_category = {v: k for k, v in category_ids.items()}

# Адреса по категориям
addresses = {
    'high': {  # Высокобюджетная категория
        'заглушка1': {
            'address': 'Заглушка адреса',
            'coordinates': None,
            'description': 'заглушка описания',
            'display_name': 'Заглушка1',
            'photo_url': None  # Можно добавить URL фото
        },
        'заглушка2': {
            'address': 'Заглушка адреса2',
            'coordinates': None,
            'description': 'заглушка описания 2',
            'display_name': 'Заглушка2',
            'photo_url': None
        },
        'заглушка3': {
            'address': 'Заглушка адреса 3',
            'coordinates': None,
            'description': 'заглушка описания 3',
            'display_name': 'Заглушка 3',
            'photo_url': None
        },
        'заглушка4': {
            'address': 'Заглушка адреса 4',
            'coordinates': None,
            'description': 'заглушка описания 4',
            'display_name': 'Заглушка 4',
            'photo_url': None
        },
    },
    'low': {  # Малобюджетные маршруты
        'проживание': {
            'address': 'хостел "турист", Адрес: ул. розважа, 11/1',
            'coordinates': (58.525747, 31.276239),
            'description': 'Описание хостела турист',
            'display_name': 'Проживание',
            'photo_url': 'https://example.com/photo1.jpg'  # Пример URL фото
        },
        'питание': {
            'address': 'ресторан быстрого питания "чайная ложка", Адрес: большая санкт петербургская, 25 в ТЦ "Русь" ',
            'coordinates': (58.533020, 31.267274),
            'description': 'Описание для ресторана',
            'display_name': 'Питание',
            'photo_url': 'https://ibb.co/4nTmZZQQ'
        },
        'бесплатные развлечения': {
            'address': 'Прогулка',
            'coordinates': None,
            'description': 'Прогулка по кремлю и по набережной Александра Невского',
            'display_name': 'Бесплатные развлечения',
            'photo_url': None
        },
        'платные развлечения': {
            'address': 'территория Кремля, 14а.',
            'coordinates': (58.522660, 31.275844),
            'description': ' экскурсия по грановитой палате',
            'display_name': 'Платные развлечения',
            'photo_url': None
        }
    }
}


# Обработчик команд
@bot.message_handler(commands=['start', 'kommands'])
def main(message):
    bot.send_message(message.chat.id,
                     'Команды для данного бота: \nлокации или /location - Показывает наши направления и расположение маршрутов в соответствии с этими направлениями;')


# Обработчик команд "локации"
@bot.message_handler(func=lambda message: message.text.lower() == 'локации' or message.text.lower() == '/location')
def info(message):
    delete_previous_messages(message.chat.id)
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    # Показываем русские названия категорий
    for category_name in category_ids.keys():
        category_id = category_ids[category_name]
        markup.add(InlineKeyboardButton(category_name, callback_data=f'cat_{category_id}'))
    msg = bot.send_message(message.chat.id, 'Наши направления:', reply_markup=markup)
    if message.chat.id not in message_ids:
        message_ids[message.chat.id] = []
    message_ids[message.chat.id].append(msg.message_id)


# Обработчик callback-запроса с категориями
@bot.callback_query_handler(func=lambda call: call.data.startswith('cat_'))
def show_categories(call):
    delete_previous_messages(call.message.chat.id)
    category_id = call.data.split('_')[1]
    category_name = id_to_category[category_id]

    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    for place_id, place_info in addresses[category_id].items():
        markup.add(InlineKeyboardButton(
            place_info['display_name'],
            callback_data=f'place_{category_id}_{place_id}'
        ))

    markup.add(InlineKeyboardButton('Назад', callback_data='back_to_categories'))
    msg = bot.send_message(call.message.chat.id, f'Выберите направление {category_name}:', reply_markup=markup)

    if call.message.chat.id not in message_ids:
        message_ids[call.message.chat.id] = []
    message_ids[call.message.chat.id].append(msg.message_id)


# Обработчик callback-запроса с направлениями
@bot.callback_query_handler(func=lambda call: call.data.startswith('place_'))
def show_address_details(call):
    delete_previous_messages(call.message.chat.id)
    _, category_id, place_id = call.data.split('_')

    address_info = addresses[category_id][place_id]
    coordinates = address_info['coordinates']
    description = address_info['description']
    photo_url = address_info.get('photo_url')

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Назад', callback_data=f'cat_{category_id}'))

    # Если есть фото URL - отправляем фото с подписью
    if photo_url:
        # Формируем подпись к фото
        caption = f"📍 {address_info['address']}\n\n📝 {description}"

        # Отправляем фото и сохраняем его message_id
        try:
            photo_msg = bot.send_photo(call.message.chat.id, photo_url, caption=caption, reply_markup=markup)
            if call.message.chat.id not in message_ids:
                message_ids[call.message.chat.id] = []
            message_ids[call.message.chat.id].append(photo_msg.message_id)
        except:
            # Если не удалось отправить фото, отправляем текст
            message_text = f"📍 {address_info['address']}\n\n📝 {description}"
            msg = bot.send_message(call.message.chat.id, message_text, reply_markup=markup)
            if call.message.chat.id not in message_ids:
                message_ids[call.message.chat.id] = []
            message_ids[call.message.chat.id].append(msg.message_id)
    else:
        # Если нет фото - отправляем обычное сообщение
        message_text = f"📍 {address_info['address']}\n\n📝 {description}"
        msg = bot.send_message(call.message.chat.id, message_text, reply_markup=markup)
        if call.message.chat.id not in message_ids:
            message_ids[call.message.chat.id] = []
        message_ids[call.message.chat.id].append(msg.message_id)

    # Проверка координат и отправка карты
    if coordinates and len(coordinates) == 2 and coordinates[0] is not None and coordinates[1] is not None:
        # Отправляем карту и сохраняем её message_id
        location_msg = bot.send_location(call.message.chat.id, latitude=coordinates[0], longitude=coordinates[1])
        if call.message.chat.id not in message_ids:
            message_ids[call.message.chat.id] = []
        message_ids[call.message.chat.id].append(location_msg.message_id)


# Обработчик callback-запроса с кнопкой "Назад"
@bot.callback_query_handler(func=lambda call: call.data == 'back_to_categories')
def back_to_categories(call):
    delete_previous_messages(call.message.chat.id)
    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    # Показываем русские названия категорий
    for category_name in category_ids.keys():
        category_id = category_ids[category_name]
        markup.add(InlineKeyboardButton(category_name, callback_data=f'cat_{category_id}'))

    msg = bot.send_message(call.message.chat.id, 'Наши направления:', reply_markup=markup)

    if call.message.chat.id not in message_ids:
        message_ids[call.message.chat.id] = []
    message_ids[call.message.chat.id].append(msg.message_id)


# Запускаем бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling()