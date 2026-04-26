# Users Service

FastAPI service for managing users.

## Endpoints

- `GET /status` - service health check
- `POST /create` - create a user
- `GET /users` - list users
- `GET /users/{user_id}` - get a user by id

## Local Run

From the parent project directory:

```powershell
uvicorn users_service.app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API docs:

```text
http://127.0.0.1:8000/docs
```

## Docker

From the `users_service` directory:

```powershell
docker build -t users-service .
docker run --rm -p 8000:8000 users-service
```

