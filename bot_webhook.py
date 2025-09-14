import os
import openpyxl
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# ---------------- CONFIG ----------------
TOKEN = "TON_BOT_TOKEN_ICI"  # Remplace par ton token
WEBHOOK_URL = "https://ton-app.onrender.com"  # Remplace par l'adresse de ton Render
PORT = int(os.environ.get("PORT", 10000))
EXCEL_FILE = "kt++.xlsx"

# ---------------- CHARGER EXCEL ----------------
wb = openpyxl.load_workbook(EXCEL_FILE)
ws = wb.active

# Charger les données dans un dictionnaire {clé: paragraphe}
excel_data = {str(row[0]): row[1] for row in ws.iter_rows(min_row=2, values_only=True)}

# ---------------- COMMANDES ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bonjour ! Envoie-moi un numéro pour recevoir le paragraphe correspondant.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Envoie un numéro ou un mot-clé pour obtenir le paragraphe associé.")

async def get_paragraph(update: Update, context: ContextTypes.DEFAULT_TYPE):
    key = update.message.text.strip()
    paragraph = excel_data.get(key)
    if paragraph:
        await update.message.reply_text(paragraph)
    else:
        await update.message.reply_text("Aucun paragraphe trouvé pour ce numéro.")

# ---------------- MAIN ----------------
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_paragraph))

    # Démarrer le webhook
    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
