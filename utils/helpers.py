from database.connection import cursor
from config.settings import MASTER_ADMIN_ID, COACH_SUPPORT_CHANNEL

def is_master_admin(chat_id): return chat_id == MASTER_ADMIN_ID
def is_coach(chat_id):
    cursor.execute("SELECT 1 FROM coaches WHERE chat_id=%s AND is_active=TRUE", (chat_id,))
    return cursor.fetchone() is not None

def get_coach_badge(chat_id):
    return " (Crown Coach)" if is_coach(chat_id) else ""

def get_leaderboard():
    cursor.execute("""
        SELECT chat_id, earnings, total_referrals 
        FROM coaches 
        WHERE is_active=TRUE 
        ORDER BY earnings DESC LIMIT 10
    """)
    rows = cursor.fetchall()
    text = "Crown Coach Leaderboard (Top Earners)\n\n"
    for i, row in enumerate(rows, 1):
        username = f"Coach {row['chat_id']}"
        cursor.execute("SELECT username FROM users WHERE chat_id=%s", (row['chat_id'],))
        u = cursor.fetchone()
        if u and u["username"]:
            username = f"@{u['username']}"
        text += f"{i}. {username} — ₦{row['earnings']:,.0f} ({row['total_referrals']} refs)\n"
    return text
