from .dbconfig import get_cursor

class AnalyticsDAO:
    def analytics(self,user_id):
        try:
            with get_cursor() as cur:
                cur.execute("""
                    SELECT SUM(Amount) FROM transactions WHERE user_id = %s AND category = 'income';
                            """,(user_id,))
                
                income = cur.fetchone()[0] or 0

                cur.execute("""
                    SELECT SUM(Amount) FROM transactions WHERE user_id = %s AND category = 'expense';
                            """,(user_id,))
                
                expense = cur.fetchone()[0] or 0

                cur.execute("""
                    SELECT COUNT(*) FROM transactions WHERE user_id = %s ;
                            """,(user_id,))

                total_transactions = cur.fetchone()[0] or 0    

                cur.execute("""
                    SELECT type, SUM(amount) FROM transactions WHERE user_id = %s AND category = 'income' 
                    GROUP BY type;""",(user_id,))
                
                income_type_breakdown = cur.fetchall()

                cur.execute("""
                    SELECT type, SUM(amount) FROM transactions WHERE user_id = %s AND category = 'expense' 
                    GROUP BY type;""",(user_id,))
                
                expense_type_breakdown = cur.fetchall()

                cur.execute("""
                    SELECT 
                        DATE_TRUNC('month', date) AS month_start,
                        category,
                        SUM(amount)
                    FROM transactions
                    WHERE user_id = %s
                    GROUP BY month_start, category
                    ORDER BY month_start;
                """, (user_id,))
                
                monthly = cur.fetchall()

                cur.execute("""
                    SELECT category, type, SUM(amount) FROM transactions WHERE user_id = %s
                    GROUP BY category, type;
                """,(user_id,))

                category_type_breakdown = cur.fetchall()

                cur.execute("""

                    SELECT DATE(date) AS day, category, SUM(amount) 
                    FROM transactions 
                    WHERE user_id = %s
                    GROUP BY day, category
                    ORDER BY day;
                """, (user_id,))
                
                daily  = cur.fetchall()

                cur.execute("""
                SELECT 
                    DATE(date) AS day,
                    category,
                    SUM(amount) AS total
                FROM transactions
                WHERE user_id = %s
                GROUP BY day, category
                ORDER BY day;
                """, (user_id,))
                
                rows = cur.fetchall()     

                return ({
                    "income":income,
                    "expense": expense,
                    "total_transactions": total_transactions,
                    "net": int(income) - int(expense),
                    "income_type_breakdown":income_type_breakdown,
                    "expense_type_breakdown":expense_type_breakdown,
                    "monthly":monthly,
                    "category_type_breakdown": category_type_breakdown,
                    "daily": daily,
                    "rows":rows
                })
        except Exception as e:
            return str(e)
