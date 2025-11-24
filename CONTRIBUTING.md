# Contributing to Task Manager API

Thank you for considering contributing to this project! 

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/task-manager-api.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
5. Install dependencies: `pip install -r requirements.txt -r requirements-dev.txt`
6. Set up pre-commit hooks: `pre-commit install`

## Development Workflow

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Write tests for your changes
4. Run tests: `pytest`
5. Run code quality checks: `make lint`
6. Commit your changes with a descriptive message
7. Push to your fork
8. Open a Pull Request

## Code Style

We use the following tools for code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pylint**: Advanced linting

Run all checks with:
```bash
make lint
```

Or run them individually:
```bash
black app tests
isort app tests
flake8 app tests
mypy app
```

## Testing

- Write tests for all new features
- Maintain test coverage above 95%
- Run tests: `pytest`
- Check coverage: `pytest --cov=app --cov-report=html`

## Commit Messages

Follow conventional commit format:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Example: `feat: add user profile update endpoint`

## Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md with your changes
5. Request review from maintainers
6. Address review feedback
7. Once approved, your PR will be merged

## Code Review Guidelines

- Be respectful and constructive
- Focus on the code, not the person
- Explain your reasoning
- Be open to feedback

## Security

If you discover a security vulnerability, please refer to [SECURITY.md](SECURITY.md) for reporting procedures.

## Questions?

Feel free to open an issue for any questions or concerns!
