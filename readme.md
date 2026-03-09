# 📈 TradeX — Stock Trading Simulator

**Video Demo:** _coming soon_

**Author:** Aselle Cunningham

---

## 🎯 Overview

TradeX is a stock trading web application simulates a real brokerage experience — users start with $10,000 in virtual cash and can look up real stock prices, buy and sell shares, track their portfolio performance, and review their full transaction history.

Stock price data is pulled in real time from the CS50 finance API, which sources live US market data.

---
**Demo account:**
- Username: `aselle123`
- Password: `aselle123`

## 🧭 App Flow

1. User registers and receives $10,000 in virtual cash
2. Looks up a stock quote
3. Buys shares
4. Monitors portfolio with live P&L
5. Sells shares when ready
6. Reviews full transaction history

---

## ✨ Features

### 👤 User Accounts
- Register and log in with username and password
- Passwords stored securely using hashed values
- Sessions managed with Flask-Session

### 💵 Cash Display
- Available cash balance visible in the navbar on every page
- Updates in real time after every buy or sell

### 🔍 Stock Quote Lookup
- Look up any valid US stock ticker
- Displays company name, symbol, and current price
- Quick "Buy" button to jump directly to purchase flow
- ETF tickers (SPY, QQQ, etc.) are not supported by the API

### 🛒 Buy Stocks
- Search by ticker symbol
- Enter number of shares
- Validates symbol, share count, and available cash
- Deducts cost from cash balance and records the transaction

### 💸 Sell Stocks
- Dropdown menu pre-populated with only stocks the user owns
- Enter number of shares to sell
- Validates against owned shares to prevent overselling
- Adds proceeds to cash balance and records the transaction

### 📊 Portfolio with P&L
- Table showing all currently owned stocks
- Columns: Symbol, Name, Shares, Avg Buy Price, Current Price, Current Value, P&L
- P&L displayed in green (profit) or red (loss)
- Bottom summary showing Cash, Invested, and Total Assets

### 📋 Transaction History
- Full log of every buy and sell ever made
- Buy/Sell action shown in green/red
- Includes symbol, name, shares, price, and formatted timestamp

### 🚨 Custom Error Pages
- Custom apology image for all error states (invalid symbol, insufficient funds, etc.)

---

## 🛠️ Technologies Used

| Tool | Purpose |
|------|---------|
| Python / Flask | Web framework |
| SQLite | Database |
| Flask-Session | User sessions |
| Werkzeug | Password hashing |
| CS50 SQL library | Simplified database access |
| Bootstrap 5 | UI components and layout |
| Custom CSS | Typography and styling |
| CS50 Finance API | Real-time stock price data |
| Gunicorn | Production server |
| Render | Hosting |

---

## 🗄️ Database Design

### `users`
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| username | TEXT UNIQUE NOT NULL |
| hash | TEXT NOT NULL |
| cash | NUMERIC DEFAULT 10000.00 |

### `transactions`
| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY |
| user_id | INTEGER NOT NULL |
| symbol | TEXT NOT NULL |
| name | TEXT NOT NULL |
| shares | INTEGER NOT NULL |
| price | NUMERIC NOT NULL |
| timestamp | DATETIME DEFAULT CURRENT_TIMESTAMP |

Sell transactions are recorded with **negative shares**, allowing the history and portfolio to derive bought vs. sold from a single table.

---

## 🚀 Deployment

The app is deployed on Render, connected to this GitHub repository.

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Live URL:** `https://tradex-ewhz.onrender.com`

---

## 📌 How to Run Locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run --debug
```

App runs at: `http://127.0.0.1:5000`

---

## 🤖 AI Assistance Acknowledgment

Per CS50 policy: I used AI tools as helpers while building this project — mainly for debugging Flask and SQL issues, improving UI/UX decisions, and learning best practices. All final logic, structure, and implementation decisions were my own.

---

## 🔮 Future Improvements

- Display stock charts for owned holdings
- Add ability to deposit more virtual cash
- Custom portfolio themes
- Price alerts
- Leaderboard comparing portfolio performance across users