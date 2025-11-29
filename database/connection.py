import psycopg
import os
from dotenv import load_dotenv
load_dotenv()

conn = psycopg.connect(os.getenv("DATABASE_URL"), autocommit=True)
cursor = conn.cursor(row_factory=psycopg.rows.dict_row)
