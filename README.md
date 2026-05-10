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
Copy-Item .env.example .env
docker compose up --build
```

The users nginx will be available at `http://localhost:8080/users/`.
