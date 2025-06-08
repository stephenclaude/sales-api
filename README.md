# Sales API

A Flask-based REST API for analyzing sales data from a SQLite database.

## Features

- Get top sales representative for a specific year
- Get all top sales representatives with sorting options
- Input validation and error handling
- Comprehensive test suite
- Docker support
- Type hints and proper code organization

## API Endpoints

### 1. Get Top Seller by Year

```
GET /api/v1/sellers/<year>/top
```

**Response:**
```json
{
  "Sales Rep": "Jane Peacock",
  "Total Sales": 184.34
}
```

### 2. Get All Top Sellers

```
GET /api/v1/sellers/top
```

**Query Parameters:**
- `order_by`: `sales_rep`, `total_sales`, `year` (default: `total_sales`)
- `order`: `asc`, `desc` (default: `desc`)

**Response:**
```json
[
  {
    "Sales Rep": "Steve Johnson",
    "Total Sales": 164.34,
    "Year": "2009"
  },
  {
    "Sales Rep": "Jane Peacock",
    "Total Sales": 221.91,
    "Year": "2010"
  }
]
```

### 3. Health Check

```
GET /health
```

## Prerequisites

- Python 3.8+
- SQLite database file (`data.db`)

## Installation & Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd sales-api
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add database file

Place your `data.db` file in the project root directory.

## Running the Application

### Local Development

```bash
python main.py
```

The API will be available at `http://localhost:5000`

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t sales-api .
docker run -p 5000:5000 -v $(pwd)/data.db:/app/data.db:ro sales-api
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

## Code Quality

### Format code with Black

```bash
black .
```

### Lint with flake8

```bash
flake8 app/ tests/
```

### Type checking with mypy

```bash
mypy app/
```

## Project Structure

```
sales-api/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── api.py               # API endpoints and Flask app
│   └── database.py          # Database operations
├── tests/
│   ├── __init__.py
│   └── test_api.py          # API tests
├── data.db                  # SQLite database (not in repo)
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── README.md               # This file
└── main.py                 # Application entry point
```

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid parameters
- **404 Not Found**: No data found for the request
- **500 Internal Server Error**: Database or server errors

All errors return JSON responses with error details:

```json
{
  "error": "Invalid year",
  "message": "Year must be between 2000 and 2030"
}
```

## Database Schema

The API expects a SQLite database with the following tables:
- `Invoice` - Contains sales transactions
- `Customer` - Customer information
- `Employee` - Employee/sales rep information

## Extending the Application

### Managing Secrets for Production Databases

For production use with external databases, consider these approaches:

#### 1. Environment Variables

```python
import os
from urllib.parse import quote_plus

# Database configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'sales_db')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')

# Connection string
DATABASE_URL = f"postgresql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}/{DB_NAME}"
```

#### 2. Configuration Files

Create a `config.py` file:

```python
import os
from dataclasses import dataclass

@dataclass
class Config:
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///data.db')
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
class ProductionConfig(Config):
    DEBUG: bool = False
    
class DevelopmentConfig(Config):
    DEBUG: bool = True
```

#### 3. Docker Secrets

For Docker Swarm:

```yaml
version: '3.8'
services:
  sales-api:
    image: sales-api
    secrets:
      - db_password
    environment:
      - DATABASE_URL=postgresql://user:password@db/sales
    
secrets:
  db_password:
    file: ./secrets/db_password.txt
```

#### 4. External Secret Management

For production systems, consider:
- **AWS Secrets Manager**
- **Azure Key Vault**
- **HashiCorp Vault**
- **Kubernetes Secrets**

Example with AWS Secrets Manager:

```python
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Usage
db_config = get_secret('prod/database/config')
DATABASE_URL = db_config['connection_string']
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Format code with Black
7. Submit a pull request

## License

This project is licensed under the MIT License.