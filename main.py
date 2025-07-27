import telebot
import requests
import os

# API keys from environment (you can hardcode if needed)
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = "36a08a0059acfdd5c086110065d44686e93aeb21"  # ShrinkEarn API Key

bot = telebot.TeleBot(BOT_TOKEN)

# Anime name and its original download link
anime_links = {
    "naruto": "https://example.com/naruto-download",
    "one piece": "https://example.com/onepiece-download",
    "bleach": "https://example.com/bleach-download",
    "attack on titan": "https://example.com/aot-download"
    # Add more anime here
}

# /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Welcome to AnimeMakes Bot!\n\nSend me the *anime name* and I’ll reply with the *shortened download link*!", parse_mode="Markdown")

# Handle text messages (user anime input)
@bot.message_handler(func=lambda message: True)
def handle_anime_name(message):
    anime_name = message.text.strip().lower()

    if anime_name in anime_links:
        long_url = anime_links[anime_name]

        # ShrinkEarn Shorten Link
        try:
            api_url = f"https://shrinkearn.com/api?api={API_KEY}&url={long_url}"
            res = requests.get(api_url)
            data = res.json()

            if "shortenedUrl" in data:
                short_link = data["shortenedUrl"]
                bot.reply_to(message, f"📥 Download Link for *{anime_name.title()}*:\n🔗 {short_link}", parse_mode="Markdown")
            elif "shortened" in data:
                bot.reply_to(message, f"📥 Download Link:\n🔗 {data['shortened']}")
            else:
                bot.reply_to(message, "❌ Failed to shorten the link. Please try again.")
        except Exception as e:
            bot.reply_to(message, f"❌ Error: {e}")
    else:
        bot.reply_to(message, "❌ Anime not found. Please enter a valid anime name.\n\nExample: Naruto, One Piece, Bleach")

bot.infinity_polling()
