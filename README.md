# Agent Bookkeeping Platform

A complete full-stack agent-native bookkeeping platform with modern technology stack.

## Project Overview

This platform provides professional accounting and financial management capabilities with:

- **FastAPI Backend**: RESTful API with comprehensive bookkeeping operations
- **Next.js Frontend**: Modern React UI with TypeScript
- **PostgreSQL Database**: Robust relational database
- **Redis & Celery**: Async task processing for invoice and receipt handling
- **Docker Compose**: Complete containerized deployment

## Features

### Core Functionality
- **Account Management**: Create and manage chart of accounts (Assets, Liabilities, Equity, Revenue, Expenses)
- **Journal Entries**: Double-entry bookkeeping records
- **Transactions**: Raw transaction tracking with status management
- **Invoices**: Invoice creation, management, and status tracking
- **Payments**: Payment recording and linking to invoices
- **Receipts**: Receipt uploads and file management

### Technical Features
- RESTful API with CRUD operations for all entities
- Pydantic validation for all requests
- SQLAlchemy ORM with PostgreSQL
- Celery async tasks for background processing
- Periodic tasks (overdue invoice checking)
- Comprehensive error handling and logging
- CORS support for frontend integration
- Health check endpoints

## Project Structure

```
.
├── backend/
│   ├── models/              # SQLAlchemy models
│   ├── routes/              # FastAPI routers
│   ├── schemas/             # Pydantic schemas
│   ├── tasks/               # Celery tasks
│   ├── utils/               # Utility functions
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # Database configuration
│   └── celery_config.py     # Celery configuration
├── frontend/
│   ├── src/
│   │   ├── pages/           # Next.js pages
│   │   ├── components/      # React components
│   │   ├── lib/             # Utility libraries
│   │   └── public/          # Static files
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   └── Dockerfile
├── docker-compose.yml       # Docker orchestration
├── Dockerfile.backend       # Backend container
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
└── README.md
```

## Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)
- PostgreSQL 16+ (if running without Docker)
- Redis 7+ (if running without Docker)

## Quick Start with Docker

### 1. Clone and Setup

```bash
git clone https://github.com/andybookkeeper/agent-bookkeeping.git
cd agent-bookkeeping
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` if needed (defaults work for local development):

```bash
ENV=development
DB_PASSWORD=password
REDIS_URL=redis://redis:6379/0
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Services

```bash
docker-compose up --build
```

Services will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 4. Access the Application

1. Open http://localhost:3000 in your browser
2. Navigate to Dashboard to view statistics
3. Use the sidebar to manage Accounts, Transactions, Invoices, etc.

## Local Development Setup

### Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run database migrations (optional - tables created automatically)
# alembic upgrade head

# Start FastAPI server
uvicorn backend.main:app --reload
```

Backend will run on http://localhost:8000

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local if needed
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

Frontend will run on http://localhost:3000

### Celery Worker (in separate terminal)

```bash
celery -A backend.tasks worker --loglevel=info
```

### Celery Beat (for periodic tasks, optional)

```bash
celery -A backend.tasks beat --loglevel=info
```

## API Endpoints

### Accounts
- `GET /api/accounts` - List accounts
- `GET /api/accounts/{id}` - Get account
- `POST /api/accounts` - Create account
- `PUT /api/accounts/{id}` - Update account
- `DELETE /api/accounts/{id}` - Delete account

### Journal Entries
- `GET /api/journal-entries` - List entries
- `GET /api/journal-entries/{id}` - Get entry
- `POST /api/journal-entries` - Create entry
- `PUT /api/journal-entries/{id}` - Update entry
- `DELETE /api/journal-entries/{id}` - Delete entry

### Transactions
- `GET /api/transactions` - List transactions
- `GET /api/transactions/{id}` - Get transaction
- `POST /api/transactions` - Create transaction
- `PUT /api/transactions/{id}` - Update transaction
- `DELETE /api/transactions/{id}` - Delete transaction

### Invoices
- `GET /api/invoices` - List invoices
- `GET /api/invoices/{id}` - Get invoice
- `POST /api/invoices` - Create invoice
- `PUT /api/invoices/{id}` - Update invoice
- `DELETE /api/invoices/{id}` - Delete invoice

### Payments
- `GET /api/payments` - List payments
- `GET /api/payments/{id}` - Get payment
- `POST /api/payments` - Create payment
- `PUT /api/payments/{id}` - Update payment
- `DELETE /api/payments/{id}` - Delete payment

### Receipts
- `GET /api/receipts` - List receipts
- `GET /api/receipts/{id}` - Get receipt
- `POST /api/receipts` - Create receipt
- `PUT /api/receipts/{id}` - Update receipt
- `DELETE /api/receipts/{id}` - Delete receipt

### System
- `GET /health` - Health check
- `GET /` - API info

## Database Schema

### Accounts Table
- id (UUID)
- name (String)
- type (Enum: asset, liability, equity, revenue, expense)
- balance (Float)
- created_at, updated_at (DateTime)

### Journal Entries Table
- id (UUID)
- date (DateTime)
- description (String)
- account_id (FK)
- amount (Float)
- type (Enum: debit, credit)
- created_at, updated_at (DateTime)

### Transactions Raw Table
- id (UUID)
- date (DateTime)
- description (String)
- amount (Float)
- source (String)
- status (Enum: pending, processing, completed, failed)
- created_at, updated_at (DateTime)

### Invoices Table
- id (UUID)
- account_id (FK)
- amount (Float)
- date (DateTime)
- due_date (DateTime)
- status (Enum: draft, sent, paid, overdue, cancelled)
- created_at, updated_at (DateTime)

### Payments Table
- id (UUID)
- invoice_id (FK)
- amount (Float)
- date (DateTime)
- method (String)
- created_at, updated_at (DateTime)

### Receipts Table
- id (UUID)
- transaction_id (FK)
- file_path (String)
- uploaded_at (DateTime)
- created_at, updated_at (DateTime)

## Background Tasks

### Invoice Processing
- Task: `process_invoice(invoice_id)`
- Updates invoice status to "sent"
- Max retries: 3

### Receipt Parsing
- Task: `parse_receipt(receipt_id)`
- Extracts data from receipt files
- Max retries: 3

### Overdue Invoice Check
- Periodic task running hourly
- Automatically marks invoices as "overdue" when due_date passes
- Skips already paid or cancelled invoices

## Environment Variables

```
# Required
DATABASE_URL=postgresql://bookkeeper:password@localhost:5432/bookkeeping
REDIS_URL=redis://localhost:6379/0

# Optional with defaults
ENV=development (development/production)
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
NEXT_PUBLIC_API_URL=http://localhost:8000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
LOG_DIR=logs
SQL_ECHO=false (set to true for SQL debug logging)
```

## Production Deployment

### Using Docker Compose

```bash
# Set environment to production
ENV=production docker-compose up -d

# Or update .env:
sed -i 's/ENV=development/ENV=production/' .env

# Start services
docker-compose up -d
```

### Security Recommendations

1. Change database password in `.env`
2. Generate secure ALLOWED_ORIGINS list
3. Use HTTPS in production
4. Set up proper logging and monitoring
5. Configure database backups
6. Use environment-specific secrets management
7. Enable SQL debug only when necessary

## Logging

Logs are written to the `logs/` directory:
- `logs/backend.main.log` - Application logs
- `logs/celery.log` - Celery worker logs

Configure LOG_LEVEL in `.env`:
- DEBUG, INFO, WARNING, ERROR, CRITICAL

## Error Handling

The application implements:
- Global exception handlers returning meaningful error messages
- Database transaction rollback on errors
- Retry logic for Celery tasks
- Input validation via Pydantic schemas
- Comprehensive logging for debugging

## Testing

Run API tests:
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
docker-compose logs postgres

# Verify credentials in .env
# Default: bookkeeper/password
```

### Redis Connection Error
```bash
# Check Redis is running
docker-compose logs redis

# Verify Redis URL in .env
```

### Frontend API Connection Issues
```bash
# Check NEXT_PUBLIC_API_URL matches backend address
# Verify CORS settings in backend/main.py
# Check network connectivity between containers
```

### Celery Tasks Not Running
```bash
# Check Celery worker is running
docker-compose logs celery-worker

# Verify Redis connection
docker-compose logs celery-beat

# Check task definitions in backend/tasks/__init__.py
```

## Performance Optimization

1. **Database**: Use indexes on frequently queried fields
2. **Caching**: Implement Redis caching for read-heavy operations
3. **Pagination**: Always use limit/skip for list endpoints
4. **Async Tasks**: Offload heavy operations to Celery
5. **Frontend**: Leverage Next.js automatic code splitting

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Check documentation at `/docs` endpoint

## Architecture Diagrams

### Service Architecture
```
┌─────────────────────────────────────────────┐
│         Next.js Frontend (Port 3000)         │
└────────────────────┬────────────────────────┘
                     │ HTTP
┌─────────────────────▼────────────────────────┐
│       FastAPI Backend (Port 8000)            │
│   ├── Accounts Routes                        │
│   ├── Journal Entries Routes                 │
│   ├── Transactions Routes                    │
│   ├── Invoices Routes                        │
│   ├── Payments Routes                        │
│   └── Receipts Routes                        │
└────────┬──────────────────────────┬──────────┘
         │                          │
    ┌────▼─────┐            ┌──────▼────┐
    │PostgreSQL│            │   Redis   │
    │Database  │            │   Queue   │
    └──────────┘            └──────┬────┘
                                   │
                     ┌─────────────┼─────────────┐
                     │             │             │
                ┌────▼────┐   ┌────▼─────┐  ┌──▼───────┐
                │ Celery  │   │ Celery   │  │Celery    │
                │ Worker  │   │ Beat     │  │Flower    │
                └─────────┘   └──────────┘  └──────────┘
```

## Changelog

### Version 1.0.0 (Initial Release)
- Full API implementation for all entities
- Frontend dashboard and management pages
- Docker Compose orchestration
- Celery async task processing
- Comprehensive error handling and logging

---

**Last Updated**: 2024

**Maintained by**: Andy Bookkeeper Team
