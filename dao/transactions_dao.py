from .dbconfig import get_cursor

class TransactionDAO:
    def add_transaction(self,user_id, type, category, amount, notes = ""):
        try:
            with get_cursor() as cur:
                cur.execute("""INSERT INTO transactions (user_id, category,type, amount, notes)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id;""", (user_id, category, type, amount, notes))  
                
                trans_id = cur.fetchone()[0]
                return trans_id
            
        except Exception as e:
            return str(e)

    def get_transaction(self,user_id):
        try:
            with get_cursor() as cur:
                cur.execute("""
                    SELECT id, date, category, type, amount , notes
                    FROM transactions where user_id = %s;
                """, (user_id,))

                transactions = cur.fetchall()
                return transactions
            
        except Exception as e:
            return str(e)
        
    def delete_transaction(self, user_id, transaction_id):
        try:
            with get_cursor() as cur:
                cur.execute("""
                    DELETE FROM transactions WHERE id = %s AND user_id = %s;
                            """,(transaction_id, user_id))
                
                return True

        except Exception as e:
            return str(e)
