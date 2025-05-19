from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Token va admin ID
TOKEN = "7914388971:AAGDeHZXlTaw-cwsWFvTGcwMP3TTASQemHg"
ADMIN_CHAT_ID = 5350323509  # Sizning Telegram ID'ingiz

# Menyu
menu_buttons = [
    ["To'y holva", "Beshik holva"],
    ["Yong'oq holva"],
    ["Buyurtmani yakunlash"]
]
menu_keyboard = ReplyKeyboardMarkup(menu_buttons, resize_keyboard=True)

# Buyurtmalar
orders = {}

# Mahsulotlar haqida ma'lumot
items = {
    "To'y holva": {
        "price": 87000,
        "image": "https://i.ibb.co/Kjgwj3wX/IMG-20241017-153645-099.webp"
    },
    "Beshik holva": {
        "price": 115000,
        "image": "https://i.ibb.co/Kjgwj3wX/IMG-20241017-153645-099.webp"
    },
    "Yong'oq holva": {
        "price": 48000,
        "image": "https://i.ibb.co/JRMnSMgy/IMG-20240223-192446-423.jpg"
    }
}

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    orders[user_id] = {}

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=items["To'y holva"]["image"],
        caption="Bek holva botiga xush kelibsiz! Holvani tanlang:",
        reply_markup=menu_keyboard
    )

# Xabarni qayta ishlash
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id not in orders:
        orders[user_id] = {}

    if text == "Buyurtmani yakunlash":
        user_orders = orders[user_id]
        if user_orders:
            order_lines = []
            total = 0
            for item, qty in user_orders.items():
                price = items[item]["price"]
                subtotal = price * qty
                total += subtotal
                order_lines.append(f"{item} – {qty} dona = {subtotal:,} so‘m")

            order_text = "Sizning buyurtmangiz:\n" + "\n".join(order_lines)
            order_text += f"\n\nJami: {total:,} so‘m"

            await update.message.reply_text(order_text)

            # Adminga yuborish
            user_info = f"Foydalanuvchi: {update.effective_user.full_name} (ID: {user_id})"
            admin_text = f"YANGI BUYURTMA!\n{user_info}\n" + "\n".join(order_lines) + f"\n\nJami: {total:,} so‘m"
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_text)

            orders[user_id] = {}
        else:
            await update.message.reply_text("Siz hali buyurtma bermadingiz.")
    elif text in items:
        orders[user_id][text] = orders[user_id].get(text, 0) + 1
        count = orders[user_id][text]
        await update.message.reply_photo(
            photo=items[text]["image"],
            caption=f"{text} – {count} dona buyurtmangizga qo‘shildi."
        )
    else:
        await update.message.reply_text("Iltimos, menyudan tanlang.")

# Botni ishga tushurish
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot ishga tushdi...")
    app.run_polling()()
