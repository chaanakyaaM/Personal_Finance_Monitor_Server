# Personal Finance Monitor server

This backend powers the core of Personal Finance Monitor, handling user authentication, transaction management, analytics, and admin controls. It ensures secure data handling and provides structured APIs for smooth communication with the frontend.

## API Endpoints

- `POST /register` → Register new user

- `POST /login` → Login existing user

- `POST /transaction` → Add new transaction

- `GET /transaction/<user_id>` → Get user transactions

- `DELETE /delete_transaction/<user_id>/<transaction_id>` → Delete a transaction

- `GET /analytics/<user_id>` → Get analytics for a user

- `GET /output` → Admin panel views

## Environment Variables
- Create a .env file and fill the following variable values:
DB_NAME = YOUR_DB_NAME 
DB_USER = YOUR_DB_USER 
DB_PASSWORD = YOUR_DB_PASSWORD 
DB_HOST = YOUR_DB_HOST 
DB_PORT = YOUR_DB_PORT 

visit this [page](https://github.com/chaanakyaaM/Personal_Finance_Monitor/blob/master/README.md) for more info.

