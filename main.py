import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

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
            except Exception:
                pass
        message_ids[chat_id] = []


# Сокращённые идентификаторы для callback_data
category_ids = {
    'Высокобюджетные варианты': 'high',
    'Малобюджетные варианты': 'low'
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

# Адреса по категориям с ЦЕНАМИ и РАЗВЛЕЧЕНИЯМИ
addresses = {
    'high': {
        # ========== ПРОЖИВАНИЕ ==========
        'high_prozhivanie_1': {
            'address': 'Отель "Волхов", ул. Предтеченская, 24',
            'coordinates': (58.523759, 31.265594),
            'description': '🏨 Отель «Волхов» в центре города, 5 минут до Кремля.\n\n💰 Цены за номер в сутки:\n• Стандарт (1-местный) — от 5 500 ₽\n• Стандарт (2-местный) — от 6 500 ₽\n• Улучшенный — от 7 500 ₽\n• Люкс — от 10 000 ₽\n\n✅ В номерах: чайник, чай/кофе, мини-бар, халаты, тапочки.\n✅ Спа-зона с бассейном, сауной, хаммамом.',
            'display_name': 'Отель "Волхов"',
            'photo_url': None,
            'type': 'prozhivanie'
        },
        'high_prozhivanie_2': {
            'address': 'Гостиница "Интурист", Великая улица, 16',
            'coordinates': (58.531380, 31.280937),
            'description': '🏨 Гостиница «Интурист» на берегу реки Волхов, недалеко от Кремля.\n\n💰 Цены за номер в сутки:\n• Стандарт — от 4 800 ₽\n• Комфорт — от 6 000 ₽\n• Апартаменты — от 8 500 ₽\n\n✅ В номерах: кондиционер, холодильник, ТВ, фен.\n✅ Сауна, бесплатная парковка.',
            'display_name': 'Гостиница "Интурист"',
            'photo_url': None,
            'type': 'prozhivanie'
        },
        'high_prozhivanie_3': {
            'address': 'Отель "Акрон", Предтеченская улица, 24',
            'coordinates': (58.523759, 31.265594),
            'description': '🏨 Acron Hotel — пятизвездочный отель в сердце Великого Новгорода.\n\n💰 Цены за номер в сутки:\n• Стандарт — от 10 000 ₽\n• Бизнес — от 15 000 ₽\n• Люкс — от 25 000 ₽\n\n✅ В номерах: кофемашина Nespresso, техника Smeg.\n✅ Спа-зона: хаммам, сауна, бассейн, тренажёрный зал, зал для йоги.',
            'display_name': 'Отель "Акрон"',
            'photo_url': None,
            'type': 'prozhivanie'
        },
        'high_prozhivanie_4': {
            'address': 'Гостиница "Береста парк", Студенческая улица, 2',
            'coordinates': (58.536543, 31.292049),
            'description': '🏨 Гостиница «Береста Парк» на берегу реки Волхов.\n\n💰 Цены за номер в сутки:\n• Стандарт — от 7 000 ₽\n• Полулюкс — от 9 000 ₽\n• Двухкомнатный люкс — от 12 000 ₽\n\n✅ В номерах: халаты, тапочки, фен, набор для чистки зубов.\n✅ В стоимость входит завтрак «шведский стол» и спа-комплекс (бассейн, джакузи, сауна, хаммам, русская баня).',
            'display_name': 'Гостиница "Береста парк"',
            'photo_url': None,
            'type': 'prozhivanie'
        },
        'high_prozhivanie_5': {
            'address': 'Гостиница "Карелинн", Большая Санкт-Петербургская ул., 21',
            'coordinates': (58.530887, 31.269340),
            'description': '🏨 Гостиница «Карелинн» в историческом центре, 10 минут до Кремля.\n\n💰 Цены за номер в сутки:\n• Стандарт — от 4 500 ₽\n• Улучшенный — от 5 800 ₽\n• Семейный — от 7 000 ₽\n\n✅ В номерах: чайник, чай/кофе, банные принадлежности.\n✅ На первом этаже ресторан «Фазенда».\n✅ Бесплатная парковка.',
            'display_name': 'Гостиница «Карелинн»',
            'photo_url': None,
            'type': 'prozhivanie'
        },

        # ========== ПИТАНИЕ ==========
        'high_pitanie_1': {
            'address': 'Ресторан "Маруся", ул. Предтеченская, 24',
            'coordinates': (58.523759, 31.265594),
            'description': '🍽️ Ресторан МАРУСЯ — гастро-интеллектуальный проект.\n\n💰 Средний чек: 2 500 - 3 500 ₽\n\nАвторская фьюжн-кухня, театральные подачи, обширная барная карта.',
            'display_name': 'Ресторан Маруся',
            'photo_url': None,
            'type': 'pitanie'
        },
        'high_pitanie_2': {
            'address': '"Фрегат Флагман", наб. Александра Невского, 22/1',
            'coordinates': (58.520824, 31.282359),
            'description': '🍽️ Ресторан на трёхпалубном паруснике у берега.\n\n💰 Средний чек: 2 000 - 3 000 ₽\n\nМеню: европейская, русская, японская кухня. Широкий выбор напитков и коктейлей.',
            'display_name': 'Фрегат флагман',
            'photo_url': None,
            'type': 'pitanie'
        },
        'high_pitanie_3': {
            'address': 'Ресторан-бар "Хурма", ул. Великая, 16',
            'coordinates': (58.530878, 31.281575),
            'description': '🍽️ Ресторан осознанной гастрономии.\n\n💰 Средний чек: 2 000 - 3 000 ₽\n\nАкцент на приготовление мяса и морепродуктов на огне. Два этажа — два настроения.',
            'display_name': 'Ресторан-бар "Хурма"',
            'photo_url': None,
            'type': 'pitanie'
        },
        'high_pitanie_4': {
            'address': 'Кондитерская "Хочу торт", пр. Александра Корсунова, 28',
            'coordinates': (58.54594687477212, 31.240844242328947),
            'description': '🍰 Современные кондитерские.\n\n💰 Средний чек: 500 - 1 000 ₽\n\nСвадебные торты, бисквитные и муссовые торты, чизкейки, капкейки, пряники, макарон.',
            'display_name': 'Кондитерская "Хочу торт"',
            'photo_url': None,
            'type': 'pitanie'
        },
        'high_pitanie_5': {
            'address': 'Ресторан "Пряник", Большая Санкт-Петербургская ул., 23',
            'coordinates': (58.531592, 31.269070),
            'description': '🍽️ Уютное место с верандой, живой музыкой.\n\n💰 Средний чек: 1 500 - 2 500 ₽\n\nВ меню: русские блюда (борщ, солянка, щи, пельмени) и грузинские (хачапури).',
            'display_name': 'Ресторан "Пряник"',
            'photo_url': None,
            'type': 'pitanie'
        },

        # ========== БЕСПЛАТНЫЕ РАЗВЛЕЧЕНИЯ ==========
        'high_besplatnie_1': {
            'address': 'Новгородский Кремль (Детинец)',
            'coordinates': None,
            'description': '🏰 Бесплатный вход на территорию Кремля!\n\n📍 Древняя крепость XI века.\n📍 Софийский собор — древнейший храм России.\n📍 Памятник «Тысячелетие России».\n\n✅ Идеально для прогулки и красивых фото.',
            'display_name': 'Новгородский Кремль',
            'photo_url': None,
            'type': 'besplatnie'
        },
        'high_besplatnie_2': {
            'address': 'Ярославово Дворище и Древний Торг',
            'coordinates': None,
            'description': '🏛️ Бесплатная прогулка по Торговой стороне.\n\n📍 Ганзейский фонтан.\n📍 Древние церкви XII-XIII веков.\n📍 Место, где проходили древние торги.\n\n✅ Очень атмосферное место!',
            'display_name': 'Ярославово Дворище',
            'photo_url': None,
            'type': 'besplatnie'
        },
        'high_besplatnie_3': {
            'address': 'Набережная Александра Невского',
            'coordinates': None,
            'description': '🌊 Прогулка по набережной с видом на Кремль и реку Волхов.\n\n📍 Красивые виды.\n📍 Место для фото.\n📍 Рядом — памятник Александру Невскому.\n\n✅ Отличное место для вечерней прогулки.',
            'display_name': 'Набережная Александра Невского',
            'photo_url': None,
            'type': 'besplatnie'
        },
        'high_besplatnie_4': {
            'address': 'Памятник «Тысячелетие России»',
            'coordinates': None,
            'description': '🗿 Знаменитый памятник внутри Кремля.\n\n📍 Установлен в 1862 году.\n📍 На барельефах — 109 исторических деятелей.\n📍 Символ единства России.\n\n✅ Можно осмотреть бесплатно (вход на территорию Кремля свободный).',
            'display_name': 'Памятник "Тысячелетие России"',
            'photo_url': None,
            'type': 'besplatnie'
        },
        'high_besplatnie_5': {
            'address': 'Софийская площадь',
            'coordinates': None,
            'description': '🏛️ Главная площадь Великого Новгорода.\n\n📍 Перед входом в Кремль.\n📍 Памятник Ленину.\n📍 Место проведения городских праздников.\n\n✅ Отличное место для начала прогулки по городу.',
            'display_name': 'Софийская площадь',
            'photo_url': None,
            'type': 'besplatnie'
        },

        # ========== ПЛАТНЫЕ РАЗВЛЕЧЕНИЯ ==========
        'high_platnie_1': {
            'address': 'Грановитая палата, Кремль, 14а',
            'coordinates': (58.522660, 31.275844),
            'description': '🎟️ Экскурсия по Грановитой палате.\n\n💰 Цена: от 500 ₽ (взрослый билет)\n\nОдин из символов Великого Новгорода. Интерьеры, где проходили важные исторические события.\n\n✅ Обязательно к посещению!',
            'display_name': 'Грановитая палата',
            'photo_url': None,
            'type': 'platnie'
        },
        'high_platnie_2': {
            'address': 'Музей деревянного зодчества «Витославлицы»',
            'coordinates': None,
            'description': '🏡 Уникальный музей под открытым небом.\n\n💰 Цена: от 300 ₽\n\nСтаринные деревянные постройки XVI–XX веков. Предметы быта, церкви, избы.\n\n✅ Трансфер от Кремля на автобусе №7.',
            'display_name': 'Витославлицы',
            'photo_url': None,
            'type': 'platnie'
        },
        'high_platnie_3': {
            'address': 'Софийский собор (внутри)',
            'coordinates': None,
            'description': '⛪ Древнейший каменный храм России (1045–1050 гг.)\n\n💰 Цена: от 300 ₽ (вход в собор)\n\nЗнаменитые Магдебургские врата, древние фрески, мощи святых.\n\n✅ Территория Кремля — бесплатно, вход в собор — платный.',
            'display_name': 'Софийский собор',
            'photo_url': None,
            'type': 'platnie'
        },
        'high_platnie_4': {
            'address': 'Теплоходная прогулка по Волхову',
            'coordinates': None,
            'description': '🛥️ Прогулка по реке Волхов.\n\n💰 Цена: от 800 ₽ (взрослый), от 500 ₽ (детский)\n\nДлительность: 1 час.\n\n📍 Отправление от причала у Кремля.\n\n✅ Красивые виды на город и Кремль с воды.',
            'display_name': 'Теплоходная прогулка',
            'photo_url': None,
            'type': 'platnie'
        },
        'high_platnie_5': {
            'address': 'Экскурсия «Мир фресок Великого Новгорода»',
            'coordinates': None,
            'description': '🎨 Экскурсия по церквям с древними фресками.\n\n💰 Цена: 7 000 ₽ за группу до 10 человек\n\nФрески XII–XV веков, в том числе работы Феофана Грека.\n\n✅ Погружение в мир древнерусской живописи.',
            'display_name': 'Мир фресок',
            'photo_url': None,
            'type': 'platnie'
        },
    },

    'low': {
        # ========== ПРОЖИВАНИЕ ==========
        'low_prozhivanie_1': {
            'address': 'Хостел "Турист", ул. Розважа, 11/1',
            'coordinates': (58.525747, 31.276239),
            'description': '🏨 Хостел «Турист» в центре города.\n\n💰 Цены за место в сутки: 800 - 1 200 ₽\n\n✅ Двухъярусные кровати, ящички под ключ.\n✅ Общая кухня: холодильник, СВЧ, термопот, кулер.\n✅ Две душевые, четыре туалета. Парковка в 30 метрах.\n✅ Круглосуточная стойка регистрации, гладильные принадлежности, аптечка.\n\n📍 Рядом: Кремль, Софийский собор, набережная.',
            'display_name': 'Хостел "Турист"',
            'photo_url': None,
            'type': 'prozhivanie'
        },
        'low_prozhivanie_2': {
            'address': 'Бм-хостел, Большая Санкт-Петербургская ул., 14',
            'coordinates': (58.529374, 31.271711),
            'description': '🏨 Хостел в центре города, недалеко от Кремля.\n\n💰 Цены за место в сутки: 700 - 1 000 ₽\n\n✅ Чистые номера, общие кухни.\n✅ Отличное место для проживания во время путешествия.',
            'display_name': 'Бм-Хостел',
            'photo_url': None,
            'type': 'prozhivanie'
        },
        'low_prozhivanie_3': {
            'address': 'Гостевой дом "Орловский дом", Орловский пер., 5/8',
            'coordinates': (58.512710, 31.257312),
            'description': '🏨 Гостевой дом «Орловский».\n\n💰 Цены за номер (2-3 чел.) в сутки: 2 500 - 3 000 ₽\n\n✅ Бесплатный Wi-Fi, кровати с ортопедическим матрасом.\n✅ В комнатах: холодильник, чайник.\n✅ Бесплатная парковка под камерами, зона барбекю, терраса.\n✅ Рядом сетевые магазины.',
            'display_name': 'Гостевой дом "Орловский дом"',
            'photo_url': None,
            'type': 'prozhivanie'
        },
        'low_prozhivanie_4': {
            'address': 'Хостел "Академ ВН", ул. Саши Устинова, 3/1',
            'coordinates': (58.540719, 31.258057),
            'description': '🏨 Хостел «Академ ВН».\n\n💰 Цены за место в сутки: 700 - 1 000 ₽\n\n✅ Чистые номера, удобные кровати, индивидуальное освещение.\n✅ Общая кухня: холодильник, микроволновка, посуда.\n✅ Душевая с феном.',
            'display_name': 'Хостел "Академ ВН"',
            'photo_url': None,
            'type': 'prozhivanie'
        },
        'low_prozhivanie_5': {
            'address': 'Хостел "sleep & go", ул. Черемнова-Конюхова, 8',
            'coordinates': (58.528496, 31.292274),
            'description': '🏨 Хостел «Слип энд ГОУ» в историческом центре.\n\n💰 Цены за место в сутки: 800 - 1 200 ₽\n\n✅ Чисто, аккуратно, свежее постельное бельё, удобные кровати.\n✅ Общая кухня для самостоятельного приготовления еды.\n✅ Приветливый персонал, регулярная уборка.',
            'display_name': 'Хостел "sleep & go"',
            'photo_url': None,
            'type': 'prozhivanie'
        },

        # ========== ПИТАНИЕ ==========
        'low_pitanie_1': {
            'address': 'Ресторан "Чайная ложка", Большая Санкт-Петербургская ул., 25 (ТЦ "Русь")',
            'coordinates': (58.533020, 31.267274),
            'description': '🍽️ Ресторан быстрого питания.\n\n💰 Средний чек: 400 - 600 ₽\n\nБыстро и вкусно. Подойдёт для перекуса во время прогулки по городу.',
            'display_name': 'Чайная ложка',
            'photo_url': None,
            'type': 'pitanie'
        },
        'low_pitanie_2': {
            'address': 'Кофейня "В шкафу", Большая Санкт-Петербургская ул., 5/1',
            'coordinates': (58.526917, 31.272780),
            'description': '☕ Уютное семейное кафе.\n\n💰 Средний чек: 500 - 800 ₽\n\nАроматный кофе, вкусные десерты: запечённая рикотта, яблочный штрудель, маковый десерт.',
            'display_name': 'Кофейня "В шкафу"',
            'photo_url': None,
            'type': 'pitanie'
        },
        'low_pitanie_3': {
            'address': 'Столовая НТШ "Блок питания", ул. Великая, 18а',
            'coordinates': (58.538525, 31.278664),
            'description': '🍽️ Столовая «Блок Питания».\n\n💰 Средний чек: 250 - 400 ₽\n\nЗавтраки, обеды, ужины. Супы, салаты, горячие блюда, десерты. Доступные цены.',
            'display_name': 'Столовая "НТШ"',
            'photo_url': None,
            'type': 'pitanie'
        },
        'low_pitanie_4': {
            'address': 'Столовая "Борщи", Большая Санкт-Петербургская ул., 5/1',
            'coordinates': (58.526917, 31.272780),
            'description': '🍽️ Столовая «Борщи» недалеко от исторического центра.\n\n💰 Средний чек: 300 - 450 ₽\n\nБольшие порции, доступные цены. Супы, вторые блюда, салаты, выпечка.',
            'display_name': 'Столовая "Борщи"',
            'photo_url': None,
            'type': 'pitanie'
        },

        # ========== БЕСПЛАТНЫЕ РАЗВЛЕЧЕНИЯ ==========
        'low_besplatnie_1': {
            'address': 'Прогулка по Кремлю и набережной',
            'coordinates': None,
            'description': '🚶 Бесплатная прогулка!\n\n📍 Кремль (Детинец) — вход на территорию свободный.\n📍 Набережная Александра Невского — живописные виды на реку Волхов.\n📍 Ярославово Дворище — древний архитектурный комплекс.\n\n✅ Идеально для неспешной прогулки и красивых фотографий.',
            'display_name': 'Прогулка по Кремлю',
            'photo_url': None,
            'type': 'besplatnie'
        },
        'low_besplatnie_2': {
            'address': 'Фестиваль «Новгородское лето»',
            'coordinates': None,
            'description': '🎉 Ежегодный летний фестиваль.\n\n💰 Бесплатно!\n\n📅 1 июня – 31 августа 2026\n\nКонцерты, мастер-классы, творческие встречи, танцевальные и спортивные мероприятия по всему городу.\n\n✅ Следите за афишей!',
            'display_name': 'Фестиваль "Новгородское лето"',
            'photo_url': None,
            'type': 'besplatnie'
        },
        'low_besplatnie_3': {
            'address': 'Выставка «Храмы Земли Русской»',
            'coordinates': None,
            'description': '🎨 Выставка в Государственном музее художественной культуры.\n\n💰 Бесплатно по Пушкинской карте\n\n📅 До 17 мая 2026\n\nБолее 70 экспонатов: живопись, графика, арт-объекты от 50 современных художников.\n\n✅ Для молодёжи 14-22 лет вход бесплатный по Пушкинской карте.',
            'display_name': 'Выставка "Храмы Земли Русской"',
            'photo_url': None,
            'type': 'besplatnie'
        },
        'low_besplatnie_4': {
            'address': 'Мультимедийный центр «Исходный код»',
            'coordinates': None,
            'description': '🎮 Центр в ЦКИ «Диалог».\n\n💰 Бесплатно по Пушкинской карте\n\nИстория края через дополненную и виртуальную реальность. AR-приложение для смартфонов.\n\n✅ Требуется предварительная запись!',
            'display_name': 'Центр "Исходный код"',
            'photo_url': None,
            'type': 'besplatnie'
        },
        'low_besplatnie_5': {
            'address': 'Экспозиция церкви Федора Стратилата на Ручье',
            'coordinates': None,
            'description': '⛪ Памятник новгородского зодчества XIV века.\n\n💰 от 100 ₽\n\nСохранилась часть первоначальной росписи, выполненной византийскими мастерами.\n\n✅ Очень атмосферное место!',
            'display_name': 'Церковь Федора Стратилата',
            'photo_url': None,
            'type': 'besplatnie'
        },

        # ========== ПЛАТНЫЕ РАЗВЛЕЧЕНИЯ ==========
        'low_platnie_1': {
            'address': 'Грановитая палата, территория Кремля, 14а',
            'coordinates': (58.522660, 31.275844),
            'description': '🎟️ Экскурсия по Грановитой палате.\n\n💰 Цена: от 500 ₽ (взрослый билет)\n\nОдин из символов Великого Новгорода. Интерьеры, где проходили важные исторические события.',
            'display_name': 'Грановитая палата',
            'photo_url': None,
            'type': 'platnie'
        },
        'low_platnie_2': {
            'address': 'Каток в Кремлёвском парке',
            'coordinates': None,
            'description': '⛸️ Платный каток с музыкой.\n\n💰 Цена: ~300-500 ₽\n\n📍 Кремлёвский парк\n\nРаботает в зимний сезон. Хороший подбор музыки, уютная атмосфера.',
            'display_name': 'Каток в Кремлёвском парке',
            'photo_url': None,
            'type': 'platnie'
        },
        'low_platnie_3': {
            'address': 'Мастер-класс «Шоколадный сувенир»',
            'coordinates': None,
            'description': '🍫 Создание сувенира из белого шоколада.\n\n💰 Цена: 2 000 ₽ за человека\n\n📍 Набережная Александра Невского\n\nВ программе — чай со сладостями. Сувенир забираете с собой.',
            'display_name': 'Шоколадный сувенир',
            'photo_url': None,
            'type': 'platnie'
        },
        'low_platnie_4': {
            'address': 'Исторический квест без гида',
            'coordinates': None,
            'description': '🗺️ Квест по городу без гида.\n\n💰 Цена: 800 ₽ за группу до 10 человек\n\n📍 Старт у Белой башни\n\nЗнакомство с городом через художественную историю и элементы ориентирования.',
            'display_name': 'Исторический квест',
            'photo_url': None,
            'type': 'platnie'
        },
        'low_platnie_5': {
            'address': 'Вечерняя водная прогулка «Круиз на закат»',
            'coordinates': None,
            'description': '🛥️ 90-минутная прогулка на теплоходе.\n\n💰 Цена: 1 800 ₽ (взрослый), 1 300 ₽ (детский до 10 лет)\n\n📍 Отправление от причала «Ярославово Дворище»\n\nЖивая музыка (саксофон). Вид на Свято-Юрьев монастырь. Ежедневно в 19:00.',
            'display_name': 'Круиз на закате',
            'photo_url': None,
            'type': 'platnie'
        },
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
    bot.polling(non_stop=True)