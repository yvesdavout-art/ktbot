import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from openpyxl import load_workbook

# 🔹 Variables Telegram / Render
TOKEN = "8303903539:AAF9uP0x9ntBfkG7V26WGEiYmQxjYX5DwDo"
WEBHOOK_URL = "https://ktbot.onrender.com"
PORT = int(os.environ.get("PORT", 10000))  # Render définira ce port automatiquement

# 🔹 Charger le fichier Excel
EXCEL_PATH = "kt++.xlsx"  # le fichier doit être dans le repo
wb = load_workbook(EXCEL_PATH)
ws = wb.active

# 🔹 Construire un dictionnaire {clé: paragraphe}
paragraphs = {str(row[0].value): str(row[1].value) for row in ws.iter_rows(min_row=2)}

# 🔹 Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salut ! Envoie-moi le numéro du paragraphe que tu veux lire."
    )

# 🔹 Lecture du paragraphe
async def get_paragraph(update: Update, context: ContextTypes.DEFAULT_TYPE):
    key = update.message.text.strip()
    paragraph = paragraphs.get(key)
    if paragraph:
        await update.message.reply_text(paragraph)
    else:
        await update.message.reply_text("Numéro de paragraphe inconnu.")

# 🔹 Main
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_paragraph))

    # 🔹 Lancer le webhook
    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
