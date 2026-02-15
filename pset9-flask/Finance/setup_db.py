#!/usr/bin/env python3
import sqlite3
import os


def setup_database():
    db_exists = os.path.exists('finance.db')

    if db_exists:
        response = input("Database exists. Recreate? (yes/no): ")
        if response.lower() != 'yes':
            print("Setup cancelled.")
            return
        os.remove('finance.db')

    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    with open('schema.sql', 'r') as f:
        cursor.executescript(f.read())

    conn.commit()
    print("✓ Database created successfully!")

    create_test = input("Create test user? (yes/no): ")
    if create_test.lower() == 'yes':
        from werkzeug.security import generate_password_hash
        username = input("Username (default: admin): ") or "admin"
        password = input("Password (default: password): ") or "password"
        hash_pw = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_pw))
        conn.commit()
        print(f"✓ User created: {username}")

    conn.close()
    print("✓ Setup complete!")


if __name__ == "__main__":
    setup_database()
