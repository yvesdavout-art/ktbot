import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from openpyxl import load_workbook

TOKEN = "8303903539:AAF9uP0x9ntBfkG7V26WGEiYmQxjYX5DwDo"
WEBHOOK_URL = "https://ton-app.onrender.com"
PORT = int(os.environ.get("PORT", 10000))

# Charger Excel
wb = load_workbook("kt++.xlsx")
ws = wb.active

# Commande start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot prêt à fonctionner H24 !")

# Commande pour chercher un paragraphe
async def search_paragraph(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    for row in ws.iter_rows(values_only=True):
        if query.lower() in str(row[0]).lower():
            await update.message.reply_text(str(row[1]))
            return
    await update.message.reply_text("Paragraphe non trouvé.")

# Création de l'application
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search_paragraph))

# Lancement du webhook **sans asyncio.run()**
app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
)
