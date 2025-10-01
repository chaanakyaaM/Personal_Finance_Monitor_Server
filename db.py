# import os
# import dotenv
# import psycopg2
# from contextlib import contextmanager

# dotenv.load_dotenv()

# password = os.getenv("DB_PASSWORD")
# dbname = os.getenv("DB_NAME")
# user = os.getenv("DB_USER")

# DAO (Data Access Object) layer : Seperates server logic from DB logic

# DB_CONFIG = {
#     "dbname" : dbname,  
#     "user" : user,
#     "password" : password,
#     "host" : "localhost",
#     "port" : "5432"
# }

# @contextmanager
# def get_cursor():
#     conn = Database_Connection.get_connection()
#     try:
#         yield conn.cursor()
#         conn.commit()
#     except Exception as e:
#         conn.rollback()
#         raise e
#     finally:
#         conn.close()

# Establish a connection to the PostgreSQL database
# class Database_Connection:
#     @staticmethod
#     def get_connection():
#         try:
#             return psycopg2.connect(**DB_CONFIG)
        
#         except Exception as e:
#             return "error at connection level:" + str(e)

# class UserDAO:
#     def get_user(self,username):
#         try:
#             with get_cursor() as cur:
#                 cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            
#                 user = cur.fetchone()
#                 return user
            
#         except Exception as e:
#             return str(e)


#     def create_user(self,username, password_hash):
#         try:
#             with get_cursor() as cur:
#                 cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id", (username, password_hash))
            
#                 user_id = cur.fetchone()[0]
#                 cur.connection.commit()
#                 return user_id
            
#         except Exception as e:
#             return str(e)

# class TransactionDAO:
#     def add_transaction(self,user_id, type, category, amount, notes = ""):
#         try:
#             with get_cursor() as cur:
#                 cur.execute("""INSERT INTO transactions (user_id, category,type, amount, notes)
#                     VALUES (%s, %s, %s, %s, %s) RETURNING id;""", (user_id, category, type, amount, notes))  
                
#                 trans_id = cur.fetchone()[0]
#                 cur.connection.commit()
#                 return trans_id
            
#         except Exception as e:
#             return str(e)

#     def get_transaction(self,user_id):
#         try:
#             with get_cursor() as cur:
#                 cur.execute("""
#                     SELECT id, date, category, type, amount , notes
#                     FROM transactions where user_id = %s;
#                 """, (user_id,))

#                 transactions = cur.fetchall()
#                 return transactions
            
#         except Exception as e:
#             return str(e)
        
#     def delete_transaction(self, user_id, transaction_id):
#         try:
#             with get_cursor() as cur:
#                 cur.execute("""
#                     DELETE FROM transactions WHERE id = %s AND user_id = %s;
#                             """,(transaction_id, user_id))
                
#                 cur.connection.commit()
#                 return True

#         except Exception as e:
#             return str(e)

# class AdminDAO:
#     def output(self,key):
#         try:
#             with get_cursor() as cur:
#                 cur.execute(f"SELECT * FROM {key};")

#                 users = cur.fetchall()
#                 return users
            
#         except Exception as e:
#             return str(e)

#     def desc(self,key):
#         try:
#             with get_cursor() as cur:
#                 cur.execute(f"SELECT * FROM {key} LIMIT 0;") 

#                 column_names = [desc[0] for desc in cur.description]
#                 return column_names
            
#         except Exception as e:
#             return str(e)

# class AnalyticsDAO:
#     def analytics(self,user_id):
#         try:
#             with get_cursor() as cur:
#                 cur.execute("""
#                     SELECT SUM(Amount) FROM transactions WHERE user_id = %s AND category = 'income';
#                             """,(user_id,))
                
#                 income = cur.fetchone()[0] or 0

#                 cur.execute("""
#                     SELECT SUM(Amount) FROM transactions WHERE user_id = %s AND category = 'expense';
#                             """,(user_id,))
                
#                 expense = cur.fetchone()[0] or 0

#                 cur.execute("""
#                     SELECT COUNT(*) FROM transactions WHERE user_id = %s ;
#                             """,(user_id,))

#                 total_transactions = cur.fetchone()[0] or 0    

#                 cur.execute("""
#                     SELECT type, SUM(amount) FROM transactions WHERE user_id = %s AND category = 'income' 
#                     GROUP BY type;""",(user_id,))
                
#                 income_type_breakdown = cur.fetchall()

#                 cur.execute("""
#                     SELECT type, SUM(amount) FROM transactions WHERE user_id = %s AND category = 'expense' 
#                     GROUP BY type;""",(user_id,))
                
#                 expense_type_breakdown = cur.fetchall()

#                 cur.execute("""
#                     SELECT 
#                         DATE_TRUNC('month', date) AS month_start,
#                         category,
#                         SUM(amount)
#                     FROM transactions
#                     WHERE user_id = %s
#                     GROUP BY month_start, category
#                     ORDER BY month_start;
#                 """, (user_id,))
                
#                 monthly = cur.fetchall()

#                 cur.execute("""
#                     SELECT category, type, SUM(amount) FROM transactions WHERE user_id = %s
#                     GROUP BY category, type;
#                 """,(user_id,))

#                 category_type_breakdown = cur.fetchall()

#                 cur.execute("""

#                     SELECT DATE(date) AS day, category, SUM(amount) 
#                     FROM transactions 
#                     WHERE user_id = %s
#                     GROUP BY day, category
#                     ORDER BY day;
#                 """, (user_id,))
                
#                 daily  = cur.fetchall()

#                 cur.execute("""
#                 SELECT 
#                     DATE(date) AS day,
#                     category,
#                     SUM(amount) AS total
#                 FROM transactions
#                 WHERE user_id = %s
#                 GROUP BY day, category
#                 ORDER BY day;
#                 """, (user_id,))
                
#                 rows = cur.fetchall()     

#                 return ({
#                     "income":income,
#                     "expense": expense,
#                     "total_transactions": total_transactions,
#                     "net": int(income) - int(expense),
#                     "income_type_breakdown":income_type_breakdown,
#                     "expense_type_breakdown":expense_type_breakdown,
#                     "monthly":monthly,
#                     "category_type_breakdown": category_type_breakdown,
#                     "daily": daily,
#                     "rows":rows
#                 })
#         except Exception as e:
#             return str(e)

