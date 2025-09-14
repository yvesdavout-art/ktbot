import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from openpyxl import load_workbook

# 🔹 Variables d'environnement Render
TOKEN = os.environ.get("8303903539:AAF9uP0x9ntBfkG7V26WGEiYmQxjYX5DwDo")  # Ton token Telegram
WEBHOOK_URL = os.environ.get("https://ktbot.onrender.com")  # URL Render

# 🔹 Flask
flask_app = Flask(__name__)

# 🔹 Initialisation bot
bot = Bot(token=TOKEN)
app = Application.builder().token(TOKEN).build()

# 🔹 Charger Excel (fichier dans le repo)
EXCEL_FILE = "kt++.xlsx"
wb = load_workbook(EXCEL_FILE)
ws = wb.active
print(f"{ws.max_row} paragraphes chargés.")

# 🔹 Commandes existantes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot prêt et opérationnel !")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Voici les commandes disponibles : /start, /help, /autrecommande")

async def autrecommande(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ceci est ta commande personnalisée !")

# 🔹 Ajouter les handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("autrecommande", autrecommande))

# 🔹 Flask route pour Telegram
@flask_app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    # Pousser la mise à jour dans la queue du bot
    app.update_queue.put_nowait(update)
    return "ok"

# 🔹 Déploiement Render
if __name__ == "__main__":
    # Définir le webhook sur Telegram
    bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    print("Webhook défini, bot prêt à fonctionner H24.")

    # Lancer Flask sur Render
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)
