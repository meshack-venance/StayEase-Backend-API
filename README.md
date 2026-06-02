# StayEase API

StayEase API is a learning-focused FastAPI backend for an accommodation booking platform. Customers will be able to view properties, view rooms, create bookings, and manage their own bookings. Admins will manage properties, rooms, bookings, and users.

The project is being built in phases so the design grows like a real backend system: requirements first, then foundation, database, authentication, business features, authorization, and deployment.

## Current Phase

The project currently covers:

- Phase 0: system design and requirements
- Phase 1: FastAPI project foundation
- Phase 2: database and configuration setup

## Tech Stack

- FastAPI for the web API
- Uvicorn / FastAPI CLI for running the app
- Pydantic Settings for typed environment configuration
- SQLAlchemy for database connection and ORM foundation
- PostgreSQL as the database

## Project Structure

```text
stayease-api/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   ├── services/
│   └── dependencies/
├── tests/
├── uploads/
├── .env
├── requirements.txt
└── README.md
```

## FastAPI vs Spring Boot Mapping

If you know Spring Boot, these are the rough equivalents:

```text
FastAPI                     Spring Boot
app/main.py                 Main application class / controllers entrypoint
.env                        application.properties / application.yml
app/core/config.py          @ConfigurationProperties
app/core/database.py        DataSource / EntityManager setup
routers/                    @RestController classes
services/                   @Service classes
models/                     @Entity classes
schemas/                    DTOs / request and response classes
dependencies/               reusable injected dependencies and route guards
```

FastAPI gives you less automatic setup than Spring Boot. That is useful for learning because you can see how configuration, database sessions, and request dependencies are wired together.

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/stayease_db
APP_NAME=StayEase API
APP_VERSION=1.0.0
APP_DEBUG=True
```

`APP_DEBUG` is used instead of `DEBUG` to avoid collisions with existing system environment variables.

## Install Dependencies

Create and activate a virtual environment if you do not already have one:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

Recommended FastAPI CLI command:

```bash
fastapi dev app/main.py
```

Classic Uvicorn command:

```bash
uvicorn app.main:app --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

## Available Endpoints

```http
GET /
GET /health
GET /health/database
```

`GET /health/database` runs a simple `SELECT 1` query to confirm that PostgreSQL is reachable.

If PostgreSQL is not running or the database credentials are wrong, this endpoint returns `503 Service Unavailable`.

## PostgreSQL Setup

Make sure PostgreSQL is running and create the database used in `.env`:

```sql
CREATE DATABASE stayease_db;
```

Then confirm your `.env` connection string matches your local PostgreSQL username, password, host, port, and database name.

## Useful Commands

If using the included `Makefile`:

```bash
make dev
make install
make check
```

What they do:

```text
make dev      starts the development server with reload
make install  installs Python dependencies
make check    compile-checks the app package
```

## Phase 2 Learning Notes

`app/core/config.py` loads settings from `.env` into a typed `Settings` object. This is similar to Spring Boot configuration properties.

`app/core/database.py` creates the SQLAlchemy engine and session factory. The engine knows how to connect to PostgreSQL. The session represents a unit of database work.

`get_db()` is a FastAPI dependency. It gives a route a database session and closes it when the request is finished. In Spring Boot, much of this session lifecycle is handled automatically.

## Next Phase

Phase 3 will add user management:

- User model
- Register endpoint
- Login endpoint
- Password hashing
- JWT authentication
- `GET /users/me`
