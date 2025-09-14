import os
from openpyxl import load_workbook
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# 🔹 Token et webhook
TOKEN = "8303903539:AAF9uP0x9ntBfkG7V26WGEiYmQxjYX5DwDo"
WEBHOOK_URL = "https://ktbot.onrender.com"

# 🔹 Lecture Excel
wb = load_workbook("kt++.xlsx")  # fichier dans le repo Render
ws = wb.active
paragraphs = [cell.value for cell in ws['A'] if cell.value]

# 🔹 Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salut ! Envoie un numéro de paragraphe.")

async def send_paragraph(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        idx = int(update.message.text) - 1
        if 0 <= idx < len(paragraphs):
            await update.message.reply_text(paragraphs[idx])
        else:
            await update.message.reply_text("Numéro invalide.")
    except:
        await update.message.reply_text("Envoie un numéro valide.")

# 🔹 Application
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_paragraph))

# 🔹 Déploiement Webhook Render
if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )
