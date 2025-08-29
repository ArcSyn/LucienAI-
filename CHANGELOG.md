# Changelog

All notable changes to LucienAI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Command router system with decorator-based registration
- Memory persistence with JSON storage
- File operations (list, read, write, delete)
- System operations (disk space, CPU usage, shell commands)
- AI integration with Groq and Ollama
- Development tooling (Makefile, setup script, CI/CD)
- Docker support for containerized development
- Comprehensive test suite with graceful service skipping
- Pre-commit hooks for code quality
- VSCode configuration for development

### Changed
- Refactored command handling to use router pattern
- Improved error handling for API calls
- Enhanced test coverage and organization

### Fixed
- Removed dead code from old command handling
- Fixed indentation and syntax issues
- Improved environment variable handling

## [0.1.0] - 2025-01-XX

### Added
- Initial release of LucienAI
- Basic AI chat functionality
- Core file and system operations
- Memory management system
