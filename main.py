# main.py
from telebot import TeleBot
from keep_alive import keep_alive
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

keep_alive()  # Botni 24/7 ishlashi uchun

# 🔹 Yangi token
BOT_TOKEN = "8750699803:AAGK1ng4UEqneMFXTIMvabbzDgu5H4Z3JrE"
bot = TeleBot(BOT_TOKEN)

# 🔹 Majburiy obuna kanallari
CHANNELS = [
    "@kanal1", "@kanal2", "@kanal3", "@kanal4", "@kanal5",
    "@kanal6", "@kanal7", "@kanal8", "@kanal9", "@kanal10",
    "@kanal11", "@kanal12", "@kanal13", "@kanal14", "@kanal15"
]

OWNER_ID = 123456789  # SENING ID
ADMINS = [OWNER_ID]

USERS = set()
ANIME_DB = {
    "101": ["https://t.me/kanaling/5", "https://t.me/kanaling/6"],
    "102": ["https://t.me/kanaling/7", "https://t.me/kanaling/8", "https://t.me/kanaling/9"],
    "103": ["https://t.me/kanaling/10"],
    "104": ["https://t.me/kanaling/11", "https://t.me/kanaling/12"]
}

SEARCH_COUNT = {}
CHECK_COUNT = 0

# 🔹 Obuna tekshirish funksiyasi
def check_sub(user_id):
    for channel in CHANNELS:
        status = bot.get_chat_member(channel, user_id).status
        if status not in ["member", "administrator", "creator"]:
            return False
    return True

# 🔹 /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    USERS.add(message.from_user.id)
    markup = InlineKeyboardMarkup()
    
    # Majburiy obuna tugmalari
    for channel in CHANNELS:
        markup.add(InlineKeyboardButton("Obuna bo‘lish", url=f"https://t.me/{channel[1:]}"))
    markup.add(InlineKeyboardButton("Tekshirish", callback_data="check"))
    
    # 🔹 Reklama / kontakt tugmasi
    markup.add(InlineKeyboardButton("📞 Menga yozish", url="https://t.me/ismingiz"))  # Telegram link yoki tel raqam
    
    # 🔹 Bot haqida tugma
    markup.add(InlineKeyboardButton("ℹ️ Bot haqida", callback_data="bot_info"))
    
    bot.send_message(message.chat.id, "Salom botimizga xush kelibsiz! 🎬", reply_markup=markup)

# 🔹 Callback tugmalar
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global CHECK_COUNT
    if call.data == "check":
        CHECK_COUNT += 1
        if check_sub(call.from_user.id):
            bot.send_message(call.message.chat.id, "Obuna tasdiqlandi ✅ Endi kod yuboring.")
        else:
            bot.answer_callback_query(call.id, "Hali obuna bo‘lmagansiz ❌", show_alert=True)
    elif call.data == "bot_info":
        info_text = """
📌 **Bot haqida ma’lumot**:

1. Anime kodini yuborsangiz barcha qismlari tugmalar bilan chiqadi 🎬  
2. Majburiy obuna – 15 ta kanal ✅  
3. Admin panel – faqat OWNER_ID va adminlar uchun 🛠  
4. Statistika – foydalanuvchilar, qidirishlar va obuna tekshiruvlari 📊  
5. Reklama tugmasi orqali siz bilan bog‘lanish mumkin 📞
"""
        bot.send_message(call.message.chat.id, info_text)

# 🔹 Anime kodi qidirish
@bot.message_handler(func=lambda message: True)
def search(message):
    USERS.add(message.from_user.id)
    code = message.text.strip()
    if code in ANIME_DB:
        SEARCH_COUNT[code] = SEARCH_COUNT.get(code, 0) + 1
        markup = InlineKeyboardMarkup()
        for idx, link in enumerate(ANIME_DB[code], 1):
            markup.add(InlineKeyboardButton(f"🎬 Qism {idx}", url=link))
        bot.send_message(message.chat.id, "Mana topildi:", reply_markup=markup)
        bot.send_message(message.chat.id, "📢 Kanalimizga obuna bo‘ling: https://t.me/anicrab_uz")
    else:
        bot.send_message(message.chat.id, "Bunday kod topilmadi ❌")

# 🔹 Admin panel
@bot.message_handler(commands=['addadmin'])
def add_admin(message):
    if message.from_user.id == OWNER_ID:
        try:
            new_admin = int(message.text.split()[1])
            ADMINS.append(new_admin)
            bot.send_message(message.chat.id, f"Admin qo‘shildi ✅\nID: {new_admin}")
        except:
            bot.send_message(message.chat.id, "ID noto‘g‘ri ❌")
    else:
        bot.send_message(message.chat.id, "Sizga ruxsat yo‘q ❌")

@bot.message_handler(commands=['removeadmin'])
def remove_admin(message):
    if message.from_user.id == OWNER_ID:
        try:
            rem_admin = int(message.text.split()[1])
            if rem_admin in ADMINS and rem_admin != OWNER_ID:
                ADMINS.remove(rem_admin)
                bot.send_message(message.chat.id, f"Admin olib tashlandi ✅\nID: {rem_admin}")
            else:
                bot.send_message(message.chat.id, "ID topilmadi yoki OWNER_ID o‘chirish mumkin emas ❌")
        except:
            bot.send_message(message.chat.id, "ID noto‘g‘ri ❌")
    else:
        bot.send_message(message.chat.id, "Sizga ruxsat yo‘q ❌")

@bot.message_handler(commands=['users'])
def list_users(message):
    if message.from_user.id in ADMINS:
        if USERS:
            bot.send_message(message.chat.id, "Foydalanuvchilar:\n" + "\n".join(map(str, USERS)))
        else:
            bot.send_message(message.chat.id, "Hali foydalanuvchi yo‘q ❌")
    else:
        bot.send_message(message.chat.id, "Sizga ruxsat yo‘q ❌")

@bot.message_handler(commands=['addanime'])
def add_anime(message):
    if message.from_user.id in ADMINS:
        try:
            parts = message.text.split()
            code = parts[1]
            links = parts[2:]
            if code in ANIME_DB:
                ANIME_DB[code].extend(links)
            else:
                ANIME_DB[code] = links
            bot.send_message(message.chat.id, f"Anime kodi {code} yangilandi ✅")
        except:
            bot.send_message(message.chat.id, "Format xato ❌\nMisol: /addanime 101 link1 link2")
    else:
        bot.send_message(message.chat.id, "Sizga ruxsat yo‘q ❌")

@bot.message_handler(commands=['removeanime'])
def remove_anime(message):
    if message.from_user.id in ADMINS:
        try:
            code = message.text.split()[1]
            if code in ANIME_DB:
                del ANIME_DB[code]
                bot.send_message(message.chat.id, f"Anime kodi {code} o‘chirildi ✅")
            else:
                bot.send_message(message.chat.id, "Kod topilmadi ❌")
        except:
            bot.send_message(message.chat.id, "Format xato ❌\nMisol: /removeanime 101")
    else:
        bot.send_message(message.chat.id, "Sizga ruxsat yo‘q ❌")

# 🔹 Statistika
@bot.message_handler(commands=['stats'])
def stats(message):
    if message.from_user.id in ADMINS:
        text = f"📊 Statistika:\n\nFoydalanuvchilar soni: {len(USERS)}\nObuna tekshirishlar: {CHECK_COUNT}\n\nAnime qidirishlar:"
        if SEARCH_COUNT:
            for code, count in SEARCH_COUNT.items():
                text += f"\n{code}: {count} marta"
        else:
            text += "\nHali qidirishlar yo‘q"
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, "Sizga ruxsat yo‘q ❌")

bot.infinity_polling()
