import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

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

# Типы мест (для второго уровня меню)
place_types = {
    'prozhivanie': '🏨 Проживание',
    'pitanie': '🍽️ Питание',
    'besplatnie': '🚶 Бесплатные развлечения',
    'platnie': '🎟️ Платные развлечения'
}

# Словарь для хранения состояния пользователя (выбранная категория)
user_category = {}

# Адреса по категориям (твои данные сократил для примера, вставь свои)
addresses = {
    'high': {
        'high_prozhivanie_1': {
            'address': 'Отель "Волхов", ул.Предтеченская, 24',
            'coordinates': (58.523759, 31.265594),
            'description': 'Гостиница «Волхов» расположена в центре города...',
            'display_name': 'Отель "Волхов"',
            'photo_url': 'https://ibb.co/VcGcxV6p',
            'type': 'prozhivanie'
        },
    },
    'low': {
        'low_prozhivanie_1': {
            'address': 'хостел "турист", ул. розважа, 11/1',
            'coordinates': (58.525747, 31.276239),
            'description': 'Хостел «Турист» находится в центре города...',
            'display_name': 'Хостел "Турист"',
            'photo_url': 'https://ibb.co/8DQsjpHD',
            'type': 'prozhivanie'
        },
    }
}


def show_main_menu(chat_id):
    """Показывает главное меню с категориями"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = []
    for name in category_ids.keys():
        buttons.append(KeyboardButton(name))
    markup.add(*buttons)

    msg = bot.send_message(chat_id, "🏠 Выберите направление:", reply_markup=markup)
    if chat_id not in message_ids:
        message_ids[chat_id] = []
    message_ids[chat_id].append(msg.message_id)


def show_place_types_menu(chat_id, category_id):
    """Показывает меню с типами мест для выбранной категории"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = []
    for name in place_types.values():
        buttons.append(KeyboardButton(name))
    markup.add(*buttons)
    markup.add(KeyboardButton("🔙 Назад"))

    category_name = id_to_category[category_id]
    msg = bot.send_message(chat_id, f"📋 Выберите категорию в {category_name}:", reply_markup=markup)
    if chat_id not in message_ids:
        message_ids[chat_id] = []
    message_ids[chat_id].append(msg.message_id)


def show_places_list(chat_id, place_type_key, place_type_name):
    """Показывает список мест выбранного типа"""
    delete_previous_messages(chat_id)

    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    category_id = user_category.get(chat_id, 'high')

    # Показываем места из выбранной категории
    for place_id, place_info in addresses[category_id].items():
        if place_info.get('type') == place_type_key:
            markup.add(InlineKeyboardButton(
                place_info['display_name'],
                callback_data=f'place_{category_id}_{place_id}'
            ))

    markup.add(InlineKeyboardButton("🔙 Назад к категориям", callback_data='back_to_types'))

    msg = bot.send_message(chat_id, f"{place_type_name}:", reply_markup=markup)
    if chat_id not in message_ids:
        message_ids[chat_id] = []
    message_ids[chat_id].append(msg.message_id)


@bot.message_handler(commands=['start', 'kommands'])
def main(message):
    delete_previous_messages(message.chat.id)
    bot.send_message(message.chat.id, '👋 Команды: \n📍 /location - Показать направления')
    show_main_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text.lower() in ['локации', '/location'])
def info(message):
    delete_previous_messages(message.chat.id)
    show_main_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text in category_ids.keys())
def handle_category_choice(message):
    """Обработчик выбора категории"""
    delete_previous_messages(message.chat.id)

    category_name = message.text
    category_id = category_ids[category_name]
    user_category[message.chat.id] = category_id

    show_place_types_menu(message.chat.id, category_id)


@bot.message_handler(func=lambda message: message.text in place_types.values())
def handle_place_type_choice(message):
    """Обработчик выбора типа места"""
    # Находим ключ типа по его названию
    place_type_key = None
    for key, value in place_types.items():
        if value == message.text:
            place_type_key = key
            break

    if place_type_key:
        show_places_list(message.chat.id, place_type_key, message.text)


@bot.message_handler(func=lambda message: message.text == "🔙 Назад")
def handle_back(message):
    """Обработчик кнопки Назад"""
    delete_previous_messages(message.chat.id)
    show_main_menu(message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('place_'))
def show_address_details(call):
    try:
        parts = call.data.split('_')
        category_id = parts[1]
        place_id = '_'.join(parts[2:])

        if category_id in addresses and place_id in addresses[category_id]:
            address_info = addresses[category_id][place_id]

            delete_previous_messages(call.message.chat.id)

            coordinates = address_info['coordinates']
            description = address_info['description']
            photo_url = address_info.get('photo_url')
            place_type = address_info.get('type', '')

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('🔙 Назад к списку', callback_data=f'back_to_places_{place_type}'))

            message_text = f"📍 {address_info['address']}\n\n📝 {description}"

            if photo_url:
                try:
                    photo_msg = bot.send_photo(call.message.chat.id, photo_url, caption=message_text,
                                               reply_markup=markup)
                    if call.message.chat.id not in message_ids:
                        message_ids[call.message.chat.id] = []
                    message_ids[call.message.chat.id].append(photo_msg.message_id)
                except:
                    msg = bot.send_message(call.message.chat.id, message_text, reply_markup=markup)
                    if call.message.chat.id not in message_ids:
                        message_ids[call.message.chat.id] = []
                    message_ids[call.message.chat.id].append(msg.message_id)
            else:
                msg = bot.send_message(call.message.chat.id, message_text, reply_markup=markup)
                if call.message.chat.id not in message_ids:
                    message_ids[call.message.chat.id] = []
                message_ids[call.message.chat.id].append(msg.message_id)

            if coordinates and len(coordinates) == 2:
                location_msg = bot.send_location(call.message.chat.id, coordinates[0], coordinates[1])
                if call.message.chat.id not in message_ids:
                    message_ids[call.message.chat.id] = []
                message_ids[call.message.chat.id].append(location_msg.message_id)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ Ошибка: {str(e)}")


@bot.callback_query_handler(func=lambda call: call.data.startswith('back_to_places_'))
def back_to_places(call):
    """Возврат к списку мест"""
    delete_previous_messages(call.message.chat.id)
    place_type = call.data.replace('back_to_places_', '')

    place_type_name = place_types.get(place_type, place_type)

    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    category_id = user_category.get(call.message.chat.id, 'high')

    for place_id, place_info in addresses[category_id].items():
        if place_info.get('type') == place_type:
            markup.add(InlineKeyboardButton(
                place_info['display_name'],
                callback_data=f'place_{category_id}_{place_id}'
            ))

    markup.add(InlineKeyboardButton("🔙 Назад к категориям", callback_data='back_to_types'))

    bot.send_message(call.message.chat.id, f"{place_type_name}:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_types')
def back_to_types(call):
    """Возврат к выбору типа места"""
    delete_previous_messages(call.message.chat.id)
    category_id = user_category.get(call.message.chat.id, 'high')
    show_place_types_menu(call.message.chat.id, category_id)


if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling()