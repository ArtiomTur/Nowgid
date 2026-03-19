import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Токен моего бота
bot = telebot.TeleBot('8553675239:AAFZH-jmYRp7wToM-RcNAMdhVxCizd9UBUg')

# Словарь для хранения ID единственного сообщения для каждого чата
chat_message = {}


# Функция для обновления сообщения (создает новое или редактирует существующее)
def update_message(chat_id, text, markup=None):
    if chat_id in chat_message:
        try:
            # Пытаемся отредактировать существующее сообщение
            bot.edit_message_text(
                text,
                chat_id,
                chat_message[chat_id],
                reply_markup=markup
            )
            return chat_message[chat_id]
        except:
            # Если не получилось (сообщение удалено или слишком старое) - удаляем из словаря
            del chat_message[chat_id]

    # Если нет сообщения для редактирования - отправляем новое
    msg = bot.send_message(chat_id, text, reply_markup=markup)
    chat_message[chat_id] = msg.message_id
    return msg.message_id


# Функция для обновления с фото (создает новое или редактирует текст)
def update_with_photo(chat_id, photo_url, caption, markup=None):
    # Сначала удаляем старое сообщение с фото (если есть)
    if chat_id in chat_message:
        try:
            bot.delete_message(chat_id, chat_message[chat_id])
        except:
            pass
        del chat_message[chat_id]

    # Отправляем новое фото
    msg = bot.send_photo(chat_id, photo_url, caption=caption, reply_markup=markup)
    chat_message[chat_id] = msg.message_id
    return msg.message_id


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

# Адреса по категориям (твои данные)
addresses = {
    'high': {  # Высокобюджетные маршруты
        # ПРОЖИВАНИЕ
        'high_prozhivanie_1': {
            'address': 'Отель "Волхов", адрес - ул.Предтеченская, 24 ',
            'coordinates': (58.523759, 31.265594),
            'description': 'Гостиница «Волхов» расположена в самом центре Великого Новгорода, в 5 минутах ходьбы от Кремля и основных достопримечательностей. Гостям предлагается проживание в номерах различных категорий, включая стандартные, улучшенные и люксы. \n\n В номерах есть все необходимое для комфортного проживания, включая чайник, чай, кофе, сахар, мини-бар, халаты и тапочки. В гостинице также есть спа-зона с бассейном, сауной и хаммамом, где можно расслабиться и отдохнуть.',
            'display_name': 'Отель "Волхов"',
            'photo_url': 'https://ibb.co/VcGcxV6p',
            'type': 'prozhivanie'
        },
        'high_prozhivanie_2': {
            'address': 'Гостиница "Интурист", адрес - Великая улица, 16',
            'coordinates': (58.531380, 31.280937),
            'description': 'Гостиница «Интурист» расположена на берегу реки Волхов, недалеко от Кремля и других достопримечательностей Великого Новгорода. Гостям предлагается проживание в номерах различных категорий, включая «Стандарт», «Комфорт» и «Апартаменты». \n\n В номерах есть все необходимое для комфортного проживания, включая кондиционер, холодильник, телевизор и фен. Также в гостинице есть сауна и бесплатная парковка для гостей.',
            'display_name': 'Гостиница "Интурист"',
            'photo_url': 'https://ibb.co/bMvLR42C',
            'type': 'prozhivanie'
        },
        'high_prozhivanie_3': {
            'address': 'Отель "Акрон", адрес - Предтеченская улица, 24',
            'coordinates': (58.523759, 31.265594),
            'description': 'Acron Hotel Veliky Novgorod — это пятизвездочный отель, расположенный в самом сердце Великого Новгорода. Он предлагает своим гостям комфортабельные номера, оборудованные всем необходимым, включая кофемашину Nespresso и технику Smeg. \n\n Кроме того, отель имеет собственную спа-зону с хаммамом, сауной, бассейном, тренажерным залом и залом для йоги.',
            'display_name': 'Отель "Акрон"',
            'photo_url': 'https://ibb.co/1JmKZPVm',
            'type': 'prozhivanie'
        },
        'high_prozhivanie_4': {
            'address': 'Гостиница "Береста парк", Студенческая улица, 2',
            'coordinates': (58.536543, 31.292049),
            'description': 'Гостиница «Береста Парк» расположена на берегу реки Волхов, недалеко от центра Великого Новгорода. Гостям предлагается проживание в номерах различных категорий, включая двухкомнатные люксы с гардеробной и гостиной зоной. \n\n  В номерах есть все необходимое для комфортного проживания, включая халаты, тапочки, фен, набор для чистки зубов. В стоимость проживания входит завтрак «шведский стол» и утреннее посещение спа-комплекса, который включает в себя бассейн, джакузи, сауну, хаммам и русскую баню.',
            'display_name': 'Гостиница "Береста парк"',
            'photo_url': 'https://ibb.co/23mmXzGM',
            'type': 'prozhivanie'
        },
        'high_prozhivanie_5': {
            'address': 'Гостиница "Карелинн", Большая Санкт-Петербургская улица, 21',
            'coordinates': (58.530887, 31.269340),
            'description': 'Гостиница «Карелинн» расположена в историческом центре Великого Новгорода, в 10 минутах ходьбы от Кремля. Гостям предлагаются комфортабельные номера с большими двуспальными кроватями, хорошей шумоизоляцией и напором горячей и холодной воды. \n\n В номерах есть все необходимое для комфортного проживания, включая чайник, чай, кофе и банные принадлежности. На первом этаже гостиницы находится ресторан «Фазенда», где можно позавтракать или поужинать. Также к услугам гостей бесплатная парковка.',
            'display_name': 'Гостиница «Карелинн»',
            'photo_url': 'https://ibb.co/kVvp51tx',
            'type': 'prozhivanie'
        },

        # ПИТАНИЕ
        'high_pitanie_1': {
            'address': 'Ресторан "Маруся", адрес - ул. Предтеченская, д. 24',
            'coordinates': (58.523759, 31.265594),
            'description': 'Ресторан МАРУСЯ — гастро-интеллектуальный проект, наполненный литературным вкусом, авторской кухней, театральными подачами, яркими событиями и душой. \n\n Авторская фьюжн-кухня, адаптированная под культуру Новгородской земли, вдохновлённая литературой и спектаклем у столика \nВас ждут интересные сочетания ингредиентов, обширная барная карта и разнообразное меню',
            'display_name': 'Ресторан Маруся',
            'photo_url': 'https://ibb.co/tMmvmFZB',
            'type': 'pitanie'
        },
        'high_pitanie_2': {
            'address': '"Фрегат Флагман", адрес - набережная Александра Невского, д. 22/1.',
            'coordinates': (58.520824, 31.282359),
            'description': '«Фрегат Флагман» — это ресторанный комплекс, расположенный на трехпалубном паруснике, пришвартованном у берега. Гостям предлагается разнообразное меню, включая блюда современной европейской, русской и японской кухни, а также широкий выбор алкогольных напитков и коктейлей.',
            'display_name': 'Фрегат флагман',
            'photo_url': 'https://ibb.co/qMjvgDS5',
            'type': 'pitanie'
        },
        'high_pitanie_3': {
            'address': 'Ресторан - бар "Хурма", адрес - ул. Великая, 16',
            'coordinates': (58.530878, 31.281575),
            'description': 'Ресторан осознанной гастрономии с акцентом на приготовление мяса и морепродуктов на огне \n\n Два этажа - два настроения (уютный спокойный ужин или атмосфера посиделок у большого бара — выбирать вам)',
            'display_name': 'Ресторан - бар "Хурма"',
            'photo_url': 'https://ibb.co/XxTk2H3c',
            'type': 'pitanie'
        },
        'high_pitanie_4': {
            'address': 'Кондитерская "Хочу торт", пр. Александра Корсунова, 28',
            'coordinates': (58.54594687477212, 31.240844242328947),
            'description': 'Сеть кондитерских «ХочуТорт»- это современные кондитерские рядом с вашим домом. Мы рады предложить вам свадебные торты, бисквитные, муссовые торты, чизкейки и капкейки, пряники, макарон и другие десерты на заказ.',
            'display_name': 'Кондитерская "Хочу торт"',
            'photo_url': 'https://ibb.co/1fQTbLcH',
            'type': 'pitanie'
        },
        'high_pitanie_5': {
            'address': 'Большая Санкт-Петербургская ул., 23, Великий Новгород',
            'coordinates': (58.531592, 31.269070),
            'description': 'Ресторан «Пряник» — это уютное место с несколькими залами и верандой, где можно насладиться живой музыкой и диджей-сетами. \n\n В меню представлены традиционные русские блюда, такие как борщ, солянка, щи «Крошево» и пельмени с сулугуни, а также грузинские блюда, такие как хачапури по-Аджарски. Гости отмечают, что кухня ресторана отличается качеством продуктов и мастерством поваров.',
            'display_name': 'Ресторан "Пряник"',
            'photo_url': 'https://ibb.co/8gv0gjQy',
            'type': 'pitanie'
        },

        # БЕСПЛАТНЫЕ
        'high_besplatnie_1': {
            'address': 'Заглушка адреса для бесплатных 1',
            'coordinates': None,
            'description': 'Заглушка описания для бесплатных 1',
            'display_name': 'Заглушка Бесплатные 1',
            'photo_url': None,
            'type': 'besplatnie'
        },

        # ПЛАТНЫЕ
        'high_platnie_1': {
            'address': 'Заглушка адреса для платных 1',
            'coordinates': None,
            'description': 'Заглушка описания для платных 1',
            'display_name': 'Заглушка Платные 1',
            'photo_url': None,
            'type': 'platnie'
        },
    },

    'low': {  # Малобюджетные маршруты
        # ПРОЖИВАНИЕ
        'low_prozhivanie_1': {
            'address': 'хостел "турист", Адрес: ул. розважа, 11/1',
            'coordinates': (58.525747, 31.276239),
            'description': 'Хостел «Турист» находится в центре города. В номерах — двухъярусные кровати, мягкий инвентарь, письменный столик, полочки, вешалка, ящички под ключ. В хостеле есть обеденная зона с холодильником, СВЧ, термопотом и кулером для воды, а также ТВ. Предусмотрены две душевые и четыре туалета. Парковка находится в 30 метрах от хостела. Заезд после 14:00, выезд до 12:00. Стойка регистрации работает круглосуточно. Предоставляются гладильные принадлежности. Есть аптечка первой помощи.\n\nРядом — Кремль, Софийский собор, Софийская площадь, набережная реки Волхов. В Кремлёвском парке есть детские площадки, летом появляются батуты и аттракционы. Неподалёку — Соколиный двор с хищными птицами.',
            'display_name': 'Хостел "Турист"',
            'photo_url': 'https://ibb.co/8DQsjpHD',
            'type': 'prozhivanie'
        },
        'low_prozhivanie_2': {
            'address': 'Бм-хостел, адрес - Большая Санкт-Петербургская ул., 14',
            'coordinates': (58.529374, 31.271711),
            'description': 'Этот хостел расположен в центре города, недалеко от кремля и главных достопримечательностей. Гости особенно выделяют чистые номера с удобствами, такими как туалеты и душевые. Также здесь есть общие кухни для самостоятельного приготовления еды. Судя по отзывам, это отличное место для проживания во время путешествия или отдыха в Новгороде.',
            'display_name': 'Бм-Хостел',
            'photo_url': 'https://ibb.co/C55MY2Dx',
            'type': 'prozhivanie'
        },
        'low_prozhivanie_3': {
            'address': 'Гостевой дом "Орловский дом", адрес - Орловский пер., 5/8, Псковский район',
            'coordinates': (58.512710, 31.257312),
            'description': 'Жильё «Орловский» предлагает комфортное проживание. В комнатах — бесплатный Wi-Fi. Есть комнаты с общей ванной комнатой и с собственным санузлом, оборудованным душевой кабиной. \n\n В комнатах — кровати с ортопедическим матрасом, холодильник, чайник. На территории — бесплатная парковка под камерами, зона барбекю, терраса со столиками под навесом. Действует бесконтактная система заселения. Рядом — сетевые магазины.',
            'display_name': 'Гостевой дом "Орловский дом"',
            'photo_url': 'https://ibb.co/C55MY2Dx',
            'type': 'prozhivanie'
        },
        'low_prozhivanie_4': {
            'address': 'Хостел "Академ ВН", адрес - улица Саши Устинова, 3/1',
            'coordinates': (58.540719, 31.258057),
            'description': 'Хостел «Академ ВН» предлагает своим гостям чистые и уютные номера с удобными кроватями и индивидуальным освещением. В номерах есть все необходимое для комфортного проживания, включая вешалки, подставки для обуви, прикроватные коврики и розетки. \n\n Кроме того, в хостеле есть общая кухня с холодильником, микроволновой печью, посудой и приборами, а также душевая с феном. ',
            'display_name': 'Хостел "Академ ВН"',
            'photo_url': 'https://ibb.co/7xq3NBxq',
            'type': 'prozhivanie'
        },
        'low_prozhivanie_5': {
            'address': 'Хостел "sleep & go", адрес - улица Черемнова-Конюхова, 8',
            'coordinates': (58.528496, 31.292274),
            'description': 'Хостел «Слип энд ГОУ» расположен в центре исторической части города, рядом протекает река Волхов. Вокруг много уютных кафе и интересных достопримечательностей. Очень удобно добираться пешком до основных туристических мест города. \n\n В номерах чисто и аккуратно, постельное бельё свежее, кровати удобные. Есть общая кухня, где можно приготовить еду самостоятельно. Персонал приветливый и внимательный, всегда готов помочь с информацией о городе и достопримечательностях. Регулярно проводится уборка помещений.',
            'display_name': 'Хостел "sleep & go"',
            'photo_url': 'https://ibb.co/fdsfYCxJ',
            'type': 'prozhivanie'
        },

        # ПИТАНИЕ
        'low_pitanie_1': {
            'address': 'ресторан быстрого питания "чайная ложка", Адрес: большая санкт петербургская, 25 в ТЦ "Русь"',
            'coordinates': (58.533020, 31.267274),
            'description': 'Описание для ресторана',
            'display_name': 'Чайная ложка',
            'photo_url': 'https://ibb.co/4nTmZZQQ',
            'type': 'pitanie'
        },
        'low_pitanie_2': {
            'address': 'Кофейня "В шкафу", Адрес: Большая Санкт-Петербургская улица, 5/1',
            'coordinates': (58.526917, 31.272780),
            'description': '«Кофейня в Шкафу» — это уютное семейное кафе, где вы можете насладиться ароматным кофе и попробовать вкусные десерты, такие как запечённая рикотта, яблочный штрудель и маковый десерт.',
            'display_name': 'Кофейня "В шкафу"',
            'photo_url': 'https://ibb.co/35SKw5nT',
            'type': 'pitanie'
        },
        'low_pitanie_3': {
            'address': 'столовая нтш "блок питания", Адрес: ул. Великая, 18а',
            'coordinates': (58.538525, 31.278664),
            'description': '«Столовая «Блок Питания» — это место, где вы можете насладиться вкусной и разнообразной едой по доступным ценам. Здесь вы найдете завтраки, обеды и ужины, а также широкий выбор блюд, таких как супы, салаты, горячие блюда и десерты.',
            'display_name': 'Столовая "НТШ"',
            'photo_url': 'https://ibb.co/sdyCRn48',
            'type': 'pitanie'
        },
        'low_pitanie_4': {
            'address': 'столовая  "Борщи", Адрес: Большая Санкт-Петербургская улица, 5/1',
            'coordinates': (58.526917, 31.272780),
            'description': 'Столовая «Борщи» — это уютное заведение, расположенное недалеко от исторического центра Великого Новгорода. \n\n Гостям нравится разнообразное меню, которое включает в себя супы, вторые блюда, салаты и выпечку. Кроме того, посетители отмечают большие порции и доступные цены.',
            'display_name': 'Столовая "Борщи"',
            'photo_url': 'https://ibb.co/SXndmTWy',
            'type': 'pitanie'
        },

        # БЕСПЛАТНЫЕ
        'low_besplatnie_1': {
            'address': 'Прогулка по кремлю и набережной',
            'coordinates': None,
            'description': 'Прогулка по кремлю и по набережной Александра Невского',
            'display_name': 'Прогулка',
            'photo_url': None,
            'type': 'besplatnie'
        },
        'low_besplatnie_2': {
            'address': 'Заглушка адреса для бесплатных 2',
            'coordinates': None,
            'description': 'Заглушка описания для бесплатных 2',
            'display_name': 'Бесплатно (вариант 2)',
            'photo_url': None,
            'type': 'besplatnie'
        },

        # ПЛАТНЫЕ
        'low_platnie_1': {
            'address': 'территория Кремля, 14а.',
            'coordinates': (58.522660, 31.275844),
            'description': 'Экскурсия по грановитой палате',
            'display_name': 'Грановитая палата',
            'photo_url': None,
            'type': 'platnie'
        },
        'low_platnie_2': {
            'address': 'Заглушка адреса для платных 2',
            'coordinates': None,
            'description': 'Заглушка описания для платных 2',
            'display_name': 'Платно (вариант 2)',
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
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for category_name in category_ids.keys():
        category_id = category_ids[category_name]
        markup.add(InlineKeyboardButton(category_name, callback_data=f'cat_{category_id}'))

    update_message(message.chat.id, 'Наши направления:', markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('cat_'))
def show_place_types(call):
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

    update_message(call.message.chat.id, f'Выберите категорию:', markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('type_'))
def show_places_by_type(call):
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

    update_message(call.message.chat.id, f'{type_display_name}:', markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('place_'))
def show_address_details(call):
    try:
        # Разделяем данные
        parts = call.data.split('_')
        category_id = parts[1]
        place_id = '_'.join(parts[2:])

        if category_id in addresses and place_id in addresses[category_id]:
            address_info = addresses[category_id][place_id]

            coordinates = address_info['coordinates']
            description = address_info['description']
            photo_url = address_info.get('photo_url')
            place_type = address_info.get('type', '')

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('Назад', callback_data=f'type_{category_id}_{place_type}'))

            message_text = f"📍 {address_info['address']}\n\n📝 {description}"

            if photo_url:
                # Для фото всегда создаем новое сообщение (удаляем старое)
                update_with_photo(call.message.chat.id, photo_url, message_text, markup)
            else:
                # Для текста - редактируем
                update_message(call.message.chat.id, message_text, markup)

            if coordinates and len(coordinates) == 2 and coordinates[0] is not None and coordinates[1] is not None:
                # Отправляем локацию отдельно (её нельзя встроить в сообщение)
                bot.send_location(call.message.chat.id, latitude=coordinates[0], longitude=coordinates[1])
    except Exception as e:
        bot.send_message(call.message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте снова.")


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_categories')
def back_to_categories(call):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    for category_name in category_ids.keys():
        category_id = category_ids[category_name]
        markup.add(InlineKeyboardButton(category_name, callback_data=f'cat_{category_id}'))

    update_message(call.message.chat.id, 'Наши направления:', markup)


if __name__ == '__main__':
    print("Бот запущен в режиме одного сообщения...")
    bot.polling()