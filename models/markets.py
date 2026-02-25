import yfinance as yf
from concurrent.futures import ThreadPoolExecutor

class Market:
    """Represents a single market and its metadata fetched via yfinance.

    Wraps yfinance's `Market` object for a given market identifier and
    exposes commonly used attributes such as `status` and `summary`.

    Args:
        name: Market identifier accepted by yfinance (e.g., 'US', 'GB').
    """
    def __init__(self, name: str):
        self.name = name
        self.market = yf.Market(name)
        self.status = self.market.status
        self.summary = self.market.summary
    

class Markets:
    """Manages a collection of Market objects for multiple market identifiers.

    Fetches and stores multiple markets using parallel processing via
    `ThreadPoolExecutor` for improved performance. The `markets` attribute is
    a dictionary mapping market identifier to `Market` instances.

    Args:
        market_names: List of market identifier strings (e.g., ['US', 'GB']).
    """
    def __init__(self, market_names: list):
        self.market_names = market_names
        self.markets = self._create_markets()

    def _create_markets(self):
        """Create Market objects for all market names using parallel processing.
        
        Uses ThreadPoolExecutor to fetch market data concurrently with a maximum
        of 4 workers for improved performance.
        
        Returns:
            dict: Dictionary mapping market name to Market object
        """
        markets_dict = {}
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                name: executor.submit(Market, name)
                for name in self.market_names
            }
            for name, future in futures.items():
                markets_dict[name] = future.result()
        return markets_dict

    def __getitem__(self, name: str):
        """Get a Market object by market identifier.

        Args:
            name: Market identifier string (e.g., 'US')

        Returns:
            Market: The Market object for the given identifier

        Raises:
            KeyError: If the market identifier is not found in the collection
        """
        return self.markets[name]
    
    def __iter__(self):
        """Iterate over all Market objects in the collection.
        
        Returns:
            Iterator: Iterator over Market objects
        """
        return iter(self.markets.values())
    

if __name__ == "__main__":
    # Initialize Markets with all available market identifiers
    markets = Markets(["US", "GB", "ASIA", "EUROPE", "RATES", "COMMODITIES", "CURRENCIES", "CRYPTOCURRENCIES"])