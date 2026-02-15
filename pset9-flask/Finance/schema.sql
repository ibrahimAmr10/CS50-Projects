-- SQLite Database Setup for Finance App
-- Run this script to create the database tables

-- Table for users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    cash NUMERIC NOT NULL DEFAULT 10000.00
);

-- Create index on username for faster lookups
CREATE UNIQUE INDEX IF NOT EXISTS username_index ON users (username);

-- Table for transactions
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,
    price NUMERIC NOT NULL,
    transaction_type TEXT NOT NULL CHECK(transaction_type IN ('BUY', 'SELL')),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS user_transactions_index ON transactions (user_id);
CREATE INDEX IF NOT EXISTS symbol_index ON transactions (symbol);
CREATE INDEX IF NOT EXISTS timestamp_index ON transactions (timestamp DESC);

-- Example: Insert a test user (password is 'password123')
-- Password hash for 'password123' generated using werkzeug
-- INSERT INTO users (username, hash, cash) 
-- VALUES ('testuser', 'pbkdf2:sha256:600000$...$...', 10000.00);
