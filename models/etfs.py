import yfinance as yf
from concurrent.futures import ThreadPoolExecutor
from yfinance_api.models.stocks import Stock


class ETF(Stock):
    """Represents an Exchange-Traded Fund (ETF) with ETF-specific metadata.

    Inherits all attributes and behaviour from `Stock` and extends it with
    ETF-relevant fields like TER (expense ratio), replication type, AUM,
    and fund family/manager when available from yfinance.
    """

    def __init__(self, symbol, ticker, period="1y", interval="1d"):
        """Initialize an ETF instance and populate ETF-specific attributes.

        Args:
            symbol (str): ETF ticker symbol (e.g., 'VOO')
            ticker: yfinance Ticker instance for the symbol
            period (str): Lookback period for historical data
            interval (str): Sampling interval for historical data
        """
        super().__init__(symbol, ticker, period, interval)
        # ETF-specific attributes (may be None if not present in ticker.info)
        # TODO: ADD ETF-specific fields like TER, replication type, AUM, fund family/manager


class ETFs:
    """Manages a collection of `ETF` objects for multiple ticker symbols.

    This container fetches ETF data in bulk using `yf.Tickers` and constructs
    `ETF` objects concurrently. Instances are accessible like a mapping via
    `__getitem__` and iterable over ETF objects.
    """

    def __init__(self, symbols: list, period: str = "1y", interval: str = "1d"):
        """Create an `ETFs` container from a list of ticker symbols.

        Args:
            symbols (list): List of ETF ticker symbols (e.g., ['VOO', 'SPY'])
            period (str, optional): Lookback period for historical data. Defaults to "1y".
            interval (str, optional): Data sampling interval. Defaults to "1d".
        """
        self.symbols = symbols
        self.period = period
        self.interval = interval
        self.tickers = yf.Tickers(symbols)
        self.etfs = self._create_etfs()

    def _create_etfs(self):
        """Create `ETF` instances concurrently for all symbols.

        Returns:
            dict: Mapping from symbol to `ETF` instance
        """
        etf_dict = {}
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                symbol: executor.submit(
                    ETF,
                    symbol,
                    self.tickers.tickers[symbol],
                    self.period,
                    self.interval,
                )
                for symbol in self.symbols
            }
            for symbol, future in futures.items():
                etf_dict[symbol] = future.result()
        return etf_dict

    def __getitem__(self, symbol):
        """Return the `ETF` instance for the given symbol."""
        return self.etfs[symbol]

    def __iter__(self):
        """Iterate over all `ETF` instances in this container."""
        return iter(self.etfs.values())
    
    def __len__(self):
        """Return the number of ETFs in this container."""
        return len(self.etfs)


if __name__ == "__main__":
    etfs = ETFs(["VOO", "SPY", "QYLD", "SYLD.L"], period="2y", interval="1d")
    print(etfs["QYLD"]._get_dividends())