# Quick Start Guide

## Prerequisites
- Python 3.11 or higher
- Git
- Docker and Docker Compose (optional)

## 5-Minute Setup

### Option 1: Local Development (Recommended for First Time)

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# 3. Set up environment variables
cp .env.example .env

# 4. Edit .env and set your SECRET_KEY (minimum 32 characters)
# You can generate one with: openssl rand -hex 32

# 5. Run the application
uvicorn app.main:app --reload

# 6. Open browser to http://localhost:8000/docs
```

### Option 2: Docker (Easiest Setup)

```bash
# 1. Start all services
docker-compose up -d

# 2. Open browser to http://localhost:8000/docs

# 3. View logs
docker-compose logs -f
```

## First API Calls

### 1. Register a User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "SecurePass123!",
    "full_name": "Test User"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "SecurePass123!"
  }'
```

Save the `access_token` from the response.

### 3. Create a Task
```bash
# Replace YOUR_TOKEN with the access_token from login
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Task",
    "description": "This is a test task",
    "priority": "high"
  }'
```

### 4. Get Your Tasks
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Interactive API Documentation

Open http://localhost:8000/docs in your browser for:
- Interactive API testing
- Complete endpoint documentation
- Request/response examples
- Authentication testing

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Development Commands

```bash
# Format code
make format

# Run linting
make lint

# Run security checks
make security

# Create database migration
make migrate-create MESSAGE="your migration message"

# Apply migrations
make migrate-up

# Start development server
make run

# View all available commands
make help
```

## Project Structure Highlights

```
app/
├── main.py          # Application entry point
├── routers/         # API endpoints
│   ├── auth.py      # Authentication
│   ├── tasks.py     # Task management
│   └── users.py     # User management
├── models/          # Database models
├── schemas/         # Request/response validation
└── utils/           # Utilities (auth, etc.)
```

## Key Features to Explore

1. **Authentication**: JWT-based with secure password hashing
2. **API Documentation**: Auto-generated OpenAPI/Swagger docs
3. **Database**: Async SQLAlchemy with migrations
4. **Testing**: 95%+ coverage with pytest
5. **Security**: Multiple security layers (headers, validation, etc.)
6. **CI/CD**: Automated testing and security scanning

## Next Steps

1. Read [README.md](README.md) for detailed information
2. Check [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
3. Review [SECURITY.md](SECURITY.md) for security best practices
4. Explore [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for architecture details

## Troubleshooting

### Database Connection Issues
```bash
# Reset database
make db-reset
```

### Port Already in Use
```bash
# Change port in command
uvicorn app.main:app --reload --port 8001
```

### Docker Issues
```bash
# Clean up and restart
docker-compose down -v
docker-compose up --build
```

## Support

For issues or questions:
1. Check the documentation
2. Review existing issues on GitHub
3. Open a new issue with details

---

**Happy Coding! 🚀**
