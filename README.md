# Task Manager API

A production-ready RESTful API built with FastAPI demonstrating enterprise-level Python development practices.

## 🚀 Features

- **Modern FastAPI Framework**: Async/await support, automatic OpenAPI documentation
- **Secure Authentication**: JWT-based authentication with password hashing
- **Database Integration**: SQLAlchemy ORM with PostgreSQL support
- **Comprehensive Testing**: 95%+ code coverage with pytest
- **Security First**: Input validation, SQL injection prevention, security headers
- **CI/CD Pipeline**: Automated testing, linting, and security scanning
- **Docker Support**: Multi-stage builds for optimized production images
- **Type Safety**: Full type hints with mypy validation
- **Code Quality**: Pre-commit hooks, Black, isort, flake8, pylint

## 📋 Requirements

- Python 3.11+
- PostgreSQL 14+ (or SQLite for development)
- Docker & Docker Compose (optional)

## 🛠️ Installation

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/task-manager-api.git
cd task-manager-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start the development server
uvicorn app.main:app --reload
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# The API will be available at http://localhost:8000
```

## 🧪 Testing

```bash
# Run all tests with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

## 🔒 Security Features

- **Password Security**: Bcrypt hashing with salt
- **JWT Authentication**: Secure token-based auth with expiration
- **Input Validation**: Pydantic models for request validation
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **CORS Configuration**: Configurable CORS policies
- **Security Headers**: Helmet-style security headers
- **Rate Limiting**: Protection against brute force attacks
- **Dependency Scanning**: Automated vulnerability checks in CI/CD

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ Project Structure

```
task-manager-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database setup
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── routers/             # API endpoints
│   ├── services/            # Business logic
│   └── utils/               # Utility functions
├── tests/                   # Test suite
├── alembic/                 # Database migrations
├── .github/
│   └── workflows/           # CI/CD pipelines
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## 🔄 CI/CD Pipeline

The project includes GitHub Actions workflows for:
- ✅ Automated testing on multiple Python versions
- 🔍 Code quality checks (Black, isort, flake8, mypy)
- 🛡️ Security scanning (Bandit, Safety)
- 📊 Code coverage reporting
- 🐳 Docker image building and testing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

Your Name - [@yourhandle](https://github.com/yourhandle)

## 🙏 Acknowledgments

- FastAPI for the excellent framework
- The Python community for amazing tools and libraries
