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
- Phase 5: room management
- Phase 6: booking management
- Phase 7: file uploads
- Phase 8: authorization and roles
- Phase 9: pagination, search, filtering, and response consistency

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
UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE_MB=5
```

`APP_DEBUG` is used instead of `DEBUG` to avoid collisions with existing system environment variables.

If your database password contains special URL characters, encode them. For example, `@` becomes `%40`.

`UPLOAD_DIR` controls where files are saved locally. `MAX_UPLOAD_SIZE_MB` controls the largest accepted image upload.

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
GET /api/v1/users
GET /api/v1/users/me
GET /api/v1/users/{user_id}
GET /api/v1/properties
GET /api/v1/properties/{property_id}
POST /api/v1/properties
PUT /api/v1/properties/{property_id}
DELETE /api/v1/properties/{property_id}
GET /api/v1/rooms
GET /api/v1/rooms/{room_id}
POST /api/v1/rooms
PUT /api/v1/rooms/{room_id}
DELETE /api/v1/rooms/{room_id}
GET /api/v1/properties/{property_id}/rooms
GET /api/v1/bookings
POST /api/v1/bookings
GET /api/v1/bookings/my
DELETE /api/v1/bookings/{booking_id}
POST /api/v1/uploads/profile
POST /api/v1/uploads/properties/{property_id}
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

## User Management

Phase 8 adds admin-only user visibility.

Admin endpoints:

```http
GET /api/v1/users
GET /api/v1/users/{user_id}
```

### List Users

```bash
curl http://127.0.0.1:8000/api/v1/users \
  -H "Authorization: Bearer admin.jwt.token"
```

Response format:

```json
{
  "success": true,
  "message": "Users retrieved successfully",
  "data": [
    {
      "id": 1,
      "first_name": "Meshack",
      "last_name": "Venance",
      "email": "meshack@example.com",
      "role": "CUSTOMER",
      "status": "ACTIVE",
      "created_at": "2026-06-04T12:00:00Z",
      "updated_at": "2026-06-04T12:00:00Z"
    }
  ]
}
```

### Get User Details

```bash
curl http://127.0.0.1:8000/api/v1/users/1 \
  -H "Authorization: Bearer admin.jwt.token"
```

## Property Management

Phase 4 adds CRUD operations for accommodation properties.

Read endpoints are public:

```http
GET /api/v1/properties
GET /api/v1/properties/{property_id}
```

Write endpoints require an ADMIN bearer token:

```http
POST /api/v1/properties
PUT /api/v1/properties/{property_id}
DELETE /api/v1/properties/{property_id}
```

Customers can browse properties, but only admins can create, update, delete, or upload property images.

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
    "status": "ACTIVE",
    "created_at": "2026-06-04T12:00:00Z",
    "updated_at": "2026-06-04T12:00:00Z"
  }
}
```

### List Properties

```bash
curl "http://127.0.0.1:8000/api/v1/properties?page=1&size=10&search=hotel&location=dar&status=ACTIVE"
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
      "status": "ACTIVE",
      "created_at": "2026-06-04T12:00:00Z",
      "updated_at": "2026-06-04T12:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "size": 10,
    "total": 25,
    "pages": 3
  }
}
```

## Room Management

Phase 5 adds rooms and connects them to properties.

Each room belongs to one property:

```text
Property
└── Room
```

Read endpoints are public:

```http
GET /api/v1/rooms
GET /api/v1/rooms/{room_id}
GET /api/v1/properties/{property_id}/rooms
```

Write endpoints require an ADMIN bearer token:

```http
POST /api/v1/rooms
PUT /api/v1/rooms/{room_id}
DELETE /api/v1/rooms/{room_id}
```

Customers can browse rooms, but only admins can create, update, or deactivate rooms.

### Create Room

```bash
curl -X POST http://127.0.0.1:8000/api/v1/rooms \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your.jwt.token" \
  -d '{
    "property_id": 1,
    "room_number": "A-101",
    "room_type": "Deluxe Double",
    "price_per_night": "120.00",
    "capacity": 2,
    "availability": true
  }'
```

Response format:

```json
{
  "success": true,
  "message": "Room created successfully",
  "data": {
    "id": 1,
    "property_id": 1,
    "room_number": "A-101",
    "room_type": "Deluxe Double",
    "price_per_night": "120.00",
    "capacity": 2,
    "availability": true,
    "status": "ACTIVE",
    "created_at": "2026-06-04T12:00:00Z",
    "updated_at": "2026-06-04T12:00:00Z"
  }
}
```

### List Rooms For A Property

List all rooms with filters:

```bash
curl "http://127.0.0.1:8000/api/v1/rooms?page=1&size=10&property_id=1&room_type=deluxe&min_price=50&max_price=200&capacity=2&availability=true"
```

List rooms under one property:

```bash
curl http://127.0.0.1:8000/api/v1/properties/1/rooms
```

Response format:

```json
{
  "success": true,
  "message": "Property rooms retrieved successfully",
  "data": [
    {
      "id": 1,
      "property_id": 1,
      "room_number": "A-101",
      "room_type": "Deluxe Double",
      "price_per_night": "120.00",
      "capacity": 2,
      "availability": true,
      "status": "ACTIVE",
      "created_at": "2026-06-04T12:00:00Z",
      "updated_at": "2026-06-04T12:00:00Z"
    }
  ]
}
```

## Booking Management

Phase 6 adds customer booking workflows.

Each booking belongs to one user and one room:

```text
User
└── Booking
    └── Room
        └── Property
```

Booking endpoints are split by role:

```http
ADMIN:
  GET /api/v1/bookings

CUSTOMER:
  POST /api/v1/bookings
  GET /api/v1/bookings/my
  DELETE /api/v1/bookings/{booking_id}
```

Booking business rules:

```text
check_out must be after check_in
room must exist and be active
room must be available
room cannot be double-booked for overlapping dates
customers can only view and cancel their own bookings
cancelled bookings do not block future bookings
```

### Create Booking

```bash
curl -X POST http://127.0.0.1:8000/api/v1/bookings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your.jwt.token" \
  -d '{
    "room_id": 1,
    "check_in": "2026-06-10",
    "check_out": "2026-06-15"
  }'
```

Response format:

```json
{
  "success": true,
  "message": "Booking created successfully",
  "data": {
    "id": 1,
    "user_id": 1,
    "room_id": 1,
    "check_in": "2026-06-10",
    "check_out": "2026-06-15",
    "status": "CONFIRMED",
    "created_at": "2026-06-04T12:00:00Z",
    "updated_at": "2026-06-04T12:00:00Z"
  }
}
```

### List My Bookings

```bash
curl "http://127.0.0.1:8000/api/v1/bookings/my?page=1&size=10&status=CONFIRMED" \
  -H "Authorization: Bearer your.jwt.token"
```

### List All Bookings

Admin only:

```bash
curl "http://127.0.0.1:8000/api/v1/bookings?page=1&size=10&status=CONFIRMED&user_id=1&room_id=1" \
  -H "Authorization: Bearer admin.jwt.token"
```

### Cancel Booking

```bash
curl -X DELETE http://127.0.0.1:8000/api/v1/bookings/1 \
  -H "Authorization: Bearer your.jwt.token"
```

## File Uploads

Phase 7 adds image uploads for user profiles and properties.

Upload endpoints are split by role:

```http
AUTHENTICATED USER:
  POST /api/v1/uploads/profile

ADMIN:
  POST /api/v1/uploads/properties/{property_id}
```

Accepted image types:

```text
jpg
jpeg
png
webp
```

Uploaded files are saved inside the local `uploads/` directory. The database stores the public URL path, for example `/uploads/profiles/user-1-image.png`.

FastAPI serves saved files from:

```text
http://127.0.0.1:8000/uploads/...
```

### Upload Profile Image

```bash
curl -X POST http://127.0.0.1:8000/api/v1/uploads/profile \
  -H "Authorization: Bearer your.jwt.token" \
  -F "file=@avatar.png"
```

Response format:

```json
{
  "success": true,
  "message": "Profile image uploaded successfully",
  "data": {
    "url": "/uploads/profiles/user-1-abc123.png"
  }
}
```

### Upload Property Image

```bash
curl -X POST http://127.0.0.1:8000/api/v1/uploads/properties/1 \
  -H "Authorization: Bearer admin.jwt.token" \
  -F "file=@property.png"
```

Response format:

```json
{
  "success": true,
  "message": "Property image uploaded successfully",
  "data": {
    "url": "/uploads/properties/property-1-abc123.png"
  }
}
```

## PostgreSQL Setup

Make sure PostgreSQL is running and create the database used in `.env`:

```sql
CREATE DATABASE stayease_db;
```

Then confirm your `.env` connection string matches your local PostgreSQL username, password, host, port, and database name.

## Database Migrations

This project uses Alembic for production-style database migrations.

FastAPI no longer creates tables on startup. Models define the database shape, and Alembic applies that shape to PostgreSQL.

Spring Boot comparison:

```text
SQLAlchemy models      JPA @Entity
Alembic migrations     Flyway / Liquibase migrations
alembic upgrade head   apply pending migrations
```

Apply migrations:

```bash
make migrate
```

Create a new migration after changing models:

```bash
make migration message="describe your schema change"
```

Rollback the last migration:

```bash
make rollback
```

Direct Alembic commands also work:

```bash
venv/bin/python -m alembic upgrade head
venv/bin/python -m alembic revision --autogenerate -m "describe your schema change"
venv/bin/python -m alembic downgrade -1
```

Important: after changing models, do not expect FastAPI to update existing tables automatically. Generate and apply an Alembic migration.

If your local database already has tables that were created by the old `Base.metadata.create_all()` startup code, use one of these learning-friendly options:

```text
Fresh dev database: drop/recreate the database, then run make migrate.
Existing matching schema: run alembic stamp head to mark the current schema as migrated.
Existing old schema: create/apply a migration that alters the old tables.
```

For this project, the simplest learning path is usually a fresh local database, then:

```bash
make migrate
```

## Useful Commands

If using the included `Makefile`:

```bash
make dev
make install
make check
make migrate
make migration message="describe your schema change"
make rollback
```

What they do:

```text
make dev      starts the development server with reload
make install  installs Python dependencies
make check    compile-checks the app package
make migrate  applies pending Alembic migrations
make migration creates a new Alembic migration from model changes
make rollback rolls back the previous Alembic migration
```

## Phase 2 Learning Notes

`app/core/config.py` loads settings from `.env` into a typed `Settings` object. This is similar to Spring Boot configuration properties.

`app/core/database.py` creates the SQLAlchemy engine and session factory. The engine knows how to connect to PostgreSQL. The session represents a unit of database work.

`get_db()` is a FastAPI dependency. It gives a route a database session and closes it when the request is finished. In Spring Boot, much of this session lifecycle is handled automatically.

`alembic/env.py` connects Alembic to the same `DATABASE_URL` used by FastAPI and points Alembic at `Base.metadata` so migrations can read SQLAlchemy models.

## Phase 3 Learning Notes

`app/models/user.py` defines the SQLAlchemy `User` model. This is similar to a Spring Boot `@Entity`.

`app/schemas/user.py` and `app/schemas/auth.py` define request and response schemas. These are similar to DTOs.

`app/services/user_service.py` contains user database logic such as creating a user and checking login credentials.

`app/core/security.py` handles password hashing and JWT tokens. This is similar to a small `PasswordEncoder` plus JWT utility.

`app/dependencies/auth.py` contains `get_current_user()`. This is a route guard: it reads the bearer token, decodes it, loads the user, and rejects the request if the token is invalid.

The protected route flow is:

```text
Request with Authorization header
-> HTTPBearer extracts token
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

## Phase 5 Learning Notes

`app/models/room.py` defines the SQLAlchemy `Room` model. This is similar to a Spring Boot `@Entity`.

`Room.property_id` is a foreign key to `Property.id`. This creates the database relationship between rooms and properties.

`app/schemas/room.py` defines room request and response schemas. These are similar to DTOs.

`app/services/room_service.py` contains room database logic such as validating the parent property, creating rooms, updating rooms, and soft-deleting rooms.

`app/routers/rooms.py` contains room HTTP endpoints. It also adds `GET /api/v1/properties/{property_id}/rooms` because customers naturally browse rooms under a property.

The room flow is:

```text
Request
-> room router
-> get_db dependency provides a database session
-> room service validates property/room rules
-> route returns the standard API response
```

## Phase 6 Learning Notes

`app/models/booking.py` defines the SQLAlchemy `Booking` model. This is similar to a Spring Boot `@Entity`.

`Booking.user_id` is a foreign key to `User.id`, and `Booking.room_id` is a foreign key to `Room.id`.

`app/schemas/booking.py` defines booking request and response schemas. These are similar to DTOs.

`app/services/booking_service.py` contains booking business logic, including date validation, overlap checks, room availability checks, and ownership checks.

`app/routers/bookings.py` contains booking HTTP endpoints. All booking routes require authentication because bookings belong to customers.

The booking flow is:

```text
Request with Authorization header
-> get_current_user validates JWT
-> booking router receives current_user
-> booking service validates dates, room, overlap, and ownership
-> route returns the standard API response
```

## Phase 7 Learning Notes

`UploadFile` is FastAPI's file-upload type. It is similar to receiving a `MultipartFile` in Spring Boot.

`File(...)` tells FastAPI that the request body is multipart form data, not JSON.

`app/services/upload_service.py` keeps upload validation and file saving outside the router. This is the same reason Spring Boot projects usually keep business logic out of controllers.

The upload service validates file type, extension, and size before saving the file. This keeps bad uploads from reaching storage.

`app.main` mounts `StaticFiles` at `/uploads`. This is similar to serving static resources in Spring Boot, but here we wire it explicitly.

The upload flow is:

```text
Request with Authorization header and multipart file
-> get_current_user validates JWT
-> upload router receives UploadFile
-> upload service validates and saves the file
-> database stores the public file URL
-> route returns the standard API response
```

## Phase 8 Learning Notes

Authentication checks who the user is. Authorization checks what that user is allowed to do.

Spring Boot comparison:

```text
FastAPI dependency guard     Spring Security @PreAuthorize / role check
require_admin                hasRole("ADMIN")
require_customer             hasRole("CUSTOMER")
```

`app/dependencies/auth.py` now has reusable role guards. Each guard first depends on `get_current_user()`, so the route gets both authentication and authorization in one dependency.

The admin authorization flow is:

```text
Request with Authorization header
-> get_current_user validates JWT
-> require_admin checks current_user.role
-> route runs only when the user is ADMIN
```

The customer authorization flow is:

```text
Request with Authorization header
-> get_current_user validates JWT
-> require_customer checks current_user.role
-> booking service still checks ownership using current_user.id
```

Role rules added in Phase 8:

```text
ADMIN:
  manage properties
  manage rooms
  upload property images
  view all bookings
  view users

CUSTOMER:
  create bookings
  view own bookings
  cancel own bookings
```

## Phase 9 Learning Notes

Phase 9 improves API usability when tables grow.

Pagination works through a reusable dependency:

```text
GET /api/v1/properties?page=1&size=10
```

Spring Boot comparison:

```text
FastAPI pagination dependency     Spring Pageable
PaginationParams                  Pageable
PaginationMeta                    Page metadata
```

The paginated response shape is:

```json
{
  "success": true,
  "message": "Request completed successfully",
  "data": [],
  "pagination": {
    "page": 1,
    "size": 10,
    "total": 25,
    "pages": 3
  }
}
```

Search and filters were added to list endpoints:

```http
GET /api/v1/properties?search=hotel&location=dar&status=ACTIVE&page=1&size=10
GET /api/v1/rooms?property_id=1&room_type=deluxe&min_price=50&max_price=200&capacity=2&availability=true&page=1&size=10
GET /api/v1/bookings?status=CONFIRMED&user_id=1&room_id=1&page=1&size=10
GET /api/v1/bookings/my?status=CONFIRMED&page=1&size=10
```

Error responses now use the same top-level envelope as successful responses:

```json
{
  "success": false,
  "message": "Room not found",
  "data": null
}
```

This is similar to using a Spring Boot `@ControllerAdvice` to standardize errors across custom exceptions, framework HTTP exceptions, and validation failures.

## Next Phase

Phase 10 will add deployment:

- Docker
- PostgreSQL environment setup
- Production startup command
- Render or Railway deployment workflow
