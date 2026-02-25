import yfinance as yf
from concurrent.futures import ThreadPoolExecutor


class Stock:
    """Represents a single stock with its financial data and metrics.
    
    Fetches and stores stock information including type, ISIN, historic price data,
    and dividend yield from yfinance.
    """
    def __init__(self, symbol: str, ticker, period: str = "1y", interval: str = "1d"):
        """Initialize a Stock instance with financial data.
        
        Fetches stock type, ISIN, historical price data, and dividend yield
        from yfinance.
        
        Args:
            symbol (str): Ticker symbol for the stock (e.g., 'AAPL')
            ticker: yfinance Ticker object for the symbol
            period (str, optional): Time period for historical data. Defaults to "1y"
            interval (str, optional): Data interval granularity. Defaults to "1d" (daily)
        """
        self.symbol = symbol
        self.ticker = ticker
        self.period = period
        self.interval = interval
    
    def _get_isin(self):
        """Get the ISIN (International Securities Identification Number).
        
        Returns:
            str: ISIN code or None if not available
        """
        return self.ticker.get_isin() if hasattr(self.ticker, "isin") else None
    
    def _get_historical_data(self):
        """Fetch historic price and dividend data for the specified period.
        
        Returns:
            pd.DataFrame: DataFrame with OHLCV and dividend data
        """
        return self.ticker.history(period=self.period, interval=self.interval)
    
    def _get_historical_metadata(self):
        """Fetch metadata about the historical data, such as start and end dates.
        
        Returns:
            dict: Metadata about the historical data
        """
        return self.ticker.get_history_metadata()
    
    def _get_dividends(self):
        """Fetch dividend data for the stock.
        
        Returns:
            pd.Series: Series with dividend amounts and dates
        """
        return self.ticker.get_dividends(period='max')
    
    def _get_splits(self):
        """Fetch stock split data for the stock.
        
        Returns:
            pd.Series: Series with split ratios and dates
        """
        return self.ticker.get_splits(period='max')
    
    def _get_actions(self):
        """Fetch corporate action data for the stock.
        
        Returns:
            pd.DataFrame: DataFrame with corporate actions and dates
        """
        return self.ticker.get_actions(period='max')
    
    def _get_capital_gains(self):
        """Fetch capital gain data for the stock.
        
        Returns:
            pd.DataFrame: DataFrame with capital gains and dates
        """
        return self.ticker.get_capital_gains(period='max')
    
    def _get_info(self):
        """Fetch general information about the stock.
        
        Returns:
            dict: A dictionary containing general information about the stock
        """
        return self.ticker.info
    
    def _get_fast_info(self):
        """Fetch fast information about the stock, such as current price and volume.
        
        Returns:
            dict: A dictionary containing fast information about the stock
        """
        return self.ticker.fast_info
    
    def _get_news(self, count: int = 5, tab: str = "news"):
        """Fetch recent news articles related to this index.
        
        Args:
            count (int, optional): Maximum number of news articles to fetch. Defaults to 5.
            tab (str, optional): The news tab to fetch from yfinance. Defaults to "news". Options include "news", "press_releases", "all".
        Returns:
            list: A list of news articles, each represented as a dictionary.
        """
        return self.ticker.get_news(count=count, tab=tab)

class Stocks:
    """Manages a collection of Stock objects for multiple ticker symbols.
    
    Fetches and stores multiple stocks using parallel processing via ThreadPoolExecutor
    for improved performance. Provides dictionary-like access to individual stocks
    and iteration over all stocks in the collection.
    """
    def __init__(self, symbols: list, period: str = "1y", interval: str = "1d"):
        """Initialize a Stocks collection from a list of ticker symbols.
        
        Fetches Stock objects for all symbols using parallel processing to improve
        performance. Creates yfinance Tickers instance for bulk data retrieval.
        
        Args:
            symbols (list): List of stock ticker symbols (e.g., ['AAPL', 'MSFT', 'GOOGL'])
            period (str, optional): Time period for historical data. Defaults to "1y"
            interval (str, optional): Data interval granularity. Defaults to "1d" (daily)
        """
        self.symbols = symbols
        self.period = period
        self.interval = interval
        self.tickers = yf.Tickers(symbols)
        self.stocks = self._create_stocks()
    
    def _create_stocks(self):
        """Create Stock objects for all symbols using parallel processing.
        
        Uses ThreadPoolExecutor to fetch stock data concurrently with a maximum
        of 4 workers for improved performance.
        
        Returns:
            dict: Dictionary mapping symbol to Stock object
        """
        stocks_dict = {}
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                symbol: executor.submit(Stock, symbol, self.tickers.tickers[symbol], self.period, self.interval)
                for symbol in self.symbols
            }
            for symbol, future in futures.items():
                stocks_dict[symbol] = future.result()
        return stocks_dict
    
    def __getitem__(self, symbol):
        """Get a Stock object by ticker symbol.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL')
            
        Returns:
            Stock: The Stock object for the given symbol
            
        Raises:
            KeyError: If the symbol is not in the collection
        """
        return self.stocks[symbol]
    
    def __iter__(self):
        """Iterate over all Stock objects in the collection.
        
        Returns:
            Iterator: Iterator over Stock objects
        """
        return iter(self.stocks.values())
    
    def __len__(self):
        """Return the number of stocks in the collection.
        
        Returns:
            int: Number of Stock objects in this Stocks collection
        """
        return len(self.stocks)


if __name__ == "__main__":
    stocks = Stocks(["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "VOO", "SPY", "QYLD", "SYLD.L"], period="2y", interval="1d")