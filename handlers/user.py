# handlers/user.py
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from database.connection import cursor
from utils.helpers import get_coach_badge

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.from_user.id

    cursor.execute("""
        SELECT package, balance, payment_status FROM users WHERE chat_id=%s
    """, (chat_id,))
    user = cursor.fetchone()

    if not user:
        await query.edit_message_text("No data found. Start with /start")
        return

    pkg = user["package"] or "Not selected"
    balance = user["balance"] or 0
    status = user["payment_status"]

    badge = get_coach_badge(chat_id)
    text = (
        f"{badge} *Your FortuneX Stats*\n\n"
        f"Package: {pkg}\n"
        f"Status: {status.title()}\n"
        f"Wallet Balance: ₦{balance:,.2f}\n\n"
        f"Minimum withdrawal: ₦50,000"
    )

    keyboard = []
    if balance >= 10000:
        keyboard.append([InlineKeyboardButton("Withdraw", callback_data="withdraw")])
    keyboard.append([InlineKeyboardButton("Back to Menu", callback_data="menu")])

    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
