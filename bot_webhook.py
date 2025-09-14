import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import openpyxl

# ================= CONFIG =================
TOKEN = "TON_TOKEN_ICI"  # ton token Telegram
WEBHOOK_URL = "https://ton-app.onrender.com"  # ton URL Render
PORT = int(os.environ.get("PORT", 5000))
EXCEL_FILE = "paragraphes.xlsx"

# ================= LOGGING =================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ================= EXCEL =================
wb = openpyxl.load_workbook(EXCEL_FILE)
ws = wb.active

# Dictionnaire clé → paragraphe
excel_data = {str(row[0]): row[1] for row in ws.iter_rows(min_row=2, values_only=True)}

# ================= COMMANDES =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot prêt ! Envoie un mot-clé pour recevoir le paragraphe associé.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Envoie un mot-clé pour recevoir le paragraphe correspondant depuis Excel.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    response = excel_data.get(text, "Aucun paragraphe trouvé pour ce mot-clé.")
    await update.message.reply_text(response)

# ================= MAIN =================
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Commandes
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Webhook
    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
