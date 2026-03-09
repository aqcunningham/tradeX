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

<img width="1709" height="772" alt="Screenshot 2026-03-08 at 9 43 21 PM" src="https://github.com/user-attachments/assets/2b24592a-6146-47ce-8d74-492d06b1f145" />
<img width="1708" height="672" alt="Screenshot 2026-03-08 at 9 44 03 PM" src="https://github.com/user-attachments/assets/be61d1e4-11f5-42e0-a40e-0758938e1c85" />
<img width="1709" height="669" alt="Screenshot 2026-03-08 at 9 44 59 PM" src="https://github.com/user-attachments/assets/23a72bef-83a1-4534-b914-10646f74de62" />
<img width="1707" height="750" alt="Screenshot 2026-03-08 at 9 45 35 PM" src="https://github.com/user-attachments/assets/d291ca9e-2e54-4edf-bb67-c82e14f94244" />
<img width="1707" height="799" alt="Screenshot 2026-03-08 at 9 45 52 PM" src="https://github.com/user-attachments/assets/6ac846b4-9e8f-4796-a77e-63c86351a525" />
<img width="1707" height="748" alt="Screenshot 2026-03-08 at 9 46 11 PM" src="https://github.com/user-attachments/assets/a0d580ec-e785-44de-a725-7a8c4d9e458f" />
<img width="1705" height="697" alt="Screenshot 2026-03-08 at 9 46 33 PM" src="https://github.com/user-attachments/assets/7cc7c32b-f479-4d36-bf18-f86d3801d85a" />
<img width="1705" height="758" alt="Screenshot 2026-03-08 at 9 47 09 PM" src="https://github.com/user-attachments/assets/f01d11b4-329b-4900-9b2c-552481a6ba20" />
<img width="1705" height="815" alt="Screenshot 2026-03-08 at 9 47 33 PM" src="https://github.com/user-attachments/assets/c8d4f7f8-ab81-4843-a1e7-c99915e505d1" />
<img width="1705" height="973" alt="Screenshot 2026-03-08 at 9 48 05 PM" src="https://github.com/user-attachments/assets/26e93f67-d2ea-4ec9-a6e6-f7b97640e2fe" />
<img width="1704" height="947" alt="Screenshot 2026-03-08 at 9 48 22 PM" src="https://github.com/user-attachments/assets/f456bf4b-bd83-4420-b229-83e229d06ebc" />


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
