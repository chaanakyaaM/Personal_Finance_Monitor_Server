import os
import psycopg2
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

password = os.getenv("DB_PASSWORD")
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

# DAO (Data Access Object) layer : Seperates server logic from DB logic
# protocol://user:password@host:port/database

DB_CONFIG = {
    "dbname" : dbname,  
    "user" : user,
    "password" : password,
    "host" : host,
    "port" : port
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