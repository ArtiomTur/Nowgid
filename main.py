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

# Типы мест (для второго уровня меню)
place_types = {
    'prozhivanie': '🏨 Проживание',
    'pitanie': '🍽️ Питание',
    'besplatnie': '🚶 Бесплатные развлечения',
    'platnie': '🎟️ Платные развлечения'
}

# Адреса по категориям
addresses = {
    'high': {  # Высокобюджетные маршруты (ЗАГЛУШКИ)
        'prozhivanie_1': {
            'address': 'Заглушка адреса для проживания 1',
            'coordinates': None,
            'description': 'Заглушка описания для проживания 1',
            'display_name': 'Заглушка Проживание 1',
            'photo_url': None,
            'type': 'prozhivanie'
        },
        'prozhivanie_2': {
            'address': 'Заглушка адреса для проживания 2',
            'coordinates': None,
            'description': 'Заглушка описания для проживания 2',
            'display_name': 'Заглушка Проживание 2',
            'photo_url': None,
            'type': 'prozhivanie'
        },
        'pitanie_1': {
            'address': 'Ресторан "Маруся", адрес - ул. Предтеченская, д. 24',
            'coordinates': (58.523759, 31.265594),
            'description': 'Ресторан МАРУСЯ — гастро-интеллектуальный проект, наполненный литературным вкусом, авторской кухней, театральными подачами, яркими событиями и душой. \n\n Авторская фьюжн-кухня, адаптированная под культуру Новгородской земли, вдохновлённая литературой и спектаклем у столика \nВас ждут интересные сочетания ингредиентов, обширная барная карта и разнообразное меню',
            'display_name': 'Ресторан Маруся',
            'photo_url': 'https://ibb.co/tMmvmFZB',
            'type': 'pitanie'
        },
        'pitanie_2': {
            'address': ' "Фрегат Флагман", адрес - набережная Александра Невского, д. 22/1.',
            'coordinates': (58.520824, 31.282359),
            'description': '«Фрегат Флагман» — это ресторанный комплекс, расположенный на трехпалубном паруснике, пришвартованном у берега. Гостям предлагается разнообразное меню, включая блюда современной европейской, русской и японской кухни, а также широкий выбор алкогольных напитков и коктейлей.',
            'display_name': 'Фрегат флагман',
            'photo_url': 'https://ibb.co/qMjvgDS5',
            'type': 'pitanie'

        },
        'pitanie_3': {
            'address': 'Ресторан - бар "Хурма, адрес -  ул. Великая, 16',
            'coordinates': (58.530878, 31.281575),
            'description': 'Ресторан осознанной гастрономии с акцентом на приготовление мяса и морепродуктов на огне \n\n Два этажа - два настроения (уютный спокойный ужин или атмосфера посиделок у большого бара — выбирать вам)',
            'display_name': 'Ресторан - бар "Хурма"',
            'photo_url': 'https://ibb.co/XxTk2H3c',
            'type': 'pitanie'

        },
        'pitanie_4': {
            'address': 'Кондитерская "Хочу торт", пр. Александра Корсунова, 28',
            'coordinates': (58.54594687477212, 31.240844242328947),
            'description': 'Сеть кондитерских «ХочуТорт»- это современные кондитерские рядом с вашим домом. Мы рады предложить вам свадебные торты, бисквитные, муссовые торты, чизкейки и капкейки, пряники, макарон и другие десерты на заказ.',
            'display_name': 'Кондитерская "Хочу торт"',
            'photo_url': 'https://ibb.co/1fQTbLcH',
            'type': 'pitanie'

        },

        'pitanie_5': {
            'address': ', Большая Санкт-Петербургская ул., 23, Великий Новгород',
            'coordinates': (58.531592, 31.269070),
            'description': 'Ресторан «Пряник» — это уютное место с несколькими залами и верандой, где можно насладиться живой музыкой и диджей-сетами. \n\n В меню представлены традиционные русские блюда, такие как борщ, солянка, щи «Крошево» и пельмени с сулугуни, а также грузинские блюда, такие как хачапури по-Аджарски. Гости отмечают, что кухня ресторана отличается качеством продуктов и мастерством поваров.',
            'display_name': 'Ресторан "Прияник"',
            'photo_url': 'https://ibb.co/8gv0gjQy',
            'type': 'pitanie'

        },


        'besplatnie_1': {
            'address': 'Заглушка адреса для бесплатных 1',
            'coordinates': None,
            'description': 'Заглушка описания для бесплатных 1',
            'display_name': 'Заглушка Бесплатные 1',
            'photo_url': None,
            'type': 'besplatnie'
        },
        'platnie_1': {
            'address': 'Заглушка адреса для платных 1',
            'coordinates': None,
            'description': 'Заглушка описания для платных 1',
            'display_name': 'Заглушка Платные 1',
            'photo_url': None,
            'type': 'platnie'
        },
    },
    'low': {  # Малобюджетные маршруты (ТВОИ ДАННЫЕ + ЗАГЛУШКИ)
        # ТВОИ РЕАЛЬНЫЕ МЕСТА
        'hoztel': {
            'address': 'хостел "турист", Адрес: ул. розважа, 11/1',
            'coordinates': (58.525747, 31.276239),
            'description': 'Хостел «Турист» находится в центре города. В номерах — двухъярусные кровати, мягкий инвентарь, письменный столик, полочки, вешалка, ящички под ключ. В хостеле есть обеденная зона с холодильником, СВЧ, термопотом и кулером для воды, а также ТВ. Предусмотрены две душевые и четыре туалета. Парковка находится в 30 метрах от хостела. Заезд после 14:00, выезд до 12:00. Стойка регистрации работает круглосуточно. Предоставляются гладильные принадлежности. Есть аптечка первой помощи.\n\nРядом — Кремль, Софийский собор, Софийская площадь, набережная реки Волхов. В Кремлёвском парке есть детские площадки, летом появляются батуты и аттракционы. Неподалёку — Соколиный двор с хищными птицами.',
            'display_name': 'Хостел "Турист"',
            'photo_url': 'https://ibb.co/8DQsjpHD',
            'type': 'prozhivanie'
        },
        'chainaya_lozhka': {
            'address': 'ресторан быстрого питания "чайная ложка", Адрес: большая санкт петербургская, 25 в ТЦ "Русь"',
            'coordinates': (58.533020, 31.267274),
            'description': 'Описание для ресторана',
            'display_name': 'Чайная ложка',
            'photo_url': 'https://ibb.co/4nTmZZQQ',
            'type': 'pitanie'
        },
        'progulka': {
            'address': 'Прогулка по кремлю и набережной',
            'coordinates': None,
            'description': 'Прогулка по кремлю и по набережной Александра Невского',
            'display_name': 'Прогулка',
            'photo_url': None,
            'type': 'besplatnie'
        },
        'kreml': {
            'address': 'территория Кремля, 14а.',
            'coordinates': (58.522660, 31.275844),
            'description': 'Экскурсия по грановитой палате',
            'display_name': 'Грановитая палата',
            'photo_url': None,
            'type': 'platnie'
        },

        # ЗАГЛУШКИ
        'prozhivanie_zaglushka': {
            'address': 'Заглушка адреса для проживания',
            'coordinates': None,
            'description': 'Заглушка описания для проживания',
            'display_name': 'Проживание (заглушка)',
            'photo_url': None,
            'type': 'prozhivanie'
        },
        'pitanie_zaglushka': {
            'address': 'Заглушка адреса для питания',
            'coordinates': None,
            'description': 'Заглушка описания для питания',
            'display_name': 'Питание (заглушка)',
            'photo_url': None,
            'type': 'pitanie'
        },
        'besplatnie_zaglushka': {
            'address': 'Заглушка адреса для бесплатных',
            'coordinates': None,
            'description': 'Заглушка описания для бесплатных',
            'display_name': 'Бесплатно (заглушка)',
            'photo_url': None,
            'type': 'besplatnie'
        },
        'platnie_zaglushka': {
            'address': 'Заглушка адреса для платных',
            'coordinates': None,
            'description': 'Заглушка описания для платных',
            'display_name': 'Платно (заглушка)',
            'photo_url': None,
            'type': 'platnie'
        }
    }
}


@bot.message_handler(commands=['start', 'kommands'])
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
    for place_id, place_info in addresses[category_id].items():
        if place_info.get('type') == place_type:
            markup.add(InlineKeyboardButton(
                place_info['display_name'],
                callback_data=f'place_{category_id}_{place_id}'
            ))
            type_display_name = place_types.get(place_type, place_type)

    markup.add(InlineKeyboardButton('Назад', callback_data=f'cat_{category_id}'))
    msg = bot.send_message(call.message.chat.id, f'{type_display_name}:', reply_markup=markup)

    if call.message.chat.id not in message_ids:
        message_ids[call.message.chat.id] = []
    message_ids[call.message.chat.id].append(msg.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('place_'))
def show_address_details(call):
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

            if coordinates and len(coordinates) == 2 and coordinates[0] is not None and coordinates[1] is not None:
                location_msg = bot.send_location(call.message.chat.id, latitude=coordinates[0],
                                                 longitude=coordinates[1])
                if call.message.chat.id not in message_ids:
                    message_ids[call.message.chat.id] = []
                message_ids[call.message.chat.id].append(location_msg.message_id)
    except Exception as e:
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
    bot.polling()