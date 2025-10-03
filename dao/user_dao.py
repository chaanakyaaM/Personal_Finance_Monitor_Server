from .dbconfig import get_cursor

class UserDAO:
    def get_user(self, username):
        try:
            with get_cursor() as cur:
                cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            
                user = cur.fetchone()
                return user
            
        except Exception as e:
            return str(e)


    def create_user(self, username, password_hash):
        try:
            with get_cursor() as cur:
                cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id", (username, password_hash))
            
                user_id = cur.fetchone()[0]
                return user_id
            
        except Exception as e:
            return str(e)

    def delete_user(self, user_id):
        try:
            with get_cursor() as cur:
                cur.execute(
                "DELETE FROM transactions WHERE user_id = %s;",
                (user_id, ) 
                )

                transactions_deleted = cur.rowcount

                cur.execute(
                    "DELETE FROM users WHERE id = %s;",
                    (user_id, )
                )

                users_deleted = cur.rowcount

                return {"users_deleted" : users_deleted}
        
        except Exception as e:
            return str(e)
            
