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


# Сокращённые идентификаторы для callback_data
category_ids = {
    'Высокобюджетные маршруты': 'high',
    'Малобюджетные маршруты': 'low'
}

# Обратные соответствия
id_to_category = {v: k for k, v in category_ids.items()}

# Адреса по категориям с НЕСКОЛЬКИМИ ВАРИАНТАМИ под каждой
addresses = {
    'high': {  # Высокобюджетная категория
        'заглушка1': {
            'address': 'Заглушка адреса',
            'coordinates': None,
            'description': 'заглушка описания',
            'display_name': 'Заглушка1',
            'photo_url': None
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
    'low': {  # Малобюджетные маршруты - ТЕПЕРЬ С НЕСКОЛЬКИМИ ВАРИАНТАМИ
        'проживание_1': {
            'address': 'хостел "Турист", Адрес: ул. Розважа, 11/1',
            'coordinates': (58.525747, 31.276239),
            'description': 'Бюджетный хостел в центре. Есть общая кухня, wi-fi, парковка.',
            'display_name': 'Хостел "Турист"',
            'photo_url': 'https://example.com/photo1.jpg',
            'category_type': 'проживание'  # Для группировки
        },
        'проживание_2': {
            'address': 'Отель "Волхов", Адрес: ул. Ленина, 4',
            'coordinates': (58.521944, 31.275833),
            'description': 'Недорогой отель с завтраками. Номера с удобствами.',
            'display_name': 'Отель "Волхов"',
            'photo_url': None,
            'category_type': 'проживание'
        },
        'проживание_3': {
            'address': 'Гостевой дом "Уют", Адрес: наб. Александра Невского, 22',
            'coordinates': (58.526389, 31.279444),
            'description': 'Гостевой дом рядом с Кремлем. Чисто, уютно, недорого.',
            'display_name': 'Гостевой дом "Уют"',
            'photo_url': None,
            'category_type': 'проживание'
        },
        'питание_1': {
            'address': 'ресторан "Чайная ложка", Адрес: ул. Большая Санкт-Петербургская, 25, ТЦ "Русь"',
            'coordinates': (58.533020, 31.267274),
            'description': 'Ресторан быстрого питания. Блины, салаты, супы. Недорого и вкусно.',
            'display_name': 'Чайная ложка',
            'photo_url': 'https://ibb.co/4nTmZZQQ',
            'category_type': 'питание'
        },
        'питание_2': {
            'address': 'Кафе "Визит", Адрес: ул. Студенческая, 10',
            'coordinates': (58.531111, 31.273611),
            'description': 'Уютное кафе с домашней кухней. Комплексные обеды.',
            'display_name': 'Кафе "Визит"',
            'photo_url': None,
            'category_type': 'питание'
        },
        'питание_3': {
            'address': 'Столовая №1, Адрес: пр. Мира, 5',
            'coordinates': (58.529722, 31.277500),
            'description': 'Городская столовая. Большой выбор, низкие цены.',
            'display_name': 'Столовая №1',
            'photo_url': None,
            'category_type': 'питание'
        },
        'бесплатные развлечения_1': {
            'address': 'Новгородский Кремль (Детинец)',
            'coordinates': (58.522222, 31.275000),
            'description': 'Прогулка по территории Кремля. Бесплатный вход на территорию.',
            'display_name': 'Новгородский Кремль',
            'photo_url': None,
            'category_type': 'бесплатные развлечения'
        },
        'бесплатные развлечения_2': {
            'address': 'Набережная Александра Невского',
            'coordinates': (58.525833, 31.281389),
            'description': 'Прогулка вдоль реки Волхов. Красивые виды, скамейки.',
            'display_name': 'Набережная',
            'photo_url': None,
            'category_type': 'бесплатные развлечения'
        },
        'бесплатные развлечения_3': {
            'address': 'Ярославово Дворище',
            'coordinates': (58.520556, 31.276389),
            'description': 'Древний архитектурный комплекс. Бесплатный осмотр территории.',
            'display_name': 'Ярославово Дворище',
            'photo_url': None,
            'category_type': 'бесплатные развлечения'
        },
        'платные развлечения_1': {
            'address': 'Грановитая палата, территория Кремля, 14а.',
            'coordinates': (58.522660, 31.275844),
            'description': 'Экскурсия по Грановитой палате. Вход платный.',
            'display_name': 'Грановитая палата',
            'photo_url': None,
            'category_type': 'платные развлечения'
        },
        'платные развлечения_2': {
            'address': 'Софийский собор, Кремль',
            'coordinates': (58.522222, 31.275000),
            'description': 'Древнейший православный храм России. Вход платный.',
            'display_name': 'Софийский собор',
            'photo_url': None,
            'category_type': 'платные развлечения'
        },
        'платные развлечения_3': {
            'address': 'Музей деревянного зодчества "Витославлицы"',
            'coordinates': (58.536667, 31.266389),
            'description': 'Музей под открытым небом. Старинные деревянные постройки.',
            'display_name': 'Витославлицы',
            'photo_url': None,
            'category_type': 'платные развлечения'
        }
    }
}

# Словарь для группировки мест по типам
place_categories = {
    'проживание': 'Проживание',
    'питание': 'Питание',
    'бесплатные развлечения': 'Бесплатные развлечения',
    'платные развлечения': 'Платные развлечения'
}


@bot.message_handler(commands=['start', 'kommands'])
def main(message):
    bot.send_message(message.chat.id,
                     'Команды для данного бота: \nлокации или /location - Показывает наши направления и расположение маршрутов в соответствии с этими направлениями;')


@bot.message_handler(func=lambda message: message.text.lower() == 'локации' or message.text.lower() == '/location')
def info(message):
    delete_previous_messages(message.chat.id)
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for category_name in category_ids.keys():
        category_id = category_ids[category_name]
        markup.add(InlineKeyboardButton(category_name, callback_data=f'cat_{category_id}'))
    msg = bot.send_message(message.chat.id, 'Наши направления:', reply_markup=markup)
    if message.chat.id not in message_ids:
        message_ids[message.chat.id] = []
    message_ids[message.chat.id].append(msg.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('cat_'))
def show_categories(call):
    delete_previous_messages(call.message.chat.id)
    category_id = call.data.split('_')[1]
    category_name = id_to_category[category_id]

    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    # Для каждой категории мест показываем типы
    for place_type, display_name in place_categories.items():
        markup.add(InlineKeyboardButton(
            display_name,
            callback_data=f'type_{category_id}_{place_type}'
        ))

    markup.add(InlineKeyboardButton('Назад', callback_data='back_to_categories'))
    msg = bot.send_message(call.message.chat.id, f'Выберите тип места в {category_name}:', reply_markup=markup)

    if call.message.chat.id not in message_ids:
        message_ids[call.message.chat.id] = []
    message_ids[call.message.chat.id].append(msg.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('type_'))
def show_places_by_type(call):
    delete_previous_messages(call.message.chat.id)
    _, category_id, place_type = call.data.split('_')

    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    # Показываем все места данного типа
    for place_id, place_info in addresses[category_id].items():
        if place_info.get('category_type') == place_type:
            markup.add(InlineKeyboardButton(
                place_info['display_name'],
                callback_data=f'place_{category_id}_{place_id}'
            ))

    markup.add(InlineKeyboardButton('Назад', callback_data=f'cat_{category_id}'))
    msg = bot.send_message(call.message.chat.id, f'Выберите место:', reply_markup=markup)

    if call.message.chat.id not in message_ids:
        message_ids[call.message.chat.id] = []
    message_ids[call.message.chat.id].append(msg.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('place_'))
def show_address_details(call):
    delete_previous_messages(call.message.chat.id)
    _, category_id, place_id = call.data.split('_')

    address_info = addresses[category_id][place_id]
    coordinates = address_info['coordinates']
    description = address_info['description']
    photo_url = address_info.get('photo_url')

    # Определяем тип места для кнопки "Назад"
    place_type = address_info.get('category_type', '')

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Назад', callback_data=f'type_{category_id}_{place_type}'))

    # Отправка фото (если есть)
    if photo_url:
        caption = f"📍 {address_info['address']}\n\n📝 {description}"
        try:
            photo_msg = bot.send_photo(call.message.chat.id, photo_url, caption=caption, reply_markup=markup)
            if call.message.chat.id not in message_ids:
                message_ids[call.message.chat.id] = []
            message_ids[call.message.chat.id].append(photo_msg.message_id)
        except:
            message_text = f"📍 {address_info['address']}\n\n📝 {description}"
            msg = bot.send_message(call.message.chat.id, message_text, reply_markup=markup)
            if call.message.chat.id not in message_ids:
                message_ids[call.message.chat.id] = []
            message_ids[call.message.chat.id].append(msg.message_id)
    else:
        message_text = f"📍 {address_info['address']}\n\n📝 {description}"
        msg = bot.send_message(call.message.chat.id, message_text, reply_markup=markup)
        if call.message.chat.id not in message_ids:
            message_ids[call.message.chat.id] = []
        message_ids[call.message.chat.id].append(msg.message_id)

    # Отправка карты (если есть координаты)
    if coordinates and len(coordinates) == 2 and coordinates[0] is not None and coordinates[1] is not None:
        location_msg = bot.send_location(call.message.chat.id, latitude=coordinates[0], longitude=coordinates[1])
        if call.message.chat.id not in message_ids:
            message_ids[call.message.chat.id] = []
        message_ids[call.message.chat.id].append(location_msg.message_id)


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_categories')
def back_to_categories(call):
    delete_previous_messages(call.message.chat.id)
    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    for category_name in category_ids.keys():
        category_id = category_ids[category_name]
        markup.add(InlineKeyboardButton(category_name, callback_data=f'cat_{category_id}'))

    msg = bot.send_message(call.message.chat.id, 'Наши направления:', reply_markup=markup)

    if call.message.chat.id not in message_ids:
        message_ids[call.message.chat.id] = []
    message_ids[call.message.chat.id].append(msg.message_id)


if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling()