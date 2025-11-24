# Project Structure

## Overview

This is a production-ready FastAPI application demonstrating enterprise-level Python development practices for senior developer positions.

## Directory Structure

```
task-manager-api/
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # GitHub Actions CI/CD pipeline
├── alembic/
│   ├── versions/               # Database migration versions
│   ├── env.py                  # Alembic environment configuration
│   └── script.py.mako         # Migration template
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI application entry point
│   ├── config.py              # Configuration and settings
│   ├── database.py            # Database setup and session management
│   ├── models/
│   │   └── __init__.py        # SQLAlchemy models (User, Task)
│   ├── schemas/
│   │   └── __init__.py        # Pydantic schemas for validation
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── tasks.py           # Task management endpoints
│   │   └── users.py           # User management endpoints
│   └── utils/
│       ├── __init__.py
│       └── auth.py            # Authentication utilities (JWT, password hashing)
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures and configuration
│   ├── test_main.py           # Main application tests
│   ├── test_auth.py           # Authentication tests
│   ├── test_tasks.py          # Task management tests
│   ├── test_users.py          # User management tests
│   └── integration/
│       ├── __init__.py
│       └── test_workflow.py   # End-to-end integration tests
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore patterns
├── .pre-commit-config.yaml    # Pre-commit hooks configuration
├── alembic.ini                # Alembic configuration
├── CONTRIBUTING.md            # Contribution guidelines
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Multi-stage Docker build
├── LICENSE                    # MIT License
├── Makefile                   # Common development commands
├── pytest.ini                 # Pytest configuration
├── README.md                  # Main project documentation
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
└── SECURITY.md                # Security policies and best practices
```

## Key Components

### Application (app/)

#### main.py
- FastAPI application initialization
- Middleware configuration (CORS, security headers, trusted hosts)
- Router inclusion
- Global exception handling
- Lifespan events (startup/shutdown)

#### config.py
- Environment variable management using pydantic-settings
- Configuration validation
- Security settings
- Database configuration

#### database.py
- Async SQLAlchemy engine setup
- Session management
- Database dependency injection

#### models/
- SQLAlchemy ORM models
- User model with authentication fields
- Task model with relationships
- Enums for status and priority

#### schemas/
- Pydantic models for request/response validation
- Strong typing with validation rules
- Password strength validation
- Email validation

#### routers/
- API endpoint implementations
- Authentication (register, login, logout)
- Task CRUD operations
- User profile management
- Proper HTTP status codes
- Error handling

#### utils/
- JWT token generation and validation
- Password hashing with bcrypt
- User authentication utilities
- Dependency injection for current user

### Tests (tests/)

#### conftest.py
- Pytest configuration
- Test database setup
- Async client fixture
- Authentication fixtures

#### Test Files
- Comprehensive unit tests for all endpoints
- Integration tests for complete workflows
- 95%+ code coverage target
- Async test support

### CI/CD (.github/workflows/)

#### ci-cd.yml
- Multi-job pipeline:
  - Code quality checks (Black, isort, flake8, pylint, mypy)
  - Security scanning (Bandit, Safety)
  - Tests on multiple Python versions
  - Docker build testing
  - Integration tests with PostgreSQL
  - Coverage reporting

### Infrastructure

#### Dockerfile
- Multi-stage build for optimization
- Non-root user for security
- Minimal alpine-based image
- Health check configuration

#### docker-compose.yml
- Complete development environment
- PostgreSQL database
- Adminer for database management
- Volume management
- Network configuration

#### Makefile
- Common development commands
- Easy setup and testing
- Docker operations
- Database migrations

## Key Features

### Security
- JWT authentication
- Password hashing with bcrypt
- Input validation
- SQL injection prevention
- Security headers
- CORS configuration
- Non-root Docker containers

### Code Quality
- Type hints throughout
- Black code formatting
- isort import sorting
- flake8 linting
- mypy type checking
- Pre-commit hooks

### Testing
- Async test support
- Comprehensive test coverage
- Unit and integration tests
- Test fixtures
- Coverage reporting

### Documentation
- OpenAPI/Swagger UI
- ReDoc
- Comprehensive README
- Security documentation
- Contributing guidelines

### Database
- Async SQLAlchemy
- Alembic migrations
- PostgreSQL support
- Connection pooling

### DevOps
- CI/CD with GitHub Actions
- Docker support
- Docker Compose for development
- Environment-based configuration
- Automated security scanning

## Getting Started

See [README.md](README.md) for installation and usage instructions.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## Security

See [SECURITY.md](SECURITY.md) for security policies and best practices.
