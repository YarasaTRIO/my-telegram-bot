import telebot
import os
from flask import Flask, request

# Token Railway'den geliyor
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN bulunamadı! Railway Variables'a eklediğinden emin ol.")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ====================== KOMUTLAR ======================
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Selam 👋")

# İstersen başka komut da ekleyebilirsin
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "Şu an sadece /start komutu var.")

# Diğer tüm mesajlara cevap (isteğe bağlı, kapatmak istersen sil)
@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, "Selam! Sadece /start yazabilirsin.")

# ====================== WEBHOOK ======================
@app.route("/" + TOKEN, methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200


if __name__ == "__main__":
    bot.remove_webhook()
    
    # Railway domainini otomatik almaya çalışır
    domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    if domain:
        webhook_url = f"https://{domain}/{TOKEN}"
    else:
        webhook_url = f"https://BURAYA-RAILWAY-DOMAININ.up.railway.app/{TOKEN}"
    
    bot.set_webhook(url=webhook_url)
    
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
