import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template
import schedule
import time
from threading import Thread

# List of Nifty 50 tickers
nifty_50_tickers = [
    "ADANIENT", "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO",
    "BAJFINANCE", "BAJAJFINSV", "BPCL", "BHARTIARTL", "BRITANNIA", "CIPLA",
    "COALINDIA", "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM", "HCLTECH",
    "HDFCBANK", "HDFCLIFE", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK",
    "ITC", "INDUSINDBK", "INFY", "JSWSTEEL", "KOTAKBANK", "LTIM", "LT", "M&M",
    "MARUTI", "NTPC", "NESTLEIND", "ONGC", "POWERGRID", "RELIANCE", "SBILIFE",
    "SHRIRAMFIN", "SBIN", "SUNPHARMA", "TCS", "TATACONSUM", "TATAMOTORS", "TATASTEEL",
    "TECHM", "TITAN", "ULTRACEMCO", "WIPRO"
]

# Flask application setup
app = Flask(__name__)

# Dictionary to store the ticker data
ticker_data = {}

def fetch_price(ticker):
    url = f"https://www.google.com/finance/quote/{ticker}:NSE"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Define the class names for prices (These need to be verified)
    class1 = "YMlKec fxKbKc"  # Example class for the current price
    class2 = "P6K39c"         # Example class for the previous close

    try:
        current_price_text = soup.find(class_=class1).text
        current_price = float(current_price_text.replace(',', '').replace('₹', '').strip())
    except (AttributeError, ValueError):
        current_price = None
        
    try:
        previous_close_text = soup.find(class_=class2).text
        previous_close = float(previous_close_text.replace(',', '').replace('₹', '').strip())
    except (AttributeError, ValueError):
        previous_close = None
    
    price_change = None
    percentage_change = None

    if current_price is not None and previous_close is not None:
        price_change = current_price - previous_close
        percentage_change = (price_change / previous_close) * 100 if previous_close != 0 else 0

    # Format price_change and percentage_change to 2 decimal places
    price_change_formatted = f"{price_change:.2f}" if price_change is not None else "Not available"
    percentage_change_formatted = f"{percentage_change:.2f}" if percentage_change is not None else "Not available"
    
    return ticker, current_price, previous_close, price_change_formatted, percentage_change_formatted

def update_data():
    global ticker_data
    for ticker in nifty_50_tickers:
        ticker, current_price, previous_close, price_change, percentage_change = fetch_price(ticker)
        ticker_data[ticker] = {
            'current_price': current_price,
            'previous_close': previous_close,
            'price_change': price_change,
            'percentage_change': percentage_change
        }
    print("Data updated.")

@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

@app.route('/api/ticker', methods=['GET'])
def get_ticker_data():
    return jsonify(ticker_data)

def schedule_updates():
    schedule.every(5).minutes.do(update_data)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Initialize the data on start
    update_data()
    
    # Start the Flask app in a separate thread
    Thread(target=lambda: app.run(host='0.0.0.0', port=5000), daemon=True).start()
    
    # Start the scheduler
    schedule_updates()