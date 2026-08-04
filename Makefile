.PHONY: install migrate seed run test compile

install:
	python -m pip install -e '.[dev]'

migrate:
	alembic upgrade head

seed:
	python scripts/seed_admin.py

run:
	uvicorn app.main:app --reload

test:
	python -m pytest

compile:
	python -m compileall app tests main.py alembic scripts
