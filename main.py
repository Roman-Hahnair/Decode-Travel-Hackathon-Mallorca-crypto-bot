import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from pixel_art_gen import generate_and_save_pixel_art
from web3_wrapper import is_valid_ethereum_address, mint_nft

# Retrieve token from environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError(
        "No token provided. Set the TELEGRAM_BOT_TOKEN environment variable."
    )

# Mapping secret numbers to locations and their image URLs
SECRET_NUMBERS = {
    "12345": (
        "The cliffs of Santaní",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Mallorca_Santany%C3%AD_Es_Pont%C3%A0s.jpg/640px-Mallorca_Santany%C3%AD_Es_Pont%C3%A0s.jpg",
    ),
    "23456": (
        "The bay Caló des Moro ",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/004_2016_11_29_Menschen_im_Urlaub.jpg/574px-004_2016_11_29_Menschen_im_Urlaub.jpg",
    ),
    "34567": (
        "Cave on the east coast of Majorca",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/003_2014_03_15_Hoehlen_Bergwerke_und_Dolinen.jpg/640px-003_2014_03_15_Hoehlen_Bergwerke_und_Dolinen.jpg",
    ),
    "45678": (
        "The statue of the beach Na Ferradura",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Cala_Rajada_na_Ferradura_escultura_Joan_Benn%C3%A0ssar-1371.jpg/640px-Cala_Rajada_na_Ferradura_escultura_Joan_Benn%C3%A0ssar-1371.jpg",
    ),
    "56789": (
        "Cathedral of Palma de Mallorca",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Consulado_del_Mar%2C_Palma_de_Mallorca%2C_Espa%C3%B1a%2C_2022-10-06%2C_DD_28-30_HDR.jpg/640px-Consulado_del_Mar%2C_Palma_de_Mallorca%2C_Espa%C3%B1a%2C_2022-10-06%2C_DD_28-30_HDR.jpg",
    ),
}
USER_SCORES = {}
WINNERS = set()
AWAITING_IMAGE_DESCRIPTION = set()
AWAITING_DONATION_DETAILS = set()
# GENERATED_IMAGE_URL = ""


async def minting_route(update, text):
    success7, report = mint_nft(text)

    await update.message.reply_text(report)

    if success7:
        await update.message.reply_text(
            "Thank you for your contribution! You will receive your NFT shortly."
        )
    else:
        await update.message.reply_text(
            "Sorry, something went wrong. Please try again later."
        )


"""
async def account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    # user = update.effective_user
    print("In account function...")

    if args:
        address = str(args[0]).strip()
        print(f"Got address from the command: {address}")
        if is_valid_ethereum_address(address):
            await update.message.reply_text(
                f"Got a valid address from the payment page: {address} . Minting NFT..."
            )
            await minting_route(update, address)
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("In the start function...")

    args = context.args
    user = update.effective_user

    if args:
        args_zero = args[0]
        if args_zero in SECRET_NUMBERS:
            await handle_number_guess(update, user.id, args[0])
        elif is_valid_ethereum_address(args_zero):
            await minting_route(update, args_zero)
    else:
        keyboard = [
            [InlineKeyboardButton("Start the Game", callback_data="start_game")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        welcome_message = f"Hello {user.first_name}, I am your bot! Click the button below to start the game."
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=welcome_message,
            reply_markup=reply_markup,
        )


async def start_new_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Game started! Guess the secret 5-digit numbers associated with locations in Mallorca."
    if update.message:
        await update.message.reply_text(text)
    else:
        await update.callback_query.edit_message_text(text)


async def start_game_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    await query.answer()
    await start_new_game(update, context)


async def handle_donation_details(update: Update, user_id: int, text: str) -> None:
    try:
        area, months = map(int, text.split())
        donation_amount = area * months * 1  # €1 per square meter per month
        text = f"""
        The total donation amount would be €{donation_amount}.
        If you're happy with the amount, please contribute here:
        https://bytemeblockheads.tiiny.site/
        """
        await update.message.reply_text(text)
        AWAITING_DONATION_DETAILS.remove(user_id)

        text = f"""If you're one of the cool crypto guys, you can also donate by purchasing our NFT. 
        We will mint a unique NFT for you, with the cool image you just generated! Enter your Ethereum address to receive the NFT (for example, 0x6e339091198CdfbAfE5942e8d4198aC7F84b470e):
        """
        await update.message.reply_text(text)
        # await update.message.reply_photo(photo=GENERATED_IMAGE_URL, caption=text)

    except ValueError:
        await update.message.reply_text(
            "Please enter two numbers: the area in square meters and the number of months."
        )


async def handle_pixel_art_request(update: Update, user_id: int, text: str) -> None:
    await update.message.reply_text(
        "Got it. Generating your unique pixel art... (takes about 10 sec)"
    )
    object_to_paint = text
    GENERATED_IMAGE_URL = generate_and_save_pixel_art(object_to_paint)
    await update.message.reply_photo(
        photo=GENERATED_IMAGE_URL, caption="Here is your custom pixel art!"
    )
    AWAITING_IMAGE_DESCRIPTION.remove(user_id)
    AWAITING_DONATION_DETAILS.add(user_id)
    text = f"""Do you want to support the restoration of Mallorca beaches? If yes, please enter the area (in square meters) you want to take stuardship for, and for how many months. For exampe: 
    1 12"""
    await update.message.reply_text(text)


async def handle_number_guess(update: Update, user_id: int, text: str) -> None:
    if text in SECRET_NUMBERS:

        if user_id not in USER_SCORES:
            USER_SCORES[user_id] = 0

        USER_SCORES[user_id] += 1
        location, image_url = SECRET_NUMBERS[text]
        congratulations_message = f"Correct! You found our secret plaque in {location}. Your score is now {USER_SCORES[user_id]}."
        await update.message.reply_photo(
            photo=image_url, caption=congratulations_message
        )
        if USER_SCORES[user_id] == 2:
            WINNERS.add(user_id)
            AWAITING_IMAGE_DESCRIPTION.add(user_id)
            await update.message.reply_text(
                "Congratulations! You won! As a prize, enter a description of anything, and I'll generate a cool pixel art image of it!"
            )
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

    text = text.strip()
    if is_valid_ethereum_address(text):
        await minting_route(update, text)


async def reset_score(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    # remove the user from the winners list
    if user_id in WINNERS:
        WINNERS.remove(user_id)

    # remove the user from the awaiting image description list
    if user_id in AWAITING_IMAGE_DESCRIPTION:
        AWAITING_IMAGE_DESCRIPTION.remove(user_id)

    # remove the user from the awaiting donation details list
    if user_id in AWAITING_DONATION_DETAILS:
        AWAITING_DONATION_DETAILS.remove(user_id)

    if user_id in USER_SCORES:
        USER_SCORES[user_id] = 0
        await update.message.reply_text(
            "Your score has been reset. Starting a new game..."
        )
    else:
        await update.message.reply_text(
            "You don't have a score to reset. Starting a new game..."
        )

    await start_new_game(update, context)


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    # app.add_handler(CommandHandler("account", account))
    app.add_handler(CallbackQueryHandler(start_game_callback, pattern="^start_game$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("reset", reset_score))
    app.run_polling()


if __name__ == "__main__":
    main()
