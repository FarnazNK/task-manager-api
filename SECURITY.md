# Security Policy

## Security Features

This project implements multiple layers of security:

### Authentication & Authorization
- **JWT-based authentication** with configurable token expiration
- **Bcrypt password hashing** with automatic salt generation
- **Strong password requirements**: minimum 8 characters, uppercase, lowercase, numbers, and special characters
- **User-specific data isolation**: Users can only access their own data

### Input Validation
- **Pydantic models** for request validation
- **SQL injection prevention** through SQLAlchemy ORM with parameterized queries
- **XSS prevention** through proper output encoding
- **Type safety** with Python type hints and mypy validation

### Security Headers
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`

### Infrastructure Security
- **Docker security**: Non-root user in containers
- **CORS configuration**: Configurable allowed origins
- **Trusted host middleware**: Protection against host header attacks
- **Rate limiting**: Protection against brute force attacks (configurable)
- **Database connection pooling**: Prevents connection exhaustion

### Dependency Security
- **Automated security scanning** with Bandit and Safety in CI/CD
- **Regular dependency updates** through Dependabot
- **Minimal Docker image** based on python:3.11-slim

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by:

1. **Email**: security@yourcompany.com
2. **Do NOT** open a public issue
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and provide a timeline for a fix.

## Security Best Practices for Deployment

### Environment Variables
- **Never commit** `.env` files to version control
- Use strong, randomly generated `SECRET_KEY` (minimum 32 characters)
- Generate secure key: `openssl rand -hex 32`
- Use different keys for different environments

### Database
- Use strong database passwords
- Enable SSL/TLS for database connections in production
- Regular backups with encryption
- Implement database access controls

### HTTPS
- **Always use HTTPS** in production
- Configure proper SSL/TLS certificates
- Enable HTTP Strict Transport Security (HSTS)
- Consider using services like Let's Encrypt

### Docker
- Scan images for vulnerabilities: `docker scan task-manager-api`
- Use specific version tags, not `latest`
- Regular updates of base images
- Implement resource limits

### Monitoring
- Enable application logging
- Monitor for suspicious activities
- Set up alerts for security events
- Regular security audits

### Access Control
- Implement principle of least privilege
- Use separate service accounts for different environments
- Regular password rotation policies
- Enable 2FA where possible

### API Security
- Implement rate limiting in production
- Use API keys for service-to-service communication
- Regular security penetration testing
- Keep dependencies up to date

## Security Checklist for Production

- [ ] Change default `SECRET_KEY` to a strong random value
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Configure CORS with specific allowed origins
- [ ] Set up proper database access controls
- [ ] Enable rate limiting
- [ ] Implement proper logging and monitoring
- [ ] Regular security updates and patches
- [ ] Regular backup procedures
- [ ] Security testing (SAST, DAST)
- [ ] Incident response plan

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Security Updates

Security updates are released as soon as possible after discovery. Subscribe to releases to stay informed.
