.PHONY: help install test lint clean run setup

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test: ## Run tests
	pytest -v

test-quick: ## Run tests quickly (no integration tests)
	pytest -v -m "not integration"

lint: ## Run linting
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

format: ## Format code with black
	black . --line-length=88

clean: ## Clean up cache files
	find . -type d -name __pycache__ -delete
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*.pyd" -delete
	find . -name ".coverage" -delete
	find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true

run: ## Run Lucien AI
	python Lucien.py

setup: ## Initial development setup
	python setup_dev.py
