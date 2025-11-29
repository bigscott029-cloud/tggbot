from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.helpers import is_coach
from database.connection import cursor, conn
from config.settings import MASTER_ADMIN_ID, COACH_SUPPORT_CHANNEL

async def handle_payment_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    username = update.effective_user.username or "User"
    photo = update.message.photo[-1].file_id

    # Get user's selected package
    cursor.execute("SELECT package, referred_by_coach FROM users WHERE chat_id=%s", (chat_id,))
    row = cursor.fetchone()
    package = row["package"] if row else None
    coach_id = row["referred_by_coach"] if row else None

    # Set correct amount and commission
    if package == "Pro":
        amount = 14500
        commission = 1450
        package_name = "Pro"
    else:
        amount = 7500
        commission = 750
        package_name = "Standard"

    # Save payment
    cursor.execute("""
        INSERT INTO payments (chat_id, coach_id, amount, package, status) 
        VALUES (%s, %s, %s, %s, 'pending') RETURNING id
    """, (chat_id, coach_id, amount, package_name))
    payment_id = cursor.fetchone()["id"]

    # Update coach earnings if applicable
    if coach_id and is_coach(coach_id):
        cursor.execute("""
            UPDATE coaches 
            SET earnings = earnings + %s, total_referrals = total_referrals + 1 
            WHERE chat_id = %s
        """, (commission, coach_id))

    conn.commit()

    # Caption
    caption = (
        f"New Registration Payment\n"
        f"User: @{username} ({chat_id})\n"
        f"Package: {package_name} → ₦{amount:,}\n"
        f"Coach: {coach_id or 'Master Admin'}\n"
        f"Commission: ₦{commission:,} (10%)"
    )

    # Send to Support Channel
    await context.bot.send_photo(
        COACH_SUPPORT_CHANNEL,
        photo,
        caption=caption
    )

    # Send to Master Admin with buttons
    await context.bot.send_photo(
        MASTER_ADMIN_ID,
        photo,
        caption=caption + "\n\nYou have final approval",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Approve", callback_data=f"master_pay_approve_{payment_id}_{chat_id}")],
            [InlineKeyboardButton("Pending", callback_data=f"master_pay_pending_{payment_id}")],
            [InlineKeyboardButton("Reject", callback_data=f"master_pay_reject_{payment_id}_{chat_id}")]
        ])
    )

    # If coach referral → send to coach too
    if coach_id and is_coach(coach_id):
        await context.bot.send_photo(
            coach_id,
            photo,
            caption=caption,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Approve", callback_data=f"coach_pay_approve_{payment_id}_{chat_id}")],
                [InlineKeyboardButton("Reject", callback_data=f"coach_pay_reject_{payment_id}_{chat_id}")]
            ])
        )

    await update.message.reply_text(
        f"Payment screenshot received!\n"
        f"Package: {package_name} (₦{amount:,})\n"
        f"Awaiting approval..."
    )
