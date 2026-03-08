# yfinance_api

Small helper API and scripts for downloading and providing market data via yfinance.

## Overview

This repository contains lightweight helper tools for retrieving financial data, simple utility functions, and a small API entry point. It is designed to be easy to run locally or inside a container.

## Project Structure

- `api.py` – Minimal HTTP entry point / example runner for the API that provides endpoints for financial data.
- `helper.py` – Helper functions used by the API and scripts, e.g. for data serialization.
- `models/` – Data models and schema helpers for structuring retrieved data such as markets, indices, etc.
- `Dockerfile` / `docker-compose.yml` – Optional, for containerizing the API.
- `requirements.txt` / `Pipfile` – Python dependency files.

## Prerequisites

- Python 3.12 or newer is installed.
- A virtual environment is used for development (venv, pipenv, or similar).
- Network access to external data providers is available.
- If running in Docker, Docker must be installed and configured on the host.

## Installation

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

**Alternatively with Pipenv**:

```bash
pipenv install
pipenv shell
```

## Usage

1. Start the API locally:

```bash
uvicorn api:app --reload --port 8000 --host localhost
```

2. Start the API in a Docker container:

```bash
docker build -t yfinance_api .
docker run --rm -p 8000:8000 yfinance_api
```

3. Call API endpoints (example):

```bash
curl http://localhost:8000/markets
curl http://localhost:8000/markets/status/US
```

Alternatively via a browser or tools such as Postman. The OpenAPI documentation is available at `http://localhost:8000/docs`.

## Configuration

- Currently no environment variables are required by default. If API keys or additional settings become necessary, document them here.

## Next Steps

- `/models/` – Add additional data models (e.g. stocks, ETFs, etc.).
- `/api.py` – Add additional endpoints for specific data (e.g. historical data, financial metrics, etc.).
- Improve error handling and logging.
- Add tests (unit tests for models and API endpoints).