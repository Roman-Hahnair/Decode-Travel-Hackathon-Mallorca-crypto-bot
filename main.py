import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

from pixel_art_gen import generate_and_save_pixel_art

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
WINNERS = set()
AWAITING_IMAGE_DESCRIPTION = set()
AWAITING_DONATION_DETAILS = set()
# GENERATED_IMAGE_URL = ""

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

async def handle_donation_details(update: Update, user_id: int, text: str) -> None:
    try:
        area, months = map(int, text.split())
        donation_amount = area * months * 1  # €1 per square meter per month
        text = f"""
        The total donation amount would be €{donation_amount}.
        If you're happy with the amount, please donate it to our foundation:
        https://seatrees.org/products/restoration-donation
        """
        await update.message.reply_text(text)
        AWAITING_DONATION_DETAILS.remove(user_id)

        text = f"""If you're one of the cool crypto guys, you can also donate by purchasing our NFT. 
        We will mint a unique NFT for you, with the cool image you just generated!
        """
        await update.message.reply_text(text)
        # await update.message.reply_photo(photo=GENERATED_IMAGE_URL, caption=text)

    except ValueError:
        await update.message.reply_text("Please enter two numbers: the area in square meters and the number of months.")

async def handle_pixel_art_request(update: Update, user_id: int, text: str) -> None:
    object_to_paint = text
    GENERATED_IMAGE_URL = generate_and_save_pixel_art(object_to_paint)
    await update.message.reply_photo(photo=GENERATED_IMAGE_URL, caption="Here is your custom pixel art!")
    AWAITING_IMAGE_DESCRIPTION.remove(user_id)
    AWAITING_DONATION_DETAILS.add(user_id)
    text = f"""Do you want to support the restoration of Mallorca beaches? If yes, please enter the area (in square meters) you want to take stuardship for, and for how many months. For exampe: 
    1 12"""
    await update.message.reply_text(text)


async def handle_number_guess(update: Update, user_id: int, text: str) -> None:
    if text in SECRET_NUMBERS:
        USER_SCORES[user_id] += 1
        location, image_url = SECRET_NUMBERS[text]
        congratulations_message = f"Correct! You found our secret QR in {location}. Your score is now {USER_SCORES[user_id]}."
        await update.message.reply_photo(photo=image_url, caption=congratulations_message)
        if USER_SCORES[user_id] == 2:
            WINNERS.add(user_id)
            AWAITING_IMAGE_DESCRIPTION.add(user_id)
            await update.message.reply_text("Congratulations! You won! As a prize, enter a description of anything, and I'll generate a cool pixel art image of it!")
    else:
        await update.message.reply_text("Wrong number, try again!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    user_id = update.effective_user.id

    if user_id not in USER_SCORES:
        USER_SCORES[user_id] = 0

    if user_id in AWAITING_DONATION_DETAILS:
        await handle_donation_details(update, user_id, text)
        return

    if user_id in WINNERS and user_id in AWAITING_IMAGE_DESCRIPTION:
        await handle_pixel_art_request(update, user_id, text)
        return

    if text.isdigit() and len(text) == 5:
        await handle_number_guess(update, user_id, text)
    else:
        if user_id not in WINNERS:
            await update.message.reply_text("Please enter a valid 5-digit number.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(start_game_callback, pattern='^start_game$'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
