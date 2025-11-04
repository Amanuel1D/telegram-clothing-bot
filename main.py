from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

BOT_TOKEN = "PASTE_YOUR_TOKEN_HERE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👗 Welcome to My Clothing Store!\nSend /post to add a product.")

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.username != "YOUR_TELEGRAM_USERNAME":
        await update.message.reply_text("❌ You don't have permission to post.")
        return
    await update.message.reply_text("Send a product photo with caption (e.g., Dress name and short desc).")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.username != "YOUR_TELEGRAM_USERNAME":
        return

    photo = update.message.photo[-1].file_id
    caption = update.message.caption or "New product"

    keyboard = [
        [InlineKeyboardButton("📤 Share to Friend", switch_inline_query=caption)],
        [InlineKeyboardButton("💬 Ask Price", callback_data="ask_price"),
         InlineKeyboardButton("🛒 Buy It", callback_data="buy")],
        [InlineKeyboardButton("🗨️ Leave a Comment", callback_data="comment")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.bot.send_photo(
        chat_id=update.message.chat_id,
        photo=photo,
        caption=caption,
        reply_markup=reply_markup
    )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "ask_price":
        await query.from_user.send_message("💲 The price will be shared with you privately. Example: $25")
    elif query.data == "buy":
        await query.from_user.send_message("🛒 Please message @YOUR_PERSONAL_ACCOUNT to complete your purchase.")
    elif query.data == "comment":
        await query.message.reply_text("💬 Reply to this message with your comment!")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("post", post))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(CallbackQueryHandler(button_click))

print("Bot is running...")
app.run_polling()
