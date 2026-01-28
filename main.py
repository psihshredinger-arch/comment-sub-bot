import telebot
from telebot import types
import json
import os

# Вставь сюда токен, который дал BotFather
TOKEN = "8512683766:AAG07KacACNAHhdOlTXJUCtxIz1KkyS6PWw"

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "subs.json"

# ---------- функции для хранения подписок ----------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ---------- обработка кнопки подписки ----------
@bot.callback_query_handler(func=lambda call: call.data.startswith("sub:"))
def subscribe(call):
    _, chat_id, post_id = call.data.split(":")
    user_id = str(call.from_user.id)

    data = load_data()
    key = f"{chat_id}:{post_id}"

    if key not in data:
        data[key] = []

    if user_id not in data[key]:
        data[key].append(user_id)
        save_data(data)
        bot.answer_callback_query(call.id, "Ты подписан(а) на комментарии 🔔")
    else:
        bot.answer_callback_query(call.id, "Ты уже подписан(а) ✅")

# ---------- ловим комментарии ----------
@bot.message_handler(func=lambda message: message.reply_to_message is not None)
def new_comment(message):
    if not message.reply_to_message.forward_from_chat:
        return

    channel_id = str(message.reply_to_message.forward_from_chat.id)
    post_id = str(message.reply_to_message.forward_from_message_id)

    key = f"{channel_id}:{post_id}"
    data = load_data()

    if key not in data:
        return

    for user_id in data[key]:
        try:
            bot.send_message(int(user_id), f"💬 Новый комментарий под постом:\n\n{message.text}")
        except:
            pass

print("Bot started")
bot.infinity_polling()
