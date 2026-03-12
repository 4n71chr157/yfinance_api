from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from enum import Enum

from helper import serialize
from models.markets import Markets
from models.indices import Indices


class MarketEnum(str, Enum):
	"""Allowed market identifiers."""
	US = "US"
	GB = "GB"
	ASIA = "ASIA"
	EUROPE = "EUROPE"
	RATES = "RATES"
	COMMODITIES = "COMMODITIES"
	CURRENCIES = "CURRENCIES"
	CRYPTOCURRENCIES = "CRYPTOCURRENCIES"


app = FastAPI(title="Yfinance API")
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """
    Root endpoint redirecting to API documentation.
    """
    return RedirectResponse(url="/docs")


@app.get("/markets", tags=["Market"], summary="List Available Markets")
def get_markets() -> dict:
	"""
	Retrieve all available market identifiers.

	Returns:
	- List of all supported markets
	"""
	return {
		"markets": [market.value for market in MarketEnum]
	}


@app.get("/markets/status/{markets}", tags=["Market"], summary="Get Status for single or multiple Markets")
def get_markets_status(markets: str = None) -> dict:
	"""
	Retrieve status information for markets.

	This endpoint supports both a path and a query form:

	- Path: `/markets/status/{markets}` where `{markets}` is a single symbol, a comma-separated list, or `all`.
	  Examples: `/markets/status/US`, `/markets/status/US,GB`, `/markets/status/all`
	- Query: `/markets/status?markets=US,GB` (the `markets` query parameter behaves the same)

	Parameters:
	- **markets** (path or query, optional): Comma-separated market identifiers (e.g., US,GB,ASIA). Use `all` or omit to request all markets.

	Returns:
	- A mapping of market identifier to its `status` data.

	Examples:
	- `/markets/status/US` - status for the US market
	- `/markets/status/US,GB` - status for US and GB
	- `/markets/status` or `/markets/status/all` - status for all supported markets
	"""
	if not markets or markets.strip().lower() == "all":
		market_list = [m.value for m in MarketEnum]
	else:
		market_list = [m.strip().upper() for m in markets.split(",") if m.strip()]
	try:
		markets = Markets(market_list)
		results = {market.name: serialize(getattr(market, "status", None)) for market in markets}
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
	return {"markets": results}


@app.get("/markets/summary/{markets}", tags=["Market"], summary="Get Summary for single or multiple Markets")
def get_markets_summary(markets: str = None) -> dict:
	"""
	Retrieve summary information for markets.

	This endpoint supports both a path and a query form:

	- Path: `/markets/summary/{markets}` where `{markets}` is a single symbol, a comma-separated list, or `all`.
	  Examples: `/markets/summary/US`, `/markets/summary/US,GB`, `/markets/summary/all`
	- Query: `/markets/summary?markets=US,GB` (the `markets` query parameter behaves the same)

	Parameters:
	- **markets** (path or query, optional): Comma-separated market identifiers (e.g., US,GB,ASIA). Use `all` or omit to request all markets.

	Returns:
	- A mapping of market identifier to its `summary` data.

	Examples:
	- `/markets/summary/US` - summary for the US market
	- `/markets/summary/US,GB` - summary for US and GB
	- `/markets/summary` or `/markets/summary/all` - summary for all supported markets
	"""
	if not markets or markets.strip().lower() == "all":
		market_list = [m.value for m in MarketEnum]
	else:
		market_list = [m.strip().upper() for m in markets.split(",") if m.strip()]
	try:
		markets = Markets(market_list)
		results = {market.name: serialize(getattr(market, "summary", None)) for market in markets}
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
	return {"markets": results}


@app.get("/indices/news/{indices}", tags=["Index"], summary="Get News for single or multiple Indices")
def get_index_news(indices: str, count: int = 10, tab: str = "news") -> dict:
	"""
	Retrieve recent news articles related to financial indices.

	Fetches raw news data from Yahoo Finance for any index symbol.

	This endpoint supports both a path and a query form:

	- Path: `/indices/news/{indices}` where `{indices}` is a single symbol or a comma-separated list of symbols.
	  Examples: `/indices/news/^GSPC`, `/indices/news/^GSPC,^IXIC`
	- Query: `/indices/news?indices=^GSPC,^IXIC` (the `indices` query parameter behaves the same)

	Parameters:
	- **indices** (required): Yahoo Finance symbol for the index, or a comma-separated list of symbols
	  - Example: `^GSPC` (S&P 500), `^IXIC` (Nasdaq), `^FTSE` (FTSE 100)
	- **count** (query): Number of news articles to retrieve (default: 10)
	- **tab** (query): News tab to retrieve (default: "news")
	  - Supported: "news", "press_releases", "all"
	
	Returns:
	- A mapping of index symbol to a list of news articles, where each article includes title, publisher, link, and published time.

	Examples:
	- `/indices/news/^GSPC` - Recent news for S&P 500
	- `/indices/news/^GSPC?count=5` - Last 5 news articles for S&P 500
	- `/indices/news/^GSPC?tab=press_releases` - Press releases
	- `/indices/news/^GSPC,^^IXIC` - Recent news for both S&P 500 and Nasdaq
	"""
	try:
		indices = Indices(m.strip().upper() for m in indices.split(",") if m.strip())
		results = {index.symbol: index._get_news(count=count, tab=tab) for index in indices}
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
	return {
		"indices": results
	}


@app.get("/indices/info/{indices}", tags=["Index"], summary="Get Information for single or multiple Indices")
def get_index_info(indices: str) -> dict:
	"""
	Retrieve detailed information about financial indices.

	Fetches raw info data from Yahoo Finance for any index symbol.

	This endpoint supports both a path and a query form:

	- Path: `/indices/info/{indices}` where `{indices}` is a single symbol or a comma-separated list of symbols.
	  Examples: `/indices/info/^GSPC`, `/indices/info/^GSPC,^IXIC`
	- Query: `/indices/info?indices=^GSPC,^IXIC` (the `indices` query parameter behaves the same)

	Parameters:
	- **indices** (required): Yahoo Finance symbol for the index, or a comma-separated list of symbols
	  - Example: `^GSPC` (S&P 500), `^IXIC` (Nasdaq), `^FTSE` (FTSE 100)

	Returns:
	- A mapping of index symbol to its detailed info data, including attributes like full name, exchange, currency, and more.

	Examples:
	- `/indices/info/^GSPC` - Info for S&P 500
	- `/indices/info/^IXIC` - Info for Nasdaq
	- `/indices/info/^FTSE,^GDAXI` - Info for FTSE 100 and DAX
	"""
	try:
		indices = Indices([m.strip().upper() for m in indices.split(",") if m.strip()])
		results = {index.symbol: index._get_info() for index in indices}
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
	return {
		"indices": results
	}


@app.get("/indices/historic_data/{indices}", tags=["Index"], summary="Get Historical Data for single or multiple Indices")
def get_index_history(indices: str, period: str = "1y", interval: str = "1d") -> dict:
	"""
	Retrieve historical price data for financial indices.

	Fetches raw historical data from Yahoo Finance for any index symbol.

	This endpoint supports both a path and a query form:

	- Path: `/indices/historic_data/{indices}` where `{indices}` is a single symbol or a comma-separated list of symbols.
	  Examples: `/indices/historic_data/^GSPC`, `/indices/historic_data/^GSPC,^IXIC`
	- Query: `/indices/historic_data?indices=^GSPC,^IXIC` (the `indices` query parameter behaves the same)

	Parameters:
	- **indices** (required): Yahoo Finance symbol for the index, or a comma-separated list of symbols
	  - Example: `^GSPC` (S&P 500), `^IXIC` (Nasdaq), `^FTSE` (FTSE 100)
	- **period** (query): Time period for historical data (default: `1y`)
	  - Supported: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`
	- **interval** (query): Data interval/frequency (default: `1d`)
	  - Supported: `1m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `1wk`, `1mo`, `3mo`

	Returns:
	- Index symbol, period, interval, and historical OHLCV data

	Examples:
	- `/indices/historic_data/^GSPC` - S&P 500 last 1 year at daily intervals
	- `/indices/historic_data/^GSPC?period=3mo&interval=1h` - Last 3 months at hourly intervals
	- `/indices/historic_data/^IXIC?period=5y&interval=1wk` - Last 5 years at weekly intervals
	"""
	try:
		indices = Indices([m.strip().upper() for m in indices.split(",") if m.strip()], period=period, interval=interval)
		results = {index.symbol: index._get_historical_data().to_dict() for index in indices}
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
	return {
		"indices": results
	}