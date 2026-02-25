
# yfinance_api

Kleine Hilfs-API und Skripte zum Herunterladen und Bereitstellen von Marktdaten über yfinance.

## Übersicht

Dieses Repository enthält schlanke Hilfsprogramme zum Abrufen von Finanzdaten, einfache Helferfunktionen und einen kleinen API-Einstiegspunkt. Es ist so konzipiert, dass es lokal oder in einem Container einfach zu betreiben ist.

## Projektstruktur

- `api.py` - Minimaler HTTP-Einstiegspunkt / Beispiel-Runner für die API, der Endpunkte für Finanzdaten bereitstellt.
- `helper.py` - Hilfsfunktionen, die von der API und Skripten genutzt werden, z.B. zur Datenserialisierung.
- `models/` - Datenmodelle und Schema-Hilfen zur Strukturierung der abgerufenen Daten wie Märkte, Indizes, etc.
- `Dockerfile` / `docker-compose.yml` - Optional, für die Containerisierung der API.
- `requirements.txt` / `Pipfile` - Python-Abhängigkeitsdateien.

## Annahmen

- Python 3.12 oder neuer ist vorhanden.
- Es wird eine virtuelle Umgebung für die Entwicklung verwendet (venv, pipenv oder ähnlich).
- Netzwerkzugang zu externen Datenanbietern ist verfügbar.
- Bei Ausführung in Docker ist Docker auf dem Host installiert und konfiguriert.

## Installation

1. Erstelle und aktiviere eine virtuelle Umgebung:

```bash
python -m venv venv
source venv/bin/activate
```

2. Installiere die Abhängigkeiten:

```bash
pip install -r requirements.txt
```

**Alternativ mit Pipenv**:

```bash
pipenv install
pipenv shell
```

## Nutzung

1. Lokal API starten:

```bash
uvicorn api:app --reload --port 8000 --host localhost
```

2. API im Docker-Container starten:

```bash
docker build -t yfinance_api .
docker run --rm -p 8000:8000 yfinance_api
```

3. API-Endpunkte aufrufen (Beispiel):
```bash
curl http://localhost:8000/markets
curl http://localhost:8000/markets/status/US
```

Alternativ über den Browser oder Tools wie Postman. OpenAPI-Dokumentation ist unter `http://localhost:8000/docs` verfügbar.

## Konfiguration

- Aktuell sind standardmäßig keine Umgebungsvariablen erforderlich. Falls API-Schlüssel oder weitere Einstellungen nötig werden, dokumentiere sie hier.

## Nächste Schritte

- /models/ - Weitere Datenmodelle hinzufügen (z.B. Aktien, ETFS, etc.)
- /api.py - Weitere Endpunkte für spezifische Daten hinzufügen (z.B. historische Daten, Finanzkennzahlen, etc.)
- Fehlerbehandlung und Logging verbessern.
- Tests hinzufügen (Unit-Tests für Modelle und API-Endpunkte).