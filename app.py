import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
from datetime import datetime

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    portfolio = []
    rows = db.execute("SELECT symbol, name, SUM(shares) as shares, AVG(price) as avg_price FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])
    
    for i in rows:
        q = lookup(i["symbol"])
        portfolio.append({"symbol": i["symbol"],
                          "name": i["name"],
                          "shares": i["shares"],
                          "avg_price": i["avg_price"], 
                          "current_price": q["price"], 
                          "value": q["price"] * i["shares"],                         
                          "pl": (q["price"] - i["avg_price"]) * i["shares"]})
    # return render_template("index.html", portfolio=portfolio)

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    total_assets = cash + sum(stock["value"] for stock in portfolio)
    return render_template("index.html", portfolio=portfolio, cash=cash, total_assets=total_assets)


@app.context_processor
def inject_cash():
    if session.get("user_id"):
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        return {"cash": cash}
    return {}

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # able to buy if the cash > price
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    # user entered data
    symbol = request.form.get("symbol")
    share = request.form.get("shares")
  

    if request.method == "GET":
        return render_template("buy.html")

    if request.method == "POST":
        # calling lookup as function, saves the whole data as dict:
        q = lookup(symbol)
        try:
            share = int(share)
        except ValueError:
            return apology("shares must be a number", 400)
        if q:
            price = q["price"]
            if symbol and price and share>0:
                if cash > 0 and price * share < cash:
                    # cash = cash - price * share
                    # return render_template("bought.html", cash=cash, name=q["name"], symbol=q["symbol"], price=q["price"] )
                    cash = cash - price * share
                    db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])
                    db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price) VALUES (?, ?, ?, ?, ?)",
                            session["user_id"], q["symbol"], q["name"], share, price)
                    return redirect("/")
                else:
                    return apology("Not Enough Cash", 400)

            else:
                return apology("need valid entry", 400)
            
        else:
            return apology("invalid symbol", 400)
    

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = []
    t = db.execute("select * from transactions where user_id = ? order by timestamp desc", session["user_id"])
    for i in t:
        history.append({"symbol": i["symbol"],
                        "name": i["name"],
                        "shares": i["shares"],
                        "price": i["price"],
                        "date": datetime.strptime(i["timestamp"], "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y %I:%M %p")})
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    
    # user entered symbol
    symbol = request.form.get("symbol")
    if not symbol:
        return apology("need stock symbol", 400)
    # retrieved from api symbol
    q = lookup(symbol)
    # above q: return a dict with all info on the symbol

    # is the user entered symbol dosent exist in the api:
    if q is None:
        return apology("invalid symbol", 400)
    
    # a["name"] accesses the value of the key name, since q is dict
    return render_template("quoted.html", name=q["name"], symbol=q["symbol"], price=q["price"])
# where do we ensure the user entered stock is in the database? like:
# if symbol == q, the proceed


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template("register.html")
    session.clear()

    username= request.form.get("username")
    password= request.form.get("password")
    confirmation= request.form.get("confirmation")

    if not username:
        return apology("Please provide username", 400)

    if not password:
        return apology("Please provide password", 400)

    if password != confirmation:
        return apology("Passwords don't match", 400)

    # to check if username already exists
    rows = db.execute("SELECT * FROM users WHERE username = ?", username)
    if len(rows) != 0:
        return apology("username already taken", 400)

    hash_pass=generate_password_hash(password)

    new_id = db.execute(
        "INSERT INTO users (username, hash) VALUES (?, ?)",
        username, hash_pass
    )
    session["user_id"] = new_id
    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    if request.method == "GET":
        stocks = db.execute("select symbol from transactions where user_id = ? group by symbol having sum(shares) > 0 ", session["user_id"])
        return render_template("sell.html", stocks=stocks)

    if request.method == "POST":
        shares = request.form.get("shares")
        symbol = request.form.get("symbol")
        # lookup gives - name, price, symbol
        q = lookup(symbol)
        try:
            shares = int(shares)
        except ValueError:
            return apology("Not Enough Shares to sell", 400)
        owned = db.execute("SELECT SUM(shares) as shares FROM transactions WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)[0]["shares"]

        if not q:
            return apology("invalid symbol", 400)
        if shares <= 0:
            return apology("enter at least 1 share to sell", 400)
        if shares > owned:
            return apology("you're trying to sell more shares than you owe", 400)
        
        
        # all checks passed, execute sale:
        cash = cash + q["price"] * shares
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], symbol, q["name"], -shares, q["price"])
        return redirect("/")   
        
