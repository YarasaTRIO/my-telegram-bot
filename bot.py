import telebot
import os
from flask import Flask, request

# Token'ı Railway'den al (güvenli)
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# Webhook endpoint
@app.route("/" + TOKEN, methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

# Örnek komut
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Merhaba! Botum Railway ile 24/7 aktif 🚀")

# Diğer mesajlara echo (istediğin gibi değiştirebilirsin)
@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, message.text)

# Webhook'u ayarla
if __name__ == "__main__":
    bot.remove_webhook()
    # Railway sana verdiği domaini buraya yazacaksın (deploy sonrası)
    bot.set_webhook(url=f"https://BOTUN-DOMAINI.up.railway.app/{TOKEN}")
    
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
