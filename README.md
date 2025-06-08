# Sales API

A Flask-based REST API for querying sales representative data from a SQLite database.

## Features

- Get top sales rep by year  
- Get all reps with filters and sorting  
- Input validation & error handling  
- Docker support  
- Test coverage and linting

## Endpoints

### 1. Get Top Sales Rep by Year  
`GET /api/v1/sellers/<year>/top`

**Response:**
```json
{
  "Sales Rep": "Jane Peacock",
  "Total Sales": 184.34
}
```

### 2. Get All Top Sales Reps
`GET /api/v1/sellers/top`

**Query Parameters:**
- `order_by`: sales_rep, total_sales, year (default: total_sales)
- `order`: asc, desc (default: desc)

**Sample Response:**
```json
[
  {
    "Sales Rep": "Steve Johnson",
    "Total Sales": 164.34,
    "Year": "2009"
  }
]
```

## Getting Started

### Local Development
```bash
git clone <your-repo-url>
cd sales-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```
Visit: http://localhost:5000

### Docker
```bash
docker build -t sales-api .
docker run -p 5000:5000 sales-api
```

## Running Tests
```bash
# Run all tests
pytest

# With coverage
pytest --cov=app

# Specific test
pytest tests/test_api.py::test_health_check
```

## Code Quality Tools
```bash
black .        # Format
flake8 .       # Lint
mypy .         # Type checks
```

## Using Production Databases

This app uses SQLite for development.
To switch to production databases (e.g. PostgreSQL), you'll need secure secret management for credentials.

**Recommended Options:**
- Environment variables (simple and effective)
- AWS Secrets Manager, Azure Key Vault, or Docker Secrets for enterprise-grade security

**Do not hardcode secrets.** Use .env (ignored in git), rotate keys regularly, and enforce least-privilege access.

## Project Structure
```
sales-api/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py
├── tests/
│   └── test_api.py
├── data.db
├── requirements.txt
├── Dockerfile
├── .env
├── .gitignore
├── README.md
└── run.py
```