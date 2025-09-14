import asyncio
import random
import re
import os
from openpyxl import load_workbook
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, CallbackQueryHandler, filters
)
from flask import Flask, request

# 🔹 Ton token Telegram
TOKEN = "8303903539:AAF9uP0x9ntBfkG7V26WGEiYmQxjYX5DwDo"

# 🔹 URL publique (Render fournira l’URL)
WEBHOOK_URL = "https://remplace-par-l-url-render.com"

# 🔹 Charger l'Excel (relatif, fichier dans le même dossier)
paragraphs = {}
wb = load_workbook("kt++.xlsx")
ws = wb.active
for row in ws.iter_rows(min_row=2, values_only=True):
    numero, texte = row
    if numero and texte:
        numero = str(int(numero))
        texte = str(texte).strip()
        try:
            texte = texte.encode("latin1").decode("utf-8")
        except:
            pass
        paragraphs[numero] = texte

print(f"{len(paragraphs)} paragraphes chargés.")

# 🔹 Fonctions utilitaires
async def send_long_text(chat, text):
    max_len = 4000
    for i in range(0, len(text), max_len):
        await chat.send_message(text[i:i+max_len], parse_mode="HTML")

# 🔹 Commandes
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "Bonjour ! Envoyez un numéro ou utilisez les commandes : /help"
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "Commandes disponibles :\n"
            "/search <mot> - recherche\n"
            "/range <début>-<fin> - plage\n"
            "/random - aléatoire\n"
            "/stats [mot] - statistiques\n"
            "/credits - infos"
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    text = update.message.text.strip()
    if text.isdigit() and text in paragraphs:
        key = text
        keyboard = [
            [InlineKeyboardButton("⬅️ Précédent", callback_data=f"{int(key)-1}"),
             InlineKeyboardButton("➡️ Suivant", callback_data=f"{int(key)+1}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await send_long_text(update.message.chat, f"Paragraphe {key} :\n{paragraphs[key]}")
        await update.message.reply_text("Navigation :", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Numéro inconnu ou commande invalide (/help).")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer(cache_time=1)
    key = str(int(query.data))
    if key in paragraphs:
        keyboard = [
            [InlineKeyboardButton("⬅️ Précédent", callback_data=f"{int(key)-1}"),
             InlineKeyboardButton("➡️ Suivant", callback_data=f"{int(key)+1}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await send_long_text(query.message.chat, f"Paragraphe {key} :\n{paragraphs[key]}")
        await query.message.reply_text("Navigation :", reply_markup=reply_markup)
    else:
        await query.message.reply_text("Paragraphe non trouvé.")

# 🔹 Créer l'application Telegram
app_bot = ApplicationBuilder().token(TOKEN).build()
bot = Bot(TOKEN)

# Ajouter les handlers
app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(CommandHandler("help", help_command))
app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app_bot.add_handler(CallbackQueryHandler(button_callback))

# 🔹 Flask serveur pour webhook
flask_app = Flask(__name__)

@flask_app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run(app_bot.update_queue.put(update))
    return "ok"

if __name__ == "__main__":
    # Définir le webhook
    bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    print("Webhook défini, bot prêt à fonctionner H24.")

    # Démarrer Flask (Render fournit HTTPS automatiquement)
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
