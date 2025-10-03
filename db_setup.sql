-- Create 'users' table

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,  
    username VARCHAR(50) UNIQUE NOT NULL,  
    password_hash VARCHAR(225) NOT NULL  
);

-- Create 'transactions' table

CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,  
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    category VARCHAR(20) NOT NULL CHECK (category IN ('income', 'expense')),
    type VARCHAR(20) NOT NULL,
    amount NUMERIC(10,2) NOT NULL,  
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    notes TEXT 
);

