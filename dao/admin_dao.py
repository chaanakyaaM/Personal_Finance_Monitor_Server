from .dbconfig import get_cursor

class AdminDAO:
    def output(self,key):
        try:
            with get_cursor() as cur:
                cur.execute(f"SELECT * FROM {key};")

                users = cur.fetchall()
                return users
            
        except Exception as e:
            return str(e)

    def desc(self,key):
        try:
            with get_cursor() as cur:
                cur.execute(f"SELECT * FROM {key} LIMIT 0;") 

                column_names = [desc[0] for desc in cur.description]
                return column_names
            
        except Exception as e:
            return str(e)
