# FinZen

> Your financial copilot

FinZen is an AI-powered financial planning assistant that helps users understand their finances, explore investments, plan budgets, calculate taxes and SIP returns, review insurance needs, and interact with financial data through a web interface and API.

## Features

- **AI financial chat** for finance-focused questions and recommendations.
- **Dashboard aggregation** for income, net worth, budgets, goals, and selected assets.
- **Investment research** for stocks and market-related queries.
- **Property research** based on a requested location.
- **Tax planning** with estimated tax calculations and regime information.
- **SIP calculations** including invested amount, estimated future value, and gains.
- **Insurance guidance** based on income and age.
- **PDF transaction ingestion** for extracting transactions from uploaded documents.
- **Trade workflow support** through the investment agent integration.
- **Market data and chart history** using Yahoo Finance data.
- **React-compatible response cards** for stocks, trades, insurance, SIP calculations, and tax results.

## Project structure

The application is located in the `finzen v3` directory:

```text
finzen v3/
├── api.py                 # FastAPI application and API routes
├── app/                   # Core, database, service, and agent modules
├── frontend/              # Frontend application
├── config.yaml            # Model, intent, safety, and response configuration
├── ingest.py              # Data ingestion utilities
├── ingest_pdf.py          # PDF transaction processing
├── init_database.py       # Database initialization
├── seed.py                # Seed data utilities
├── requirement.txt        # Python dependencies
├── package.json            # JavaScript dependencies
└── test_*.py              # Test and integration scripts
```

## Requirements

- Python 3.10+
- Node.js and npm
- A database supported by SQLAlchemy/PostgreSQL configuration
- API credentials for the AI, brokerage, or external data services enabled in your local configuration

## Installation

Clone the repository and move into the application directory:

```bash
git clone https://github.com/gogul098/Fin_zen.git
cd Fin_zen/"finzen v3"
```

Create and activate a Python virtual environment:

```bash
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.venv\\Scripts\\Activate.ps1
```

Install the backend dependencies:

```bash
pip install -r requirement.txt
```

Install the frontend dependencies:

```bash
cd frontend
npm install
cd ..
```

The repository also contains a root-level JavaScript dependency manifest with `axios`.

## Configuration

Before starting the application, configure the environment variables required by the services in `app/` and the database configuration. Store secrets in a local `.env` file and do not commit it.

Typical integrations may require credentials for:

- AI model providers
- Brokerage or trading services
- PostgreSQL/database access
- Market data or research services

Review `config.yaml` and the service modules in `app/` to determine the exact variables required by your deployment.

## Database setup

From the `finzen v3` directory, initialize and seed the database as needed:

```bash
python init_database.py
python seed.py
```

Run only the commands that match your local database configuration.

## Running the backend

Start the FastAPI server from the `finzen v3` directory:

```bash
python api.py
```

The API runs on:

```text
http://localhost:8001
```

Interactive API documentation is available at:

- `http://localhost:8001/docs`
- `http://localhost:8001/redoc`

You can also start it with Uvicorn:

```bash
uvicorn api:app --host 0.0.0.0 --port 8001 --reload
```

## API overview

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Health check |
| `GET` | `/dashboard/{user_id}` | Retrieve dashboard data |
| `GET` | `/recommendations/stock` | Retrieve stock recommendations |
| `GET` | `/recommendations/property` | Retrieve property recommendations |
| `POST` | `/update-context` | Save user context |
| `POST` | `/upload-pdf` | Upload and process a transaction PDF |
| `POST` | `/trade` | Submit a trade request |
| `POST` | `/chat` | Send a message to the FinZen financial assistant |

Example health check:

```bash
curl http://localhost:8001/
```

Example chat request:

```bash
curl -X POST http://localhost:8001/chat \\
  -H "Content-Type: application/json" \\
  -d '{"message":"Calculate the future value of a SIP of 5000 for 10 years","user_id":1}'
```

## Running the frontend

The frontend is located at `finzen v3/frontend`. Start it using the scripts defined in its `package.json`:

```bash
cd frontend
npm install
npm run dev
```

If the frontend uses a different start script, run `npm run` to list the available scripts.

## Testing

Run the available Python test scripts from the `finzen v3` directory:

```bash
python test_requests.py
python test_alpaca.py
```

Some tests may require configured external services, credentials, a running backend, or seeded database records.

## Safety and disclaimer

FinZen is a software project for financial education, planning assistance, and experimentation. Its responses, calculations, market data, recommendations, and trade-related workflows may be incomplete or inaccurate. They are **not financial, tax, legal, or investment advice**. Always verify information with qualified professionals and use appropriate safeguards before making financial decisions or executing trades.

Do not commit API keys, brokerage credentials, database passwords, personal financial records, or other sensitive information to the repository.

## Contributing

1. Create a feature branch.
2. Make focused changes.
3. Add or update tests where appropriate.
4. Confirm that secrets and personal data are not included.
5. Open a pull request with a clear description of the change.

## License

No license has been specified yet. Until a license is added, the repository should be treated as **all rights reserved**.
