import requests
import yfinance as yf 

def get_ticker(company_name):
    """Fetches the stock ticker symbol for a given company name"""
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    params = {"q": company_name, "quotes_count": 1, "country": "United States"}

    try:
        res = requests.get(url=url, params=params, headers={'User-Agent': user_agent})
        res.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        data = res.json()

        # Check if 'quotes' is in the response and it has at least one result
        if 'quotes' in data and len(data['quotes']) > 0:
            company_code = data['quotes'][0]['symbol']
            return company_code
        else:
            return f"No results found for '{company_name}'. Please check the company name."

    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"
    
def get_stock_price(ticker):
    """Fetches the current stock price using Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        
        if data.empty:
            return f"Stock data not found for {ticker}."
        
        price = data["Close"].iloc[0]  # Today's closing price
        return {"Stock": ticker, "Price": price, "Source": "Yahoo Finance"}
    except Exception as e:
        return f"Error fetching stock data for {ticker}: {str(e)}"

def is_stock_query(query):
    """Check if query contains TWO stock-related terms"""
    query = query.lower()
    
    # Pairs of terms that indicate stock intent
    required_combos = [
        ("stock", "price"),
        ("share", "price"),
        ("market", "price"), 
        ("stock", "value"),
        ("ticker", "price"),
        ("stocks", "price"),("stock", "prices"),("stocks", "prices"),
        ("share", "prices"),("shares", "price"),("shares", "prices")
    ]
    
    # Check if ANY pair exists in the query
    return any(
        (word1 in query and word2 in query)
        for (word1, word2) in required_combos
    )


stopwords = {",",".","?","what", "is", "the","price","stock", "where", "why", "how", "of", "you", "tell", "me", "a", "to", "in", "on", "for", "by","today","current", "and", "at", "from", "can", "which", "when"}
# Function to process stock-related queries and return simplified stock data
def find_stock_price(query):
    """Processes the query to return simplified stock prices or general results."""
    words = query.lower().split()
    meaningful_words = [word for word in words if word not in stopwords]
    
    if not meaningful_words:
        return "no stock data available"
    
    stock_results = []
    
    for word in meaningful_words:
        ticker = get_ticker(word)
        if not ticker:
            continue
            
        stock_data = get_stock_price(ticker)
        
        # Handle cases where get_stock_price() returns an error string
        if isinstance(stock_data, str):
            print(f"Error for {ticker}: {stock_data}")  # Log the error
            continue
            
        # Ensure stock_data has the expected structure
        if isinstance(stock_data, dict) and 'Price' in stock_data:
            stock_results.append({
                "name": word,
                "symbol": ticker,
                "price": stock_data['Price'],
                "source": "Yahoo Finance"
            })
    
    return stock_results if stock_results else "no stock data available"