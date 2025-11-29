# handlers/tasks.py
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from database.connection import cursor

async def daily_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.from_user.id

    cursor.execute("SELECT package FROM users WHERE chat_id=%s", (chat_id,))
    pkg = cursor.fetchone()["package"]

    if pkg == "Pro":
        link = "https://t.me/your_pro_tasks_channel"
    else:
        link = "https://t.me/your_standard_tasks"

    await query.edit_message_text(
        f"Daily Tasks\n\n"
        f"Complete today's tasks here:\n{link}\n\n"
        f"Earn up to ₦15,000 daily!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Open Tasks", url=link)],
            [InlineKeyboardButton("Back", callback_data="menu")]
        ])
    )

async def earn_extra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "Extra Tasks Coming Soon!\n\n"
        "High-reward tasks will appear here for active users.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Back", callback_data="menu")]
        ])
    )
