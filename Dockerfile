FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Minimal install: copy only requirements first for caching, install, then copy app
COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

# Run the ASGI app; override in docker-compose or CLI as needed
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]