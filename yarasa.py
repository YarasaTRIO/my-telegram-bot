import telebot
import os
from flask import Flask, request

# ====================== TOKEN ======================
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("❌ TOKEN bulunamadı! Railway -> Variables bölümünden 'TOKEN' eklediğinden emin ol.")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ====================== KOMUTLAR ======================
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Selam 👋")

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "Komutlar:\n/start → Selam verir")

# Diğer mesajlara cevap (istediğin zaman kapatabilirsin)
@bot.message_handler(func=lambda message: True)
def all_messages(message):
    bot.reply_to(message, "Selam! /start yazmayı dene.")

# ====================== WEBHOOK ======================
@app.route("/" + TOKEN, methods=["POST"])
def webhook():
    try:
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
    except Exception as e:
        print(f"Webhook hatası: {e}")
    return "OK", 200


if __name__ == "__main__":
    # Mevcut webhook'u kaldır
    bot.remove_webhook()
    
    # Railway domainini otomatik al
    domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    
    if domain:
        webhook_url = f"https://{domain}/{TOKEN}"
    else:
        webhook_url = f"https://senin-domainin.up.railway.app/{TOKEN}"  # ← Burayı kendi domaininle değiştir
    
    bot.set_webhook(url=webhook_url)
    print(f"✅ Webhook ayarlandı: {webhook_url}")
    
    # Railway portu
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
