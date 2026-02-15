from cs50 import SQL
from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from helpers import lookup, usd, apology, login_required


app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "your-secret-key-change-this"  # Change this to a random secret key!
Session(app)

# Register the usd filter for Jinja templates
app.jinja_env.filters["usd"] = usd

db = SQL("sqlite:///finance.db")

# Login required decorator


def login_required(f):
    """
    Decorate routes to require login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Username is required", 400)
        elif not password:
            return apology("Password is required", 400)
        elif not confirmation:
            return apology("Password confirmation is required", 400)
        elif password != confirmation:
            return apology("Passwords do not match", 400)
        elif len(password) < 6:
            return apology("Password must be at least 6 characters", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            return apology("Username already exists", 400)

        try:
            hash_pw = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pw)
            flash("Registration successful! Please log in.", "success")
            return redirect("/login")
        except Exception as e:
            return apology("Registration failed Please try again", 400)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("Username is required", 400)
        elif not password:
            return apology("Password is required", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]['hash'], password):
            return apology("Invalid username and/or password", 400)

        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        flash(f"Welcome back, {username}!", "success")
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    username = session.get("username", "User")
    session.clear()
    flash(f"Goodbye, {username}!", "success")
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote"""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Symbol is required", 400)

        stock = lookup(symbol.upper().strip())
        if stock is None:
            return apology(f"Invalid symbol {symbol}", 400)

        return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("Symbol is required", 400)

        if not shares:
            return apology("Number of shares is required", 400)

        try:
            shares = int(shares)
            if shares <= 0:
                return apology("Shares must be a positive number", 400)
        except ValueError:
            return apology("Shares must be a valid number", 400)

        stock = lookup(symbol.upper().strip())

        if stock is None:
            return apology(f"Invalid symbol {symbol}", 400)

        cost = shares * stock['price']
        user = db.execute("SELECT cash FROM users WHERE id = ?", session['user_id'])[0]

        if user['cash'] < cost:
            return apology(f"Not enough cash You need {usd(cost)} but only have {usd(user['cash'])}", 400)

        try:
            db.execute(
                "INSERT INTO transactions (user_id, symbol, shares, price, transaction_type) VALUES (?, ?, ?, ?, 'BUY')",
                session['user_id'], stock['symbol'], shares, stock['price']
            )
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, session['user_id'])
            flash(
                f"Successfully bought {shares} shares of {stock['symbol']} for {usd(cost)}!", "success")
            return redirect("/")
        except Exception as e:
            return apology("Transaction failed Please try again", 400)
    else:
        return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total > 0",
        session['user_id']
    )

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_to_sell = request.form.get("shares")

        if not symbol:
            return apology("Symbol is required", 400)

        if not shares_to_sell:
            return apology("Number of shares is required", 400)

        try:
            shares_to_sell = int(shares_to_sell)
            if shares_to_sell <= 0:
                return apology("Shares must be a positive number", 400)
        except ValueError:
            return apology("Shares must be a valid number", 400)

        owned_result = db.execute(
            "SELECT SUM(shares) as total FROM transactions WHERE user_id = ? AND symbol = ?",
            session['user_id'], symbol
        )

        owned = owned_result[0]['total'] if owned_result and owned_result[0]['total'] is not None else 0

        if shares_to_sell > owned:
            return apology(f"You don't have enough shares You only own {owned} shares of {symbol}", 400)

        stock = lookup(symbol.upper().strip())
        if stock is None:
            return apology(f"Invalid symbol {symbol}", 400)

        revenue = shares_to_sell * stock['price']

        try:
            db.execute(
                "INSERT INTO transactions (user_id, symbol, shares, price, transaction_type) VALUES (?, ?, ?, ?, 'SELL')",
                session['user_id'], symbol, -shares_to_sell, stock['price']
            )
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", revenue, session['user_id'])
            flash(
                f"Successfully sold {shares_to_sell} shares of {symbol} for {usd(revenue)}!", "success")
            return redirect("/")
        except Exception as e:
            return apology("Transaction failed Please try again", )
    else:
        return render_template("sell.html", stocks=stocks)


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    try:
        user = db.execute("SELECT cash FROM users WHERE id = ?", session['user_id'])[0]
        portfolio = db.execute(
            "SELECT symbol, SUM(shares) as shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING shares > 0",
            session['user_id']
        )

        total_value = user['cash']

        for stock in portfolio:
            quote_data = lookup(stock['symbol'])
            if quote_data:
                stock['name'] = quote_data['name']
                stock['price'] = quote_data['price']
                stock['total'] = stock['price'] * stock['shares']
                total_value += stock['total']
            else:
                stock['name'] = stock['symbol']
                stock['price'] = 0
                stock['total'] = 0

        return render_template("index.html", portfolio=portfolio, cash=user['cash'], total=total_value)
    except Exception as e:
        return apology("Error loading portfolio", 400)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC",
        session['user_id']
    )
    return render_template("history.html", transactions=transactions)


if __name__ == "__main__":
    app.run(debug=True)
