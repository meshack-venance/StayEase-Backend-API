.PHONY: dev install check migrate migration rollback

# Start the FastAPI development server with auto-reload.
dev:
	venv/bin/uvicorn app.main:app --reload

# Install project dependencies into the virtual environment.
install:
	venv/bin/python -m pip install -r requirements.txt

# Compile-check Python files without starting the API server.
check:
	venv/bin/python -m compileall app

# Apply all pending Alembic migrations to the configured database.
migrate:
	venv/bin/python -m alembic upgrade head

# Generate a new Alembic migration from SQLAlchemy model changes.
migration:
	venv/bin/python -m alembic revision --autogenerate -m "$(message)"

# Roll back the most recent Alembic migration.
rollback:
	venv/bin/python -m alembic downgrade -1
