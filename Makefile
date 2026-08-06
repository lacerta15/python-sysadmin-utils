.PHONY: install dev test lint cov clean

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest -q

lint:
	flake8 sysadmin_utils --max-line-length=100

cov:
	pytest --cov=sysadmin_utils --cov-report=term-missing

clean:
	rm -rf build dist *.egg-info .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
