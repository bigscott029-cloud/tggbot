from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.helpers import is_master_admin
from database.connection import cursor, conn

async def removecoach(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_master_admin(update.effective_chat.id):
        return
    if not context.args:
        await update.message.reply_text("Usage: /removecoach <chat_id>")
        return
    coach_id = int(context.args[0])
    cursor.execute("UPDATE coaches SET is_active=FALSE WHERE chat_id=%s", (coach_id,))
    conn.commit()
    await update.message.reply_text(f"Coach {coach_id} removed.")

def get_admin_handlers():
    return [
        CommandHandler("removecoach", removecoach),
    ]
