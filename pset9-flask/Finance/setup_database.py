#!/usr/bin/env python3
"""
Database Setup Script for Finance App
Run this script to create the SQLite database with all required tables and indexes
"""

from cs50 import SQL
import os


def setup_database():
    """Create database tables and indexes"""

    # Check if database already exists
    db_exists = os.path.exists("finance.db")

    if db_exists:
        print("⚠️  Database 'finance.db' already exists!")
        response = input("Do you want to recreate it? (yes/no): ").lower()
        if response != 'yes':
            print("Setup cancelled.")
            return
        os.remove("finance.db")
        print("✅ Old database removed.")

    # Connect to database
    db = SQL("sqlite:///finance.db")

    print("📊 Creating database tables...")

    # Create users table
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            hash TEXT NOT NULL,
            cash NUMERIC NOT NULL DEFAULT 10000.00
        )
    """)
    print("✅ Table 'users' created successfully")

    # Create index on username
    db.execute("CREATE UNIQUE INDEX IF NOT EXISTS username_index ON users (username)")
    print("✅ Index 'username_index' created successfully")

    # Create transactions table
    db.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            shares INTEGER NOT NULL,
            price NUMERIC NOT NULL,
            transaction_type TEXT NOT NULL CHECK(transaction_type IN ('BUY', 'SELL')),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    print("✅ Table 'transactions' created successfully")

    # Create indexes for better performance
    db.execute("CREATE INDEX IF NOT EXISTS user_transactions_index ON transactions (user_id)")
    db.execute("CREATE INDEX IF NOT EXISTS symbol_index ON transactions (symbol)")
    db.execute("CREATE INDEX IF NOT EXISTS timestamp_index ON transactions (timestamp DESC)")
    print("✅ Indexes created successfully")

    print("\n🎉 Database setup completed successfully!")
    print("\n📝 Next steps:")
    print("1. Run: python app.py")
    print("2. Open browser to: http://127.0.0.1:5000")
    print("3. Register a new account")
    print("4. Start trading!\n")


if __name__ == "__main__":
    try:
        setup_database()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure you have installed all requirements:")
        print("pip install -r requirements.txt")
