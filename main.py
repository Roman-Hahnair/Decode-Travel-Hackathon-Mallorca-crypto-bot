
"""
Install it with:
pip install python-telegram-bot==21.1.1

"""


import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

# Retrieve token from environment variable
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("No token provided. Set the TELEGRAM_BOT_TOKEN environment variable.")

# Mapping secret numbers to locations and their image URLs
SECRET_NUMBERS = {
    '12345': ('Palma de Mallorca', 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Rathaus_Palma_de_Mallorca_abends_%28Zuschnitt%29.jpg/320px-Rathaus_Palma_de_Mallorca_abends_%28Zuschnitt%29.jpg'),
    '23456': ('Sóller', 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Sant_Bartomeu%2C_S%C3%B3ller%2C_Mallorca.jpg/177px-Sant_Bartomeu%2C_S%C3%B3ller%2C_Mallorca.jpg'),
    '34567': ('Valldemossa', 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Chopin-Valldemossa-KStanowski.jpg/180px-Chopin-Valldemossa-KStanowski.jpg'),
    '45678': ('Deià', 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/EmbarcadorcalaDei%C3%A0.JPG/320px-EmbarcadorcalaDei%C3%A0.JPG'),
    '56789': ('Alcúdia', 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Alcudia_6745.jpg/320px-Alcudia_6745.jpg')
}
USER_SCORES = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    keyboard = [[InlineKeyboardButton("Start the Game", callback_data='start_game')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_message = f"Hello {user.first_name}, I am your bot! Click the button below to start the game."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message, reply_markup=reply_markup)

async def start_game_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Game started! Guess the secret 5-digit numbers associated with locations in Mallorca.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    user_id = update.effective_user.id

    # Ensure the user's score is initialized
    if user_id not in USER_SCORES:
        USER_SCORES[user_id] = 0

    if text.isdigit() and len(text) == 5:
        if text in SECRET_NUMBERS:
            USER_SCORES[user_id] += 1
            location, image_url = SECRET_NUMBERS[text]
            congratulations_message = f"Correct! You found our secret QR in {location}. Your score is now {USER_SCORES[user_id]}."
            await update.message.reply_photo(photo=image_url, caption=congratulations_message)
        else:
            await update.message.reply_text("Wrong number, try again!")
    else:
        await update.message.reply_text("Please enter a valid 5-digit number.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(start_game_callback, pattern='^start_game$'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == '__main__':
    main()
