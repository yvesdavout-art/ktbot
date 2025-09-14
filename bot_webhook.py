import os
import asyncio
from openpyxl import load_workbook
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# --- CONFIG ---
TOKEN = "TON_TOKEN_ICI"
WEBHOOK_URL = "https://TON_ADRESSE_RENDER.onrender.com"
PORT = int(os.environ.get("PORT", 10000))
EXCEL_FILE = "kt++.xlsx"  # Assure-toi que ce fichier est dans ton repo

# --- CHARGEMENT DU FICHIER EXCEL ---
wb = load_workbook(EXCEL_FILE)
ws = wb.active

# Convertit les lignes en dictionnaire {clé: paragraphe}
excel_data = {str(row[0].value): row[1].value for row in ws.iter_rows(min_row=2, values_only=True)}

# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot prêt ! Envoie une clé pour recevoir le paragraphe correspondant.")

async def get_paragraph(update: Update, context: ContextTypes.DEFAULT_TYPE):
    key = update.message.text.strip()
    paragraph = excel_data.get(key)
    if paragraph:
        await update.message.reply_text(paragraph)
    else:
        await update.message.reply_text("Aucun paragraphe trouvé pour cette clé.")

# --- APPLICATION ---
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_paragraph))

    # Lancement du webhook
    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )

# --- RUN ---
if __name__ == "__main__":
    asyncio.run(main())
