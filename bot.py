
import os
import json
import telebot

TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])

bot = telebot.TeleBot(TOKEN)
FILE = "movies.json"

def load_movies():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_movies(movies):
    with open(FILE, "w") as f:
        json.dump(movies, f)

movies = load_movies()
waiting_for_code = set()

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🎬 ALI CINEMA ga xush kelibsiz!\n"
        "Kino kodini yuboring 🍿"
    )

@bot.message_handler(commands=["add"])
def add_movie(message):
    if message.from_user.id != ADMIN_ID:
        return
    waiting_for_code.add(message.from_user.id)
    bot.reply_to(message, "Kino kodini yuboring:")

@bot.message_handler(content_types=["video", "document"])
def receive_movie(message):
    if message.from_user.id != ADMIN_ID:
        return
    if message.from_user.id not in waiting_for_code:
        return
    bot.reply_to(message, "Avval kino kodini yuboring: /add")
    
@bot.message_handler(func=lambda m: bool(m.text))
def handle_text(message):
    if message.from_user.id == ADMIN_ID and message.text == "/cancel":
        waiting_for_code.discard(message.from_user.id)
        bot.reply_to(message, "Bekor qilindi.")
        return

    movie = movies.get(message.text.strip())
    if movie:
        bot.send_video(message.chat.id, movie)
    else:
        bot.reply_to(message, "❌ Bu kodda kino topilmadi.")

bot.infinity_polling()
