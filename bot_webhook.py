# bot_webhook.py

import os
import asyncio
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from openpyxl import load_workbook
import pandas as pd

# 🔹 Variables
TOKEN = "8303903539:AAF9uP0x9ntBfkG7V26WGEiYmQxjYX5DwDo"
WEBHOOK_URL = "https://ktbot.onrender.com"  # Ton URL Render
PORT = int(os.environ.get("PORT", 5000))

# 🔹 Charger ton fichier Excel (mettre le chemin relatif)
wb = load_workbook("kt++.xlsx")  # Ton fichier Excel doit être dans le repo Render
sheet = wb.active

# 🔹 Fonction de test
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot prêt et fonctionnel !")

# 🔹 Créer l'application
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

# 🔹 Fonction main pour lancer le webhook
async def main():
    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )

if __name__ == "__main__":
    asyncio.run(main())
