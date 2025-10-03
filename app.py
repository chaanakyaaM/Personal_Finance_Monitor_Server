from flask_cors import CORS 
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from dao import admin_dao, analytics_dao, transactions_dao, user_dao

app = Flask(__name__)
CORS(app)

userDAO = user_dao.UserDAO()
adminDAO = admin_dao.AdminDAO()
transactionsDAO = transactions_dao.TransactionDAO()
analyticsDAO = analytics_dao.AnalyticsDAO()

@app.route("/",methods = ["GET"])
def home():
    return jsonify({
        "message" : "server is active"
    })

@app.route("/register", methods = ["POST"])
def register():
    try:
        data = request.json
        username = data.get("username")
        password_hash = data.get("password_hash")

        if userDAO.get_user(username):
            return jsonify({"error" : "User already exists"}), 400
        
        password_hash = generate_password_hash(password_hash)

        user_id = userDAO.create_user(username, password_hash)

        return jsonify({
                "message" : "User created successfully",
                "auth":True,
                "user_id" : user_id,
            })
    
    except Exception as e:
        return jsonify({
            "error":f"Error at DB level: {str(e)}"
        })


@app.route("/login", methods = ["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password_hash")

    user = userDAO.get_user(username)

    if username == "admin" and check_password_hash(user[2], password):
        return jsonify({
            "message" : "Admin login successful",
            "auth" : False,
            "admin":True
        })

    if not user:
        return jsonify({"error": "User does not exits"}),400
    
    stored_hash = user[2]  # id=0, username=1, password_hash=2
    
    if not check_password_hash(stored_hash, password):
        return jsonify({
        "error" : "Invalid password",
        "auth" : False}),401

    return jsonify({
        "auth" : True,
        "message" : "Login successful",
        "user_id" : user[0]})

@app.route("/transaction", methods = ["POST"])
def transaction():
    data = request.json
    user_id = data.get("user_id")
    type = data.get("type")
    category = data.get("category")
    amount = data.get("amount")
    notes = data.get("notes", "")

    try:
        trans_id = transactionsDAO.add_transaction(user_id = user_id, category = category, type = type, amount = amount, notes = notes)
        return jsonify({
            "message" : "Transaction added successfully",
            "transaction_id" : trans_id
        })
    
    except Exception as e:
        return jsonify({
            "error" : f"Error at DB level: {str(e)}"
        })

@app.route("/transaction/<int:user_id>", methods = ["GET"])
def get_transaction(user_id):
    try:
        transactions = transactionsDAO.get_transaction(user_id)
        return jsonify(transactions)
    except Exception as e:
        return jsonify({
            "error" : str(e)
        })

@app.route("/output",methods=["GET"])
def output():
    try:
        output1 = adminDAO.output("users")
        output2 = adminDAO.output("transactions")

        desc1 = adminDAO.desc("users")
        desc2 = adminDAO.desc("transactions")

        return jsonify({
            "labels" : {
                "users" : desc1,
                "transactions" : desc2,
            },
            "values" : {
            "users" : output1,
            "transactions" : output2,
            }
        })
    except Exception as e:
        return jsonify({
            "error" : f"error at DB level {str(e)}"
        })


@app.route("/analytics/<int:user_id>", methods=["GET"])
def analytics(user_id):
    try:
        data = analyticsDAO.analytics(user_id)

        return jsonify({
            "income" : data.get("income"),
            "expense": data.get("expense"),
            "total_transactions" : data.get("total_transactions"),
            "net" : data.get("net"),
            "income_type_breakdown" : data.get("income_type_breakdown"),
            "expense_type_breakdown" : data.get("expense_type_breakdown"),
            "monthly" : data.get("monthly"),
            "category_type_breakdown" : data.get("category_type_breakdown"),
            "daily" : data.get("daily"),
            "rows" : data.get("rows")
        })
    
    except Exception as e:
        return jsonify({
            "error" : f"error at DB level {str(e)}"
        })
    
@app.route("/delete_transaction/<int:user_id>/<int:transaction_id>", methods = ["DELETE"])
def delete_transaction(user_id, transaction_id):
    try:
        res = transactionsDAO.delete_transaction(user_id, transaction_id)

        if res:
            return jsonify({
                "message" : "Transaction deleted successfully"
            })
    except Exception as e:
        return jsonify({
            "error" : f"Error at DB level: {str(e)}"
        })

@app.route("/delete_user/<int:user_id>", methods = ["DELETE"])
def delete_user(user_id):
    try:
        res = userDAO.delete_user(int(user_id))
        if res:
            if res.get("users_deleted") > 0:
                return jsonify({
                    "message" : "User deleted successfully"
                }),200
    except Exception as e:
        return jsonify({
            "error" : f"Error at DB level: {str(e)}"
        })


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 5000)
