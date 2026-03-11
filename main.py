import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os

# Токен моего бота
bot = telebot.TeleBot('8553675239:AAFZH-jmYRp7wToM-RcNAMdhVxCizd9UBUg')

# Файл для хранения истории сообщений
HISTORY_FILE = 'message_history.json'


# Загружаем историю сообщений из файла
def load_message_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}


# Сохраняем историю сообщений в файл
def save_message_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


# Словарь для хранения идентификаторов сообщений (с загрузкой из файла)
message_ids = load_message_history()


# Функция для удаления ВСЕХ предыдущих сообщений (включая давние)
def delete_all_previous_messages(chat_id):
    if chat_id in message_ids:
        # Проходим по всем сохраненным сообщениям этого чата
        deleted_count = 0
        for msg_id in message_ids[chat_id][:]:  # Копия списка для безопасного удаления
            try:
                bot.delete_message(chat_id, msg_id)
                deleted_count += 1
            except telebot.apihelper.ApiTelegramException:
                pass  # Сообщение уже удалено или слишком старое

        # Очищаем список для этого чата
        message_ids[chat_id] = []
        save_message_history(message_ids)
        print(f"Удалено {deleted_count} сообщений в чате {chat_id}")


# Функция для добавления сообщения в историю
def add_message_to_history(chat_id, message_id):
    if chat_id not in message_ids:
        message_ids[chat_id] = []

    message_ids[chat_id].append(message_id)

    # Ограничиваем историю последними 100 сообщениями на чат
    if len(message_ids[chat_id]) > 100:
        message_ids[chat_id] = message_ids[chat_id][-100:]

    save_message_history(message_ids)


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

# Адреса по категориям (твой полный словарь остается без изменений)
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
        # ... остальные твои данные ...
    },
    'low': {  # Малобюджетные маршруты
        'low_prozhivanie_1': {
            'address': 'хостел "турист", Адрес: ул. розважа, 11/1',
            'coordinates': (58.525747, 31.276239),
            'description': 'Хостел «Турист» находится в центре города. В номерах — двухъярусные кровати, мягкий инвентарь, письменный столик, полочки, вешалка, ящички под ключ. В хостеле есть обеденная зона с холодильником, СВЧ, термопотом и кулером для воды, а также ТВ. Предусмотрены две душевые и четыре туалета. Парковка находится в 30 метрах от хостела. Заезд после 14:00, выезд до 12:00. Стойка регистрации работает круглосуточно. Предоставляются гладильные принадлежности. Есть аптечка первой помощи.\n\nРядом — Кремль, Софийский собор, Софийская площадь, набережная реки Волхов. В Кремлёвском парке есть детские площадки, летом появляются батуты и аттракционы. Неподалёку — Соколиный двор с хищными птицами.',
            'display_name': 'Хостел "Турист"',
            'photo_url': 'https://ibb.co/8DQsjpHD',
            'type': 'prozhivanie'
        },
        # ... остальные твои данные ...
    }
}


@bot.message_handler(commands=['start', 'kommands'])
def main(message):
    # Очищаем ВСЮ историю перед началом
    delete_all_previous_messages(message.chat.id)

    msg = bot.send_message(message.chat.id,
                           'Команды для данного бота: \nлокации или /location - Показывает наши направления')
    add_message_to_history(message.chat.id, msg.message_id)


@bot.message_handler(func=lambda message: message.text.lower() == 'локации' or message.text.lower() == '/location')
def info(message):
    # Удаляем ВСЕ предыдущие сообщения
    delete_all_previous_messages(message.chat.id)

    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for category_name in category_ids.keys():
        category_id = category_ids[category_name]
        markup.add(InlineKeyboardButton(category_name, callback_data=f'cat_{category_id}'))

    msg = bot.send_message(message.chat.id, 'Наши направления:', reply_markup=markup)
    add_message_to_history(message.chat.id, msg.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('cat_'))
def show_place_types(call):
    # Удаляем ВСЕ предыдущие сообщения
    delete_all_previous_messages(call.message.chat.id)

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

    add_message_to_history(call.message.chat.id, msg.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('type_'))
def show_places_by_type(call):
    # Удаляем ВСЕ предыдущие сообщения
    delete_all_previous_messages(call.message.chat.id)

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

    add_message_to_history(call.message.chat.id, msg.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('place_'))
def show_address_details(call):
    try:
        # Разделяем данные
        parts = call.data.split('_')
        category_id = parts[1]
        place_id = '_'.join(parts[2:])

        if category_id in addresses and place_id in addresses[category_id]:
            address_info = addresses[category_id][place_id]

            # Удаляем ВСЕ предыдущие сообщения
            delete_all_previous_messages(call.message.chat.id)

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
                    add_message_to_history(call.message.chat.id, photo_msg.message_id)
                except:
                    msg = bot.send_message(call.message.chat.id, message_text, reply_markup=markup)
                    add_message_to_history(call.message.chat.id, msg.message_id)
            else:
                msg = bot.send_message(call.message.chat.id, message_text, reply_markup=markup)
                add_message_to_history(call.message.chat.id, msg.message_id)

            if coordinates and len(coordinates) == 2 and coordinates[0] is not None and coordinates[1] is not None:
                location_msg = bot.send_location(call.message.chat.id, latitude=coordinates[0],
                                                 longitude=coordinates[1])
                add_message_to_history(call.message.chat.id, location_msg.message_id)
    except Exception as e:
        bot.send_message(call.message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте снова.")


@bot.callback_query_handler(func=lambda call: call.data == 'back_to_categories')
def back_to_categories(call):
    # Удаляем ВСЕ предыдущие сообщения
    delete_all_previous_messages(call.message.chat.id)

    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    for category_name in category_ids.keys():
        category_id = category_ids[category_name]
        markup.add(InlineKeyboardButton(category_name, callback_data=f'cat_{category_id}'))

    msg = bot.send_message(call.message.chat.id, 'Наши направления:', reply_markup=markup)

    add_message_to_history(call.message.chat.id, msg.message_id)


if __name__ == '__main__':
    print("Бот запущен с сохранением истории...")
    print(f"Загружена история для {len(message_ids)} чатов")
    bot.polling()