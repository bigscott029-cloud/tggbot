from .connection import cursor, conn
from datetime import datetime

def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id BIGINT PRIMARY KEY,
            username TEXT,
            package TEXT,
            payment_status TEXT DEFAULT 'new',
            name TEXT,
            email TEXT,
            phone TEXT,
            password TEXT,
            balance REAL DEFAULT 0,
            referral_code TEXT,
            referred_by BIGINT,
            referred_by_coach BIGINT,
            join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS coaches (
            chat_id BIGINT PRIMARY KEY,
            approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            approved_by BIGINT,
            is_active BOOLEAN DEFAULT TRUE,
            earnings REAL DEFAULT 0,
            total_referrals INTEGER DEFAULT 0,
            last_payout TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS payments (
            id SERIAL PRIMARY KEY,
            chat_id BIGINT,
            type TEXT DEFAULT 'registration',
            amount INTEGER,
            coach_id BIGINT,
            status TEXT DEFAULT 'pending',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS coach_tasks (
            id SERIAL PRIMARY KEY,
            title TEXT,
            reward REAL,
            link TEXT,
            assigned_by BIGINT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()

create_tables()
