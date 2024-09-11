from dhanhq import dhanhq, marketfeed
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template
import asyncio
import threading
import time

# Replace with your actual client ID and access token
client_id = "1101930723"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI3NDExNTgxLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMTkzMDcyMyJ9.rIuLCmSr1B5SXa157b5wkMwzL0686RWCo-E0N6Wb-idQv0a_p7OIhAsoiIYSdsmO4F9gU8mYhcMKSy6EnHJNjg"

# Create an instance of the DhanAPI
dhan = dhanhq(client_id, access_token)

# List of tickers to fetch data for
tickers = [   "ABB",
    "ADANIENSOL",
    "ADANIENT",
    "ADANIGREEN",
    "ADANIPORTS",
    "ADANIPOWER",
    "ATGL",
    "AMBUJACEM",
    "APOLLOHOSP",
    "ASIANPAINT",
    "DMART",
    "AXISBANK",
    "BAJAJ-AUTO",
    "BAJFINANCE",
    "BAJAJFINSV",
    "BAJAJHLDNG",
    "BANKBARODA",
    "BERGEPAINT",
    "BEL",
    "BPCL",
    "BHARTIARTL",
    "BOSCHLTD",
    "BRITANNIA",
    "CANBK",

    "CIPLA",
    "COALINDIA",
    "COLPAL",
    "DLF",
    "DABUR",
    "DIVISLAB",
    "DRREDDY",
    "EICHERMOT",
    "GAIL",
    "GODREJCP",
    "GRASIM",
    "HCLTECH",
    "HDFCBANK",
    "HDFCLIFE",
    "HAVELLS",
    "HEROMOTOCO",
    "HINDALCO",
    "HAL",
    "HINDUNILVR",
    "ICICIBANK",
    "ICICIGI",
    "ICICIPRULI",
    "ITC",
    "IOC",
    "IRCTC",
    "IRFC",
    "INDUSINDBK",
    "NAUKRI",
    "INFY",
    "INDIGO",
    "JSWSTEEL",
    "JINDALSTEL",
    "JIOFIN",
    "KOTAKBANK",
    "LTIM",
    "LT",
    "LICI",
    "M&M",
    "MARICO",
    "MARUTI",
    "NTPC",
    "NESTLEIND",
    "ONGC",
    "PIDILITIND",
    "PFC",
    "POWERGRID",
    "PNB",
    "RECLTD",
    "RELIANCE",
    "SBICARD",
    "SBILIFE",
    "SRF",
    "MOTHERSON",
    "SHREECEM",
    "SHRIRAMFIN",
    "SIEMENS",
    "SBIN",
    "SUNPHARMA",
    "TVSMOTOR",
    "TCS",
    "TATACONSUM",
 
    "TATAMOTORS",
    "TATAPOWER",
    "TATASTEEL",
    "TECHM",
    "TITAN",
    "TORNTPHARM",
    "TRENT",
    "ULTRACEMCO",
    "UNITDSPR",
    "VBL",
    "VEDL",
    "WIPRO",
    "ZOMATO",
    "ZYDUSLIFE"]

# Split tickers into batches
batch_size = 8
batches = [tickers[i:i + batch_size] for i in range(0, len(tickers), batch_size)]

# Initialize a dictionary to store results
results = {}

# Calculate the date range for the previous day
today = datetime.now()
daybtm = today - timedelta(days=1)
yesterday = today 
from_date = daybtm.strftime('%Y-%m-%d')
to_date = yesterday.strftime('%Y-%m-%d')

def fetch_close_prices():
    for batch in batches:
        for ticker in batch:
            try:
                # Fetch the historical minute charts data
                historical_daily_data = dhan.historical_minute_charts(
                    symbol=ticker,
                    exchange_segment='NSE_EQ',
                    instrument_type='EQUITY',
                    expiry_code=0,
                    from_date=from_date,
                    to_date=to_date
                )
                
                # Check if the 'data' key exists and is not empty
                if 'data' in historical_daily_data and historical_daily_data['data']:
                    # Convert the data to a pandas DataFrame
                    historical_df = pd.DataFrame(historical_daily_data['data'])

                    # Extract only the 'close' column if it exists
                    if 'close' in historical_df.columns:
                        close_price = historical_df['close'].iloc[-1]  # Get the last close price
                        results[ticker] = close_price
                    else:
                        results[ticker] = None
                        print(f"The 'close' column is not present in the DataFrame for {ticker}.")
                else:
                    results[ticker] = None
                    print(f"No data found in the API response for {ticker}.")
                    
            except Exception as e:
                results[ticker] = None
                print(f"An error occurred for {ticker}: {e}")

        # Delay to respect rate limit
        time.sleep(1)

fetch_close_prices()

# Store last close prices in variables
previous_close_prices = {

    "13": results.get("ABB"),
    "10217": results.get("ADANIENSOL"),
    "25": results.get("ADANIENT"),
    "3563": results.get("ADANIGREEN"),
    "15083": results.get("ADANIPORTS"),
    "17388": results.get("ADANIPOWER"),
    "6066": results.get("ATGL"),
    "1270": results.get("AMBUJACEM"),
    "157": results.get("APOLLOHOSP"),
    "236": results.get("ASIANPAINT"),
    "19913": results.get("DMART"),
    "5900": results.get("AXISBANK"),
    "16669": results.get("BAJAJ-AUTO"),
    "317": results.get("BAJFINANCE"),
    "16675": results.get("BAJAJFINSV"),
    "305": results.get("BAJAJHLDNG"),
    "4668": results.get("BANKBARODA"),
    "404": results.get("BERGEPAINT"),
    "383": results.get("BEL"),
    "526": results.get("BPCL"),
    "10604": results.get("BHARTIARTL"),
    "2181": results.get("BOSCHLTD"),
    "547": results.get("BRITANNIA"),
    "10794": results.get("CANBK"),

    "694": results.get("CIPLA"),
    "20374": results.get("COALINDIA"),
    "15141": results.get("COLPAL"),
    "14732": results.get("DLF"),
    "772": results.get("DABUR"),
    "10940": results.get("DIVISLAB"),
    "881": results.get("DRREDDY"),
    "910": results.get("EICHERMOT"),
    "4717": results.get("GAIL"),
    "10099": results.get("GODREJCP"),
    "1232": results.get("GRASIM"),
    "7229": results.get("HCLTECH"),
    "1333": results.get("HDFCBANK"),
    "467": results.get("HDFCLIFE"),
    "9819": results.get("HAVELLS"),
    "1348": results.get("HEROMOTOCO"),
    "1363": results.get("HINDALCO"),
    "2303": results.get("HAL"),
    "1394": results.get("HINDUNILVR"),
    "4963": results.get("ICICIBANK"),
    "21770": results.get("ICICIGI"),
    "18652": results.get("ICICIPRULI"),
    "1660": results.get("ITC"),
    "1624": results.get("IOC"),
    "13611": results.get("IRCTC"),
    "2029": results.get("IRFC"),
    "5258": results.get("INDUSINDBK"),
    "13751": results.get("NAUKRI"),
    "1594": results.get("INFY"),
    "11195": results.get("INDIGO"),
    "11723": results.get("JSWSTEEL"),
    "6733": results.get("JINDALSTEL"),
    "18143": results.get("JIOFIN"),
    "1922": results.get("KOTAKBANK"),
    "17818": results.get("LTIM"),
    "11483": results.get("LT"),
    "9480": results.get("LICI"),
    "2031": results.get("M&M"),
    "4067": results.get("MARICO"),
    "10999": results.get("MARUTI"),
    "11630": results.get("NTPC"),
    "17963": results.get("NESTLEIND"),
    "2475": results.get("ONGC"),
    "2664": results.get("PIDILITIND"),
    "14299": results.get("PFC"),
    "14977": results.get("POWERGRID"),
    "10666": results.get("PNB"),
    "15355": results.get("RECLTD"),
    "2885": results.get("RELIANCE"),
    "17971": results.get("SBICARD"),
    "21808": results.get("SBILIFE"),
    "3273": results.get("SRF"),
    "4204": results.get("MOTHERSON"),
    "3103": results.get("SHREECEM"),
    "4306": results.get("SHRIRAMFIN"),
    "3150": results.get("SIEMENS"),
    "3045": results.get("SBIN"),
    "3351": results.get("SUNPHARMA"),
    "8479": results.get("TVSMOTOR"),
    "11536": results.get("TCS"),
    "3432": results.get("TATACONSUM"),

    "3456": results.get("TATAMOTORS"),
    "3426": results.get("TATAPOWER"),
    "3499": results.get("TATASTEEL"),
    "13538": results.get("TECHM"),
    "3506": results.get("TITAN"),
    "3518": results.get("TORNTPHARM"),
    "1964": results.get("TRENT"),
    "11532": results.get("ULTRACEMCO"),
    "10447": results.get("UNITDSPR"),
    "18921": results.get("VBL"),
    "3063": results.get("VEDL"),
    "3787": results.get("WIPRO"),
    "5097": results.get("ZOMATO"),
    "7929": results.get("ZYDUSLIFE")
}



# Mapping from security ID to ticker name
security_id_to_name = {
    
    "13": "ABB",
    "10217": "ADANIENSOL",
    "25": "ADANIENT",
    "3563": "ADANIGREEN",
    "15083": "ADANIPORTS",
    "17388": "ADANIPOWER",
    "6066": "ATGL",
    "1270": "AMBUJACEM",
    "157": "APOLLOHOSP",
    "236": "ASIANPAINT",
    "19913": "DMART",
    "5900": "AXISBANK",
    "16669": "BAJAJ-AUTO",
    "317": "BAJFINANCE",
    "16675": "BAJAJFINSV",
    "305": "BAJAJHLDNG",
    "4668": "BANKBARODA",
    "404": "BERGEPAINT",
    "383": "BEL",
    "526": "BPCL",
    "10604": "BHARTIARTL",
    "2181": "BOSCHLTD",
    "547": "BRITANNIA",
    "10794": "CANBK",

    "694": "CIPLA",
    "20374": "COALINDIA",
    "15141": "COLPAL",
    "14732": "DLF",
    "772": "DABUR",
    "10940": "DIVISLAB",
    "881": "DRREDDY",
    "910": "EICHERMOT",
    "4717": "GAIL",
    "10099": "GODREJCP",
    "1232": "GRASIM",
    "7229": "HCLTECH",
    "1333": "HDFCBANK",
    "467": "HDFCLIFE",
    "9819": "HAVELLS",
    "1348": "HEROMOTOCO",
    "1363": "HINDALCO",
    "2303": "HAL",
    "1394": "HINDUNILVR",
    "4963": "ICICIBANK",
    "21770": "ICICIGI",
    "18652": "ICICIPRULI",
    "1660": "ITC",
    "1624": "IOC",
    "13611": "IRCTC",
    "2029": "IRFC",
    "5258": "INDUSINDBK",
    "13751": "NAUKRI",
    "1594": "INFY",
    "11195": "INDIGO",
    "11723": "JSWSTEEL",
    "6733": "JINDALSTEL",
    "18143": "JIOFIN",
    "1922": "KOTAKBANK",
    "17818": "LTIM",
    "11483": "LT",
    "9480": "LICI",
    "2031": "M&M",
    "4067": "MARICO",
    "10999": "MARUTI",
    "11630": "NTPC",
    "17963": "NESTLEIND",
    "2475": "ONGC",
    "2664": "PIDILITIND",
    "14299": "PFC",
    "14977": "POWERGRID",
    "10666": "PNB",
    "15355": "RECLTD",
    "2885": "RELIANCE",
    "17971": "SBICARD",
    "21808": "SBILIFE",
    "3273": "SRF",
    "4204": "MOTHERSON",
    "3103": "SHREECEM",
    "4306": "SHRIRAMFIN",
    "3150": "SIEMENS",
    "3045": "SBIN",
    "3351": "SUNPHARMA",
    "8479": "TVSMOTOR",
    "11536": "TCS",
    "3432": "TATACONSUM",

    "3456": "TATAMOTORS",
    "3426": "TATAPOWER",
    "3499": "TATASTEEL",
    "13538": "TECHM",
    "3506": "TITAN",
    "3518": "TORNTPHARM",
    "1964": "TRENT",
    "11532": "ULTRACEMCO",
    "10447": "UNITDSPR",
    "18921": "VBL",
    "3063": "VEDL",
    "3787": "WIPRO",
    "5097": "ZOMATO",
    "7929": "ZYDUSLIFE"
}



app = Flask(__name__)

# Structure for subscribing is ("exchange_segment", "security_id")
instruments = [
    (1, "13"),        # ABB
    (1, "10217"),     # ADANIENSOL
    (1, "25"),        # ADANIENT
    (1, "3563"),      # ADANIGREEN
    (1, "15083"),     # ADANIPORTS
    (1, "17388"),     # ADANIPOWER
    (1, "6066"),      # ATGL
    (1, "1270"),      # AMBUJACEM
    (1, "157"),       # APOLLOHOSP
    (1, "236"),       # ASIANPAINT
    (1, "19913"),     # DMART
    (1, "5900"),      # AXISBANK
    (1, "16669"),     # BAJAJ-AUTO
    (1, "317"),       # BAJFINANCE
    (1, "16675"),     # BAJAJFINSV
    (1, "305"),       # BAJAJHLDNG
    (1, "4668"),      # BANKBARODA
    (1, "404"),       # BERGEPAINT
    (1, "383"),       # BEL
    (1, "526"),       # BPCL
    (1, "10604"),     # BHARTIARTL
    (1, "2181"),      # BOSCHLTD
    (1, "547"),       # BRITANNIA
    (1, "10794"),     # CANBK
  
    (1, "694"),       # CIPLA
    (1, "20374"),     # COALINDIA
    (1, "15141"),     # COLPAL
    (1, "14732"),     # DLF
    (1, "772"),       # DABUR
    (1, "10940"),     # DIVISLAB
    (1, "881"),       # DRREDDY
    (1, "910"),       # EICHERMOT
    (1, "4717"),      # GAIL
    (1, "10099"),     # GODREJCP
    (1, "1232"),      # GRASIM
    (1, "7229"),      # HCLTECH
    (1, "1333"),      # HDFCBANK
    (1, "467"),       # HDFCLIFE
    (1, "9819"),      # HAVELLS
    (1, "1348"),      # HEROMOTOCO
    (1, "1363"),      # HINDALCO
    (1, "2303"),      # HAL
    (1, "1394"),      # HINDUNILVR
    (1, "4963"),      # ICICIBANK
    (1, "21770"),     # ICICIGI
    (1, "18652"),     # ICICIPRULI
    (1, "1660"),      # ITC
    (1, "1624"),      # IOC
    (1, "13611"),     # IRCTC
    (1, "2029"),      # IRFC
    (1, "5258"),      # INDUSINDBK
    (1, "13751"),     # NAUKRI
    (1, "1594"),      # INFY
    (1, "11195"),     # INDIGO
    (1, "11723"),     # JSWSTEEL
    (1, "6733"),      # JINDALSTEL
    (1, "18143"),     # JIOFIN
    (1, "1922"),      # KOTAKBANK
    (1, "17818"),     # LTIM
    (1, "11483"),     # LT
    (1, "9480"),      # LICI
    (1, "2031"),      # M&M
    (1, "4067"),      # MARICO
    (1, "10999"),     # MARUTI
    (1, "11630"),     # NTPC
    (1, "17963"),     # NESTLEIND
    (1, "2475"),      # ONGC
    (1, "2664"),      # PIDILITIND
    (1, "14299"),     # PFC
    (1, "14977"),     # POWERGRID
    (1, "10666"),     # PNB
    (1, "15355"),     # RECLTD
    (1, "2885"),      # RELIANCE
    (1, "17971"),     # SBICARD
    (1, "21808"),     # SBILIFE
    (1, "3273"),      # SRF
    (1, "4204"),      # MOTHERSON
    (1, "3103"),      # SHREECEM
    (1, "4306"),      # SHRIRAMFIN
    (1, "3150"),      # SIEMENS
    (1, "3045"),      # SBIN
    (1, "3351"),      # SUNPHARMA
    (1, "8479"),      # TVSMOTOR
    (1, "11536"),     # TCS
    (1, "3432"),      # TATACONSUM
  
    (1, "3456"),      # TATAMOTORS
    (1, "3426"),      # TATAPOWER
    (1, "3499"),      # TATASTEEL
    (1, "13538"),     # TECHM
    (1, "3506"),      # TITAN
    (1, "3518"),      # TORNTPHARM
    (1, "1964"),      # TRENT
    (1, "11532"),     # ULTRACEMCO
    (1, "10447"),     # UNITDSPR
    (1, "18921"),     # VBL
    (1, "3063"),      # VEDL
    (1, "3787"),      # WIPRO
    (1, "5097"),      # ZOMATO
    (1, "7929")       # ZYDUSLIFE
]

# Type of data subscription
subscription_code = marketfeed.Ticker
import asyncio
import threading
from flask import Flask, render_template, jsonify
 # Ensure this is the correct import based on your actual library

app = Flask(__name__)

# Dictionary to store ticker data by security ID
ticker_data = {}

async def on_connect(instance):
    print("Connected to WebSocket")

async def on_message(instance, message):
    global ticker_data
    try:
        if message.get('type') == 'Ticker Data':
            security_id = str(message.get('security_id'))

            current_price_str = message.get('LTP')
            try:
                current_price = float(current_price_str)
            except ValueError:
                print(f"Error: Invalid current price '{current_price_str}' for Security ID {security_id}.")
                return

            previous_close_str = previous_close_prices.get(security_id)
            try:
                previous_close = float(previous_close_str) if previous_close_str is not None else None
            except ValueError:
                print(f"Error: Invalid previous close price '{previous_close_str}' for Security ID {security_id}.")
                return

            if previous_close is None:
                print(f"Error: No previous close price available for Security ID {security_id}.")
                return

            price_change = current_price - previous_close
            percentage_change = (price_change / previous_close) * 100 if previous_close != 0 else 0

            price_change = round(price_change, 2)
            percentage_change = round(percentage_change, 2)
            ticker_name = security_id_to_name.get(security_id, "Unknown Ticker")

            ticker_data[security_id] = {
                'name': ticker_name,
                'price': current_price,
                'time': message.get('LTT'),
                'price_change': price_change,
                'percentage_change': percentage_change
            }
    except Exception as e:
        print("Error processing message:", str(e))

async def start_feed(feed):
    try:
        await feed.connect()
        await feed.run_forever()
    except asyncio.CancelledError:
        print("Feed connection was cancelled.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # No need to call feed.close() if it doesn't exist
        print("Feed connection is closing.")

@app.route('/')
def index():
    return render_template('index.html', ticker_data=list(ticker_data.values()))

@app.route('/api/ticker', methods=['GET'])
def get_ticker_data():
    return jsonify(list(ticker_data.values()))

def run_flask_app():
    app.run(host='0.0.0.0', port=5000, use_reloader=False)

if __name__ == '__main__':
    # Start Flask app in a separate thread
    threading.Thread(target=run_flask_app, daemon=True).start()

    # Initialize the WebSocket feed
    feed = marketfeed.DhanFeed(
        client_id, access_token, instruments, subscription_code,
        on_connect=on_connect, on_message=on_message
    )

    # Run the WebSocket feed in an asyncio event loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_feed(feed))
    except KeyboardInterrupt:
        print("Script interrupted by user.")
    finally:
        print("Script is terminating.")
        loop.close()
