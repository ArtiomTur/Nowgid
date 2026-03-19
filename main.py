import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Токен моего бота - УБЕДИСЬ ЧТО ОН ПРАВИЛЬНЫЙ!
bot = telebot.TeleBot('8553675239:AAFZH-jmYRp7wToM-RcNAMdhVxCizd9UBUg')

# Словарь для хранения идентификаторов сообщений
message_ids = {}


# Функция для удаления предыдущих сообщений
def delete_previous_messages(chat_id):
    if chat_id in message_ids:
        for msg_id in message_ids[chat_id]:
            try:
                bot.delete_message(chat_id, msg_id)
            except Exception:
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

# Исправленные ссылки на изображения (примеры)
addresses = {
    'high': {  # Высокобюджетные маршруты
        # ПРОЖИВАНИЕ
        'high_prozhivanie_1': {
            'address': 'Отель "Волхов", адрес - ул.Предтеченская, 24 ',
            'coordinates': (58.523759, 31.265594),
            'description': 'Гостиница «Волхов» расположена в самом центре Великого Новгорода, в 5 минутах ходьбы от Кремля и основных достопримечательностей. Гостям предлагается проживание в номерах различных категорий, включая стандартные, улучшенные и люксы. \n\n В номерах есть все необходимое для комфортного проживания, включая чайник, чай, кофе, сахар, мини-бар, халаты и тапочки. В гостинице также есть спа-зона с бассейном, сауной и хаммамом, где можно расслабиться и отдохнуть.',
            'display_name': 'Отель "Волхов"',
            'photo_url': None,  # Временно убираем фото до исправления ссылок
            'type': 'prozhivanie'
        },
        # ... остальные данные (временно без фото или с правильными прямыми ссылками)
    },
    'low': {  # Малобюджетные маршруты
        # ПРОЖИВАНИЕ
        'low_prozhivanie_1': {
            'address': 'хостел "турист", Адрес: ул. розважа, 11/1',
            'coordinates': (58.525747, 31.276239),
            'description': 'Хостел «Турист» находится в центре города. В номерах — двухъярусные кровати, мягкий инвентарь, письменный столик, полочки, вешалка, ящички под ключ. В хостеле есть обеденная зона с холодильником, СВЧ, термопотом и кулером для воды, а также ТВ. Предусмотрены две душевые и четыре туалета. Парковка находится в 30 метрах от хостела. Заезд после 14:00, выезд до 12:00. Стойка регистрации работает круглосуточно. Предоставляются гладильные принадлежности. Есть аптечка первой помощи.\n\nРядом — Кремль, Софийский собор, Софийская площадь, набережная реки Волхов. В Кремлёвском парке есть детские площадки, летом появляются батуты и аттракционы. Неподалёку — Соколиный двор с хищными птицами.',
            'display_name': 'Хостел "Турист"',
            'photo_url': None,  # Временно убираем фото до исправления ссылок
            'type': 'prozhivanie'
        },
        # ... остальные данные
    }
}


@bot.message_handler(commands=['start', 'commands'])  # Исправлено: kommands -> commands
def main(message):
    bot.send_message(message.chat.id,
                     'Команды для данного бота: \nлокации или /location - Показывает наши направления')


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
def show_place_types(call):
    delete_previous_messages(call.message.chat.id)
    category_id = call.data.split('_')[1]
    category_name = id_to_category[category_id]

    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    # Показываем типы мест
    for type_key, type_name in place_types.items():
        markup.add(InlineKeyboardButton(
            type_name,
            callback_data=f'type_{category_id}_{type_key}'
        ))

    markup.add(InlineKeyboardButton('Назад', callback_data='back_to_categories'))
    msg = bot.send_message(call.message.chat.id, f'Выберите категорию:', reply_markup=markup)

    if call.message.chat.id not in message_ids:
        message_ids[call.message.chat.id] = []
    message_ids[call.message.chat.id].append(msg.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('type_'))
def show_places_by_type(call):
    delete_previous_messages(call.message.chat.id)
    _, category_id, place_type = call.data.split('_')

    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    # Показываем все места выбранного типа
    type_display_name = ""
    found_places = False

    for place_id, place_info in addresses[category_id].items():
        if place_info.get('type') == place_type:
            markup.add(InlineKeyboardButton(
                place_info['display_name'],
                callback_data=f'place_{category_id}_{place_id}'
            ))
            type_display_name = place_types.get(place_type, place_type)
            found_places = True

    if not found_places:
        markup.add(InlineKeyboardButton('❌ Нет мест в этой категории', callback_data='no_action'))

    markup.add(InlineKeyboardButton('Назад', callback_data=f'cat_{category_id}'))
    msg = bot.send_message(call.message.chat.id, f'{type_display_name}:', reply_markup=markup)

    if call.message.chat.id not in message_ids:
        message_ids[call.message.chat.id] = []
    message_ids[call.message.chat.id].append(msg.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('place_'))
def show_address_details(call):
    if call.data == 'no_action':
        bot.answer_callback_query(call.id, "Нет доступных мест")
        return

    try:
        # Разделяем данные
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
            markup.add(InlineKeyboardButton('Назад', callback_data=f'type_{category_id}_{place_type}'))

            message_text = f"📍 {address_info['address']}\n\n📝 {description}"

            # Отправляем сообщение с фото или без
            if photo_url:
                try:
                    photo_msg = bot.send_photo(call.message.chat.id, photo_url, caption=message_text,
                                               reply_markup=markup)
                    if call.message.chat.id not in message_ids:
                        message_ids[call.message.chat.id] = []
                    message_ids[call.message.chat.id].append(photo_msg.message_id)
                except Exception as e:
                    print(f"Ошибка при отправке фото: {e}")
                    msg = bot.send_message(call.message.chat.id, message_text, reply_markup=markup)
                    if call.message.chat.id not in message_ids:
                        message_ids[call.message.chat.id] = []
                    message_ids[call.message.chat.id].append(msg.message_id)
            else:
                msg = bot.send_message(call.message.chat.id, message_text, reply_markup=markup)
                if call.message.chat.id not in message_ids:
                    message_ids[call.message.chat.id] = []
                message_ids[call.message.chat.id].append(msg.message_id)

            # Отправляем координаты если есть
            if coordinates and len(coordinates) == 2 and coordinates[0] is not None and coordinates[1] is not None:
                location_msg = bot.send_location(call.message.chat.id, latitude=coordinates[0],
                                                 longitude=coordinates[1])
                if call.message.chat.id not in message_ids:
                    message_ids[call.message.chat.id] = []
                message_ids[call.message.chat.id].append(location_msg.message_id)
    except Exception as e:
        print(f"Ошибка в show_address_details: {e}")
        bot.send_message(call.message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте снова.")


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
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")