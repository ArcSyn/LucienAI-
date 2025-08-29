# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in LucienAI, please follow these steps:

1. **Do not create a public GitHub issue** for the vulnerability
2. **Email the details to** the maintainer at [maintainer-email]
3. **Include the following information:**
   - Description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact
   - Suggested fix (if any)

## Security Best Practices

### For Users
- **Never commit API keys** to version control
- Use environment variables for sensitive configuration
- Keep dependencies updated
- Run LucienAI in a controlled environment

### For Developers
- Follow secure coding practices
- Validate all user inputs
- Use HTTPS for API communications
- Implement proper error handling
- Avoid logging sensitive information

### Environment Variables
Always use environment variables for sensitive data:

```bash
# Good
export GROQ_API_KEY="your-secret-key"

# Bad - never do this
GROQ_API_KEY="your-secret-key"  # in code
```

### API Key Management
- Store API keys in `.env` files (not committed to git)
- Use different keys for development and production
- Rotate keys regularly
- Monitor API usage for unusual activity

## Response Timeline

- **Initial response**: Within 48 hours
- **Status update**: Within 1 week
- **Fix release**: Within 30 days (depending on severity)

## Acknowledgments

We appreciate security researchers who responsibly disclose vulnerabilities.
