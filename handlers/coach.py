# handlers/coach.py
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.helpers import is_coach, is_master_admin, get_coach_badge, get_leaderboard
from database.connection import cursor, conn
from config.settings import MASTER_ADMIN_ID


async def apply_coach(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.from_user.id
    username = query.from_user.username or "User"
    full_name = query.from_user.full_name

    if is_coach(chat_id):
        await query.edit_message_text("You are already an approved FortuneX Coach!")
        return

    await context.bot.send_message(
        chat_id=MASTER_ADMIN_ID,
        text=f"New FortuneX Coach Application!\n\n"
             f"User: @{username}\n"
             f"Name: {full_name}\n"
             f"ID: {chat_id}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Approve Coach", callback_data=f"coach_approve_{chat_id}")],
            [InlineKeyboardButton("Reject Coach", callback_data=f"coach_reject_{chat_id}")]
        ])
    )

    await query.edit_message_text(
        "Your application to become a FortuneX Coach has been sent!\n\n"
        "You will earn 10% commission (₦750–₦1,450) on every registration via your link.\n"
        "You’ll be notified once approved."
    )


async def coach_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.from_user.id

    if not is_coach(chat_id):
        await query.edit_message_text("You are not an approved FortuneX Coach yet.")
        return

    cursor.execute("SELECT earnings, total_referrals FROM coaches WHERE chat_id = %s", (chat_id,))
    row = cursor.fetchone()
    earnings = row["earnings"] if row else 0
    referrals = row["total_referrals"] if row else 0

    ref_link = f"https://t.me/{context.bot.username}?start=coach_{chat_id}"

    text = (
        f"{get_coach_badge(chat_id)} *FortuneX Coach Dashboard*\n\n"
        f"Total Earnings: *₦{earnings:,.0f}*\n"
        f"Successful Referrals: *{referrals}*\n\n"
        f"Your Referral Link:\n`{ref_link}`\n\n"
        f"Commission Rate: 10% per registration\n"
        f"Auto-payout every Monday (minimum ₦5,000)"
    )

    keyboard = [
        [InlineKeyboardButton("My Referral Link", callback_data="coach_show_link")],
        [InlineKeyboardButton("View Leaderboard", callback_data="coach_leaderboard")],
        [InlineKeyboardButton("Pending Payments", callback_data="coach_pending")],
        [InlineKeyboardButton("Refresh Dashboard", callback_data="coach_dashboard")],
        [InlineKeyboardButton("Back to Menu", callback_data="menu")]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )


async def show_coach_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.from_user.id
    link = f"https://t.me/{context.bot.username}?start=coach_{chat_id}"

    await query.edit_message_text(
        f"Your FortuneX Coach Link:\n\n`{link}`\n\n"
        f"Share this → earn ₦750 (Standard) or ₦1,450 (Pro) per paid user!",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Back to Dashboard", callback_data="coach_dashboard")]
        ])
    )


async def show_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    leaderboard = get_leaderboard().replace("Coach", "FortuneX Coach")
    await query.edit_message_text(
        leaderboard,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Back to Dashboard", callback_data="coach_dashboard")]
        ])
    )
