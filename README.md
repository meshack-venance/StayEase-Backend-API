# StayEase API

StayEase API is a learning-focused FastAPI backend for an accommodation booking platform. Customers will be able to view properties, view rooms, create bookings, and manage their own bookings. Admins will manage properties, rooms, bookings, and users.

The project is being built in phases so the design grows like a real backend system: requirements first, then foundation, database, authentication, business features, authorization, and deployment.

## Current Phase

The project currently covers:

- Phase 0: system design and requirements
- Phase 1: FastAPI project foundation
- Phase 2: database and configuration setup
- Phase 3: user management and JWT authentication
- Phase 4: property management

## Tech Stack

- FastAPI for the web API
- Uvicorn / FastAPI CLI for running the app
- Pydantic Settings for typed environment configuration
- SQLAlchemy for database connection and ORM foundation
- PostgreSQL as the database
- Passlib and bcrypt for password hashing
- PyJWT for access tokens

## Project Structure

```text
stayease-api/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
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
app/core/security.py        PasswordEncoder / JWT utility
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
SECRET_KEY=change-this-secret-key-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

`APP_DEBUG` is used instead of `DEBUG` to avoid collisions with existing system environment variables.

If your database password contains special URL characters, encode them. For example, `@` becomes `%40`.

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
POST /api/v1/auth/register
POST /api/v1/auth/login
GET /api/v1/users/me
GET /api/v1/properties
GET /api/v1/properties/{property_id}
POST /api/v1/properties
PUT /api/v1/properties/{property_id}
DELETE /api/v1/properties/{property_id}
```

`GET /health/database` runs a simple `SELECT 1` query to confirm that PostgreSQL is reachable.

If PostgreSQL is not running or the database credentials are wrong, this endpoint returns `503 Service Unavailable`.

## User Authentication

Phase 3 adds user registration, login, password hashing, JWT authentication, and a protected current-user endpoint.

### Register

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Meshack",
    "last_name": "Venance",
    "email": "meshack@example.com",
    "password": "password123"
  }'
```

The API stores a hashed password. It does not return the password in the response.

### Login

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "meshack@example.com",
    "password": "password123"
  }'
```

Response:

```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "your.jwt.token",
    "token_type": "bearer"
  }
}
```

### Get Current User

Use the token from login:

```bash
curl http://127.0.0.1:8000/api/v1/users/me \
  -H "Authorization: Bearer your.jwt.token"
```

## Property Management

Phase 4 adds CRUD operations for accommodation properties.

Read endpoints are public:

```http
GET /api/v1/properties
GET /api/v1/properties/{property_id}
```

Write endpoints require a bearer token:

```http
POST /api/v1/properties
PUT /api/v1/properties/{property_id}
DELETE /api/v1/properties/{property_id}
```

Admin-only role checks are intentionally left for Phase 8. For now, Phase 4 teaches CRUD structure and authenticated write operations.

### Create Property

```bash
curl -X POST http://127.0.0.1:8000/api/v1/properties \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your.jwt.token" \
  -d '{
    "name": "StayEase City Hotel",
    "description": "Modern hotel near the city center with free Wi-Fi.",
    "location": "Dar es Salaam, Tanzania",
    "rating": "4.5"
  }'
```

Response format:

```json
{
  "success": true,
  "message": "Property created successfully",
  "data": {
    "id": 1,
    "name": "StayEase City Hotel",
    "description": "Modern hotel near the city center with free Wi-Fi.",
    "location": "Dar es Salaam, Tanzania",
    "rating": "4.5",
    "created_at": "2026-06-04T12:00:00Z"
  }
}
```

### List Properties

```bash
curl http://127.0.0.1:8000/api/v1/properties
```

Response format:

```json
{
  "success": true,
  "message": "Properties retrieved successfully",
  "data": [
    {
      "id": 1,
      "name": "StayEase City Hotel",
      "description": "Modern hotel near the city center with free Wi-Fi.",
      "location": "Dar es Salaam, Tanzania",
      "rating": "4.5",
      "created_at": "2026-06-04T12:00:00Z"
    }
  ]
}
```

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

## Phase 3 Learning Notes

`app/models/user.py` defines the SQLAlchemy `User` model. This is similar to a Spring Boot `@Entity`.

`app/schemas/user.py` and `app/schemas/auth.py` define request and response schemas. These are similar to DTOs.

`app/services/user_service.py` contains user database logic such as creating a user and checking login credentials.

`app/core/security.py` handles password hashing and JWT tokens. This is similar to a small `PasswordEncoder` plus JWT utility.

`app/dependencies/auth.py` contains `get_current_user()`. This is a route guard: it reads the bearer token, decodes it, loads the user, and rejects the request if the token is invalid.

The protected route flow is:

```text
Request with Authorization header
-> OAuth2PasswordBearer extracts token
-> get_current_user decodes JWT
-> user is loaded from PostgreSQL
-> route receives current_user
```

## Phase 4 Learning Notes

`app/models/property.py` defines the SQLAlchemy `Property` model. This is similar to a Spring Boot `@Entity`.

`app/schemas/property.py` defines property request and response schemas. These are similar to DTOs.

`app/services/property_service.py` contains property database logic such as fetching, creating, updating, and deleting properties.

`app/routers/properties.py` contains the property HTTP endpoints. This is similar to a Spring Boot `@RestController`.

The property flow is:

```text
Request
-> property router
-> get_db dependency provides a database session
-> property service runs SQLAlchemy logic
-> route returns the standard API response
```

For write operations:

```text
Request with Authorization header
-> get_current_user validates JWT
-> property service performs create/update/delete
```

## Next Phase

Phase 5 will add room management:

- Room model
- Room schemas
- Room service
- Room CRUD routes
- Relationship between rooms and properties
- Admin-only protection later in Phase 8
