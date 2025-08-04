install:
	pipenv install --dev

lint:
	flake8 .

format:
	black .

test:
	pytest

precommit:
	pre-commit run --all-files

run:
	pytest tests/test_prepare_data.py tests/test_integration_training.py
