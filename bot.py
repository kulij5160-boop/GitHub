import random
import telebot
from telebot import types

# Подключаем бота по вашему токену
bot = telebot.TeleBot("8874829311:AAE27B2dVEgOg8WatroZ73w3wKrFIzmhWOU")

# База данных игроков в памяти
users_db = {}

# Цены в автосалоне
CAR_SHOP = {
    "Запорожец 966": 40000,
    "ВАЗ 2101": 70000,
    "ВАЗ 2103": 120000,
    "ВАЗ 2107": 200000,
    "ВАЗ 2112": 250000,
    "ГАЗ Победа": 500000
}

# Остальные категории магазина
SHOP_ITEMS = {
    "жилье": {"Каморка": 500, "Квартира": 5000, "Вилла": 50000},
    "одежда": {"Худи с рынка": 300, "Деловой костюм": 3000, "Бренд Gucci": 20000},
    "телефон": {"Xiaomi Redmi 9": 800, "iPhone 15 Pro": 7000},
    "яхта": {"Катер": 30000, "Суперъяхта": 500000},
    "оружие": {"Пистолет Макарова": 15000, "Автомат АК-74": 45000, "Винтовка СВД": 90000}
}

# Проверка и регистрация пользователя
def check_user(user_id, username):
    if user_id not in users_db:
        users_db[user_id] = {
            "name": username if username else "Игрок",
            "balance": 0,
            "mined_kg": 0,
            "housing": "Нет",
            "car": "Нет",
            "clothes": "Нет",
            "phone": "Нет",
            "yacht": "Нет",
            "weapon": "Нет"
        }

# Главное меню
def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_profile = types.KeyboardButton("👤 Профиль")
    btn_jobs = types.KeyboardButton("💼 На работу")
    btn_shop = types.KeyboardButton("🛒 Магазин")
    markup.add(btn_profile)
    markup.add(btn_jobs, btn_shop)
    return markup

# Меню выбора работы
def get_jobs_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("⛏ Шахтер"), types.KeyboardButton("🏭 Завод"))
    markup.add(types.KeyboardButton("📦 Грузчик"), types.KeyboardButton("⬅️ Назад"))
    return markup

@bot.message_handler(commands=['start'])
def start_game(message):
    check_user(message.from_user.id, message.from_user.first_name)
    bot.send_message(
        message.chat.id, 
        f"👋 Привет, {message.from_user.first_name}! Твой игровой аккаунт готов.", 
        reply_markup=get_main_keyboard()
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    check_user(user_id, message.from_user.first_name)
    user = users_db[user_id]

    # --- ПРОФИЛЬ ---
    if message.text == "👤 Профиль":
        profile_text = (
            f"💰 **Игровой профиль:**\n\n"
            f"💵 Баланс: {user['balance']} ₽\n"
            f"📦 Перенесено/добыто груза: {user['mined_kg']} кг\n"
            f"------------------------\n"
            f"🏠 Жилье: {user['housing']}\n"
            f"🚗 Авто: {user['car']}\n"
            f"👕 Одежда: {user['clothes']}\n"
            f"📱 Телефон: {user['phone']}\n"
            f"🛥 Яхта: {user['yacht']}\n"
            f"🔫 Оружие: {user['weapon']}"
        )
        bot.send_message(message.chat.id, profile_text, parse_mode="Markdown")

    # --- ВЫБОР РАБОТЫ ---
    elif message.text == "💼 На работу":
        bot.send_message(message.chat.id, "Куда отправимся работать?", reply_markup=get_jobs_keyboard())

    elif message.text == "⬅️ Назад":
        bot.send_message(message.chat.id, "Возвращаемся в меню.", reply_markup=get_main_keyboard())

    # --- РАБОТА 1: ШАХТЕР ---
    elif message.text == "⛏ Шахтер":
        kg = random.randint(10, 15)
        money = random.randint(300, 400)
        user["balance"] += money
        user["mined_kg"] += kg
        bot.send_message(message.chat.id, f"⛏ Ты отработал смену шахтером!\n📦 Добыто руды: +{kg} кг\n💵 Заработано: +{money} ₽")

    # --- РАБОТА 2: ЗАВОД ---
    elif message.text == "🏭 Завод":
        kg = random.randint(4, 9)
        money = random.randint(250, 340)
        user["balance"] += money
        user["mined_kg"] += kg
        bot.send_message(message.chat.id, f"🏭 Вы отстояли смену у станка!\n📦 Сделано деталей: +{kg} кг\n💵 Заработано: +{money} ₽")

    # --- РАБОТА 3: ГРУЗЧИК ---
    elif message.text == "📦 Грузчик":
        kg = random.randint(10, 14)
        money = random.randint(270, 380)
        user["balance"] += money
        user["mined_kg"] += kg
        bot.send_message(message.chat.id, f"📦 Ты таскал тяжелые коробки на складе!\n📦 Перенесено: +{kg} кг\n💵 Заработано: +{money} ₽")

    # --- МАГАЗИН И АВТОСАЛОН ---
    elif message.text == "🛒 Магазин":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="🚗 Автосалон", callback_data="cat_cars"))
        for category in SHOP_ITEMS.keys():
            markup.add(types.InlineKeyboardButton(text=category.capitalize(), callback_data=f"cat_{category}"))
        
        bot.send_message(message.chat.id, "🏪 Выберите раздел магазина:", reply_markup=markup)

# Обработка Inline-покупок
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    check_user(user_id, call.from_user.first_name)
    user = users_db[user_id]

    # Меню автосалона
    if call.data == "cat_cars":
        markup = types.InlineKeyboardMarkup()
        text = "🚗 **Добро пожаловать в Автосалон:**\n\n"
        for car_name, price in CAR_SHOP.items():
            text += f"▪️ {car_name} — {price:,} ₽\n"
            markup.add(types.InlineKeyboardButton(text=f"Купить {car_name}", callback_data=f"buy_car_{car_name}"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")

    # Покупка машины
    elif call.data.startswith("buy_car_"):
        car_name = call.data.replace("buy_car_", "")
        price = CAR_SHOP[car_name]

        if user["balance"] < price:
            bot.answer_callback_query(call.id, text="❌ У вас недостаточно денег в рублях!", show_alert=True)
        else:
            user["balance"] -= price
            user["car"] = car_name
            bot.answer_callback_query(call.id, text=f"🎉 Поздравляем! Вы купили {car_name}!", show_alert=True)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"✅ Успешно куплено авто: {car_name} за {price:,} ₽.")

    # Остальные категории
    elif call.data.startswith("cat_"):
        category = call.data.split("_")
        markup = types.InlineKeyboardMarkup()
        text = f"🏪 Раздел *{category.capitalize()}*:\n\n"
        for item_name, price in SHOP_ITEMS[category].items():
            text += f"▪️ {item_name} — {price:,} ₽\n"
            markup.add(types.InlineKeyboardButton(text=f"Купить {item_name}", callback_data=f"buy_item_{category}_{item_name}"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("buy_item_"):
        _, _, category, item_name = call.data.split("_")
        price = SHOP_ITEMS[category][item_name]

        if user["balance"] < price:
            bot.answer_callback_query(call.id, text="❌ Недостаточно рублей!", show_alert=True)
        else:
            user["balance"] -= price
            if category == "жилье": user["housing"] = item_name
            elif category == "одежда": user["clothes"] = item_name
            elif category == "телефон": user["phone"] = item_name
            elif category == "яхта": user["yacht"] = item_name
            elif category == "оружие": user["weapon"] = item_name
            
            bot.answer_callback_query(call.id, text=f"🎉 Успешная покупка: {item_name}!", show_alert=True)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"✅ Вы приобрели {item_name} за {price:,} ₽.")

# Запуск
print("Игровой бот v2 успешно запущен...")
bot.infinity_polling()
