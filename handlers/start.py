from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.states import user_state
from database.connection import cursor, conn

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    args = context.args

    # Default registration under Master Admin unless coach link
    cursor.execute("""
        INSERT INTO users (chat_id, referred_by_coach) 
        VALUES (%s, %s) 
        ON CONFLICT (chat_id) DO NOTHING
    """, (chat_id, None))

    if args and args[0].startswith("coach_"):
        try:
            coach_id = int(args[0].split("_")[1])
            cursor.execute("UPDATE users SET referred_by_coach=%s WHERE chat_id=%s", (coach_id, chat_id))
            conn.commit()
        except:
            pass

    user_state[chat_id] = {}
    keyboard = [[InlineKeyboardButton("Get Started", callback_data="menu")]]
    await update.message.reply_text(
        "Welcome to Tapify!\n\n"
        "Earn daily by walking, snapping, posting, and inviting friends.\n"
        "Click below to choose your package and start earning!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query if update.callback_query else None
    chat_id = query.from_user.id if query else update.effective_chat.id

    keyboard = [
        [InlineKeyboardButton("Register / Upgrade", callback_data="package_selector")],
        [InlineKeyboardButton("Help", callback_data="help")],
        [InlineKeyboardButton("Coach Dashboard", callback_data="coach_dashboard")] if is_coach(chat_id) else []
    ]
    keyboard = [x for x in keyboard if x]  # Remove empty
    keyboard += [[InlineKeyboardButton("Back", callback_data="menu")]]

    text = "Tapify Main Menu\n\nChoose an option:"

    if query:
        await query.answer()
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def package_selector(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("FortuneX Standard – ₦7,500", callback_data="pkg_standard")],
        [InlineKeyboardButton("FortuneX Pro – ₦14,500 (Recommended)", callback_data="pkg_pro")],
        [InlineKeyboardButton("Back to Menu", callback_data="menu")]
    ]

    await query.edit_message_text(
        "*Choose Your FortuneX Package*\n\n"
        "Standard – ₦7,500\n"
        "   • Newbie Bonus: ₦7,000\n"
        "   • 10GB Data or ₦5,000 Airtime\n\n"
        "Pro – ₦14,500\n"
        "   • Newbie Bonus: ₦14,000\n"
        "   • 20GB Data or ₦8,000 Airtime\n"
        "   • ₦50k–₦1.5M Loan Access\n"
        "   • 10× Faster Earnings + Priority Tasks",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
