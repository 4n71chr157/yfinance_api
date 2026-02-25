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
	- List of all supported markets (US, GB, ASIA, EUROPE, RATES, COMMODITIES, CURRENCIES, CRYPTOCURRENCIES)
	"""
	return {
		"markets": [market.value for market in MarketEnum]
	}


@app.get("/markets/status/{markets}", tags=["Market"], summary="Get Status for single or multiple Markets (path)")
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
	results = {}
	for market in market_list:
		try:
			market_enum = MarketEnum(market)
			m = Market(market_enum.value)
			results[market_enum.value] = serialize(getattr(m, "status", None))
		except ValueError:
			raise HTTPException(status_code=400, detail=f"Invalid market: {market}")
		except Exception as e:
			raise HTTPException(status_code=400, detail=str(e))

	return {"markets": results}


@app.get("/markets/summary/{markets}", tags=["Market"], summary="Get Summary for single or multiple Markets (path)")
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
	results = {}
	for market in market_list:
		try:
			market_enum = MarketEnum(market)
			m = Market(market_enum.value)
			results[market_enum.value] = serialize(getattr(m, "summary", None))
		except ValueError:
			raise HTTPException(status_code=400, detail=f"Invalid market: {market}")
	return {"markets": results}


@app.get("/index/news/{index}", tags=["Index"], summary="Get Index News")
def get_index_news(index: str, count: int = 10, tab: str = "news") -> dict:
	"""
	Retrieve recent news articles related to a financial index.

	Fetches raw news data from Yahoo Finance for any index symbol.

	Parameters:
	- **index** (required): Yahoo Finance symbol for the index
	  - Example: `^GSPC` (S&P 500), `^IXIC` (Nasdaq), `^FTSE` (FTSE 100)
	- **count** (query): Number of news articles to retrieve (default: 10)
	- **tab** (query): News tab to retrieve (default: "news")
	  - Supported: "news", "press_releases", "all"
	Returns:
	- Index symbol and list of recent news articles with title, publisher, link, and published date

	Examples:
	- `/index/news/^GSPC` - Recent news for S&P 500
	- `/index/news/^IXIC` - Recent news for Nasdaq
	- `/index/news/^FTSE` - Recent news for FTSE 100
	"""
	try:
		i = Index(index)
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
	return {
		"index": index, 
		"news": i._get_news(count=count, tab=tab)
	}


@app.get("/index/info/{index}", tags=["Index"], summary="Get Index Info")
def get_index_info(index: str) -> dict:
	"""
	Retrieve detailed information about a financial index.

	Fetches raw info data from Yahoo Finance for any index symbol.

	Parameters:
	- **index** (required): Yahoo Finance symbol for the index
	  - Example: `^GSPC` (S&P 500), `^IXIC` (Nasdaq), `^FTSE` (FTSE 100)

	Returns:
	- Index symbol and detailed info including name, exchange, currency, etc.

	Examples:
	- `/index/info/^GSPC` - Info for S&P 500
	- `/index/info/^IXIC` - Info for Nasdaq
	- `/index/info/^FTSE` - Info for FTSE 100
	"""
	try:
		i = Index(index)
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
	return {
		"index": index, 
		"info":	 i._get_info()
	}


@app.get("/index/historic_data/{index}", tags=["Index"], summary="Get Index Historical Data")
def get_index_history(index: str, period: str = "1y", interval: str = "1d") -> dict:
	"""
	Retrieve historical price data for a financial index.

	Fetches raw historical data from Yahoo Finance for any index symbol.

	Parameters:
	- **index** (required): Yahoo Finance symbol for the index
	  - Example: `^GSPC` (S&P 500), `^IXIC` (Nasdaq), `^FTSE` (FTSE 100)
	- **period** (query): Time period for historical data (default: `1y`)
	  - Supported: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`
	- **interval** (query): Data interval/frequency (default: `1d`)
	  - Supported: `1m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `1wk`, `1mo`, `3mo`

	Returns:
	- Index symbol, period, interval, and historical OHLCV data

	Examples:
	- `/index/historic_data/^GSPC` - S&P 500 last 1 year at daily intervals
	- `/index/historic_data/^GSPC?period=3mo&interval=1h` - Last 3 months at hourly intervals
	- `/index/historic_data/^IXIC?period=5y&interval=1wk` - Last 5 years at weekly intervals
	"""
	try:
		i = Index(index, period=period, interval=interval)
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
	return {
		"index": index, 
		"period": period, 
		"interval": interval, 
		"data": i._get_historical_data().to_dict(orient="records")
	}