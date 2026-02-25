import yfinance as yf
from concurrent.futures import ThreadPoolExecutor

class Index:
    """Represent a single market index with convenience data accessors.

    This class wraps a `yfinance.Ticker` for an index symbol and provides
    convenience attributes and methods to access historical price data and
    recent news. Instances expose the following attributes:
    """

    def __init__(self, symbol: str, ticker=None, period: str = "1y", interval: str = "1d"):
        """Initialize an `Index`.

        Args:
            symbol (str): Ticker symbol for the index.
            ticker (yfinance.Ticker): A constructed yfinance Ticker for the symbol.
            period (str, optional): Lookback period for historical data. Defaults to "1y".
            interval (str, optional): Data sampling interval. Defaults to "1d".
            history_data (pandas.DataFrame, optional): Historical price data for the index. Defaults to None.
            news (list, optional): Recent news articles related to the index. Defaults to None.
        """
        self.symbol = symbol
        self.ticker = ticker if ticker else yf.Ticker(symbol)
        self.period = period
        self.interval = interval

    def _get_historical_data(self):
        """Fetch historical price data for this index.

        Returns:
            pandas.DataFrame: Historical price data for the index.
        """
        return self.ticker.history(period=self.period, interval=self.interval)

    def _get_news(self, count: int = 5, tab: str = "news"):
        """Fetch recent news articles related to this index.
        
        Args:
            count (int, optional): Maximum number of news articles to fetch. Defaults to 5.
            tab (str, optional): The news tab to fetch from yfinance. Defaults to "news". Options include "news", "press_releases", "all".
        Returns:
            list: A list of news articles, each represented as a dictionary.
        """
        return self.ticker.get_news(count=count, tab=tab)
    
    def _get_info(self):
        """Fetch general information about the index.

        Returns:
            dict: A dictionary containing general information about the index.
        """
        return self.ticker.get_info()
    

class Indices:
    """Manage a collection of `Index` objects for multiple symbols.

    The `Indices` container constructs `Index` instances for a provided list
    of ticker symbols and offers mapping-like access and iteration over the
    created `Index` objects.
    """

    def __init__(self, symbols: list, period: str = "1y", interval: str = "1d"):
        """Create an `Indices` container from a list of ticker symbols.

        Args:
            symbols (list): Iterable of ticker symbol strings to create indices for.
            period (str, optional): Default lookback period for historical data. Defaults to "1y".
            interval (str, optional): Default sampling interval for historical data. Defaults to "1d".
        """
        self.symbols = symbols
        self.tickers = yf.Tickers(symbols)
        self.period = period
        self.interval = interval
        self.indices = self._create_indices()
    
    def _create_indices(self):
        """Create `Index` instances concurrently for all symbols.

        Uses a ThreadPoolExecutor to construct `Index` objects in parallel.

        Returns:
            dict: Mapping from symbol string to `Index` instance.
        """
        indices_dict = {}
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                symbol: executor.submit(Index, symbol, self.tickers.tickers[symbol], period=self.period, interval=self.interval)
                for symbol in self.symbols
            }
            for symbol, future in futures.items():
                indices_dict[symbol] = future.result()
        return indices_dict
    
    def __getitem__(self, symbol: str):
        """Return the `Index` instance for the given symbol.

        Args:
            symbol (str): The ticker symbol to look up.

        Returns:
            Index: The corresponding `Index` object.
        """
        return self.indices[symbol]
    
    def __iter__(self):
        """Iterate over all `Index` instances in this container.

        Yields:
            Iterator[Index]: Iterator over `Index` objects.
        """
        return iter(self.indices.values())


if __name__ == "__main__":
    # Initialize Indices with a list of popular index symbols
    indices = Indices(["^GSPC", "^DJI", "^IXIC", "^RUT", "^FTSE", "^N225", "^HSI"], period="2y", interval="1d")
    print(indices["^GSPC"]._get_news())