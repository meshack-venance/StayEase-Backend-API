.PHONY: dev install check migrate migration rollback

dev:
	venv/bin/uvicorn app.main:app --reload

install:
	venv/bin/python -m pip install -r requirements.txt

check:
	venv/bin/python -m compileall app

migrate:
	venv/bin/python -m alembic upgrade head

migration:
	venv/bin/python -m alembic revision --autogenerate -m "$(message)"

rollback:
	venv/bin/python -m alembic downgrade -1
