import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template
import schedule
import time
from threading import Thread
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('ticker.log')
    ]
)
logger = logging.getLogger(__name__)

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
last_update_time = None

def fetch_price(ticker):
    url = f"https://www.google.com/finance/quote/{ticker}:NSE"
    try:
        response = requests.get(url, timeout=10)  # Add timeout
        response.raise_for_status()  # Raise exception for bad status codes
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Define the class names for prices
        class1 = "YMlKec fxKbKc"  # Current price
        class2 = "P6K39c"         # Previous close

        try:
            current_price_text = soup.find(class_=class1).text
            current_price = float(current_price_text.replace(',', '').replace('₹', '').strip())
        except (AttributeError, ValueError) as e:
            logger.error(f"Error parsing current price for {ticker}: {str(e)}")
            current_price = None
            
        try:
            previous_close_text = soup.find(class_=class2).text
            previous_close = float(previous_close_text.replace(',', '').replace('₹', '').strip())
        except (AttributeError, ValueError) as e:
            logger.error(f"Error parsing previous close for {ticker}: {str(e)}")
            previous_close = None
        
        price_change = None
        percentage_change = None

        if current_price is not None and previous_close is not None:
            price_change = current_price - previous_close
            percentage_change = (price_change / previous_close) * 100 if previous_close != 0 else 0

        # Format price_change and percentage_change to 2 decimal places
        price_change_formatted = f"{price_change:.2f}" if price_change is not None else "N/A"
        percentage_change_formatted = f"{percentage_change:.2f}" if percentage_change is not None else "N/A"
        
        return {
            'ticker': ticker,
            'current_price': current_price,
            'previous_close': previous_close,
            'price_change': price_change_formatted,
            'percentage_change': percentage_change_formatted,
            'error': None
        }

    except requests.RequestException as e:
        logger.error(f"Error fetching data for {ticker}: {str(e)}")
        return {
            'ticker': ticker,
            'current_price': None,
            'previous_close': None,
            'price_change': "N/A",
            'percentage_change': "N/A",
            'error': str(e)
        }

def update_data():
    global ticker_data, last_update_time
    logger.info("Starting data update...")
    
    for ticker in nifty_50_tickers:
        result = fetch_price(ticker)
        ticker_data[ticker] = result
    
    last_update_time = datetime.now()
    logger.info("Data update completed")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ticker', methods=['GET'])
def get_ticker_data():
    global last_update_time
    logger.info(f"API request received. Data count: {len(ticker_data)}")
    return jsonify({
        'data': ticker_data,
        'last_update': last_update_time.isoformat() if last_update_time else None
    })

@app.route('/test')
def test():
    return jsonify({'message': 'Test endpoint working', 'data_count': len(ticker_data)})

def schedule_updates():
    schedule.every(5).minutes.do(update_data)  # Update every 5 minutes
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Initialize the data on start
    logger.info("Starting application...")
    update_data()
    
    # Start the Flask app in a separate thread
    Thread(target=lambda: app.run(host='0.0.0.0', port=5000), daemon=True).start()
    logger.info("Flask application started")
    
    # Start the scheduler
    schedule_updates()
