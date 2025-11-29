from telegram.ext import Application
from datetime import datetime
from database.connection import cursor, conn
from utils.helpers import get_leaderboard

def setup_jobs(app: Application):
    async def weekly_payout(context):
        cursor.execute("SELECT chat_id, earnings FROM coaches WHERE earnings >= 5000 AND is_active=TRUE")
        for row in cursor.fetchall():
            chat_id, earnings = row["chat_id"], row["earnings"]
            await context.bot.send_message(chat_id, f"Auto-Payout! ₦{earnings:,.0f} sent to your account.")
            cursor.execute("UPDATE coaches SET earnings=0, last_payout=%s WHERE chat_id=%s", (datetime.now(), chat_id))
        conn.commit()

    async def weekly_leaderboard(context):
        await context.bot.send_message(COACH_SUPPORT_CHANNEL, get_leaderboard())

    app.job_queue.run_repeating(weekly_payout, interval=604800, first=10)  # Every Monday
    app.job_queue.run_repeating(weekly_leaderboard, interval=604800, first=20)
