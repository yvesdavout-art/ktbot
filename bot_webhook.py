import os
import asyncio
from openpyxl import load_workbook
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Ton token et URL webhook
TOKEN = "8303903539:AAF9uP0x9ntBfkG7V26WGEiYmQxjYX5DwDo"
WEBHOOK_URL = "https://ktbot.onrender.com"

# Charger le fichier Excel
wb = load_workbook("kt++.xlsx")
sheet = wb.active
print(f"{sheet.max_row} paragraphes chargés.")

# Créer le bot
app = ApplicationBuilder().token(TOKEN).build()

# Commande /start
async def start(update: Update, context):
    await update.message.reply_text("Bonjour ! Envoie un numéro de paragraphe pour recevoir son contenu.")

app.add_handler(CommandHandler("start", start))

# Répondre aux messages textes (numéro de paragraphe)
async def send_paragraph(update: Update, context):
    text = update.message.text
    if text.isdigit():
        num = int(text)
        if 1 <= num <= sheet.max_row:
            paragraph = sheet[f"A{num}"].value
            await update.message.reply_text(f"Paragraphe {num} : {paragraph}")
        else:
            await update.message.reply_text("Numéro de paragraphe invalide.")
    else:
        await update.message.reply_text("Envoie un numéro de paragraphe.")

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_paragraph))

# Déployer en webhook
async def main():
    await app.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )

if __name__ == "__main__":
    asyncio.run(main())
