import os
import psycopg2
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

password = os.getenv("DB_PASSWORD")
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")

# DAO (Data Access Object) layer : Seperates server logic from DB logic

DB_CONFIG = {
    "dbname" : dbname,  
    "user" : user,
    "password" : password,
    "host" : "localhost",
    "port" : "5432"
}

@contextmanager
def get_cursor():
    conn = Database_Connection.get_connection()
    try:
        yield conn.cursor()
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

class Database_Connection:
    @staticmethod
    def get_connection():
        try:
            return psycopg2.connect(**DB_CONFIG)
        
        except Exception as e:
            return "error at connection level:" + str(e)