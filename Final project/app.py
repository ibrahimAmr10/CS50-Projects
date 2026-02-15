from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# Database setup
DB_PATH = 'finance.db'

def init_db():
    """Initialize the database with the calculations table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number1 REAL NOT NULL,
            number2 REAL NOT NULL,
            operator TEXT NOT NULL,
            result REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database when app starts
init_db()

@app.route('/')
def index():
    """Main calculator page"""
    return render_template('index.html')

@app.route('/history')
def history():
    """History page showing all past calculations"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT number1, number2, operator, result, timestamp 
        FROM calculations 
        ORDER BY timestamp DESC
    ''')
    calculations = cursor.fetchall()
    conn.close()
    return render_template('history.html', calculations=calculations)

@app.route('/calculate', methods=['POST'])
def calculate():
    """Handle calculation requests and save to database"""
    try:
        data = request.get_json()
        number1 = float(data['number1'])
        number2 = float(data['number2'])
        operator = data['operator']
        
        # Perform calculation based on operator
        if operator == '+':
            result = number1 + number2
        elif operator == '-':
            result = number1 - number2
        elif operator == '*':
            result = number1 * number2
        elif operator == '/':
            if number2 == 0:
                return jsonify({'error': 'Cannot divide by zero'}), 400
            result = number1 / number2
        elif operator == '%':
            result = number1 % number2
        else:
            return jsonify({'error': 'Invalid operator'}), 400
        
        # Save to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO calculations (number1, number2, operator, result)
            VALUES (?, ?, ?, ?)
        ''', (number1, number2, operator, result))
        conn.commit()
        conn.close()
        
        return jsonify({'result': result})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear-history', methods=['POST'])
def clear_history():
    """Clear all calculation history"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM calculations')
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
