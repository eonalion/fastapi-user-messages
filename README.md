# About
This is a simple FastAPI application that allows user and message management.
It supports CRUD operations for users and messages and getting messages sent by a specific user.

# Running in Docker
With `docker` installed, run the following commands in the root directory of the project:

```bash
docker build -t fastapi-user-messages .
docker run -d -p 8000:8000 fastapi-user-messages
```
Application will be available at http://localhost:8000.  
Swagger UI will be available at http://localhost:8000/docs.

# Local Development
`./scripts/local.sh` is a script that helps with developing and running the application locally.  
All commands are executed in the virtual environment created by the script.

To run the application locally, execute the following command:
```bash
./scripts/local.sh run
```

To run tests, execute the following command:
```bash
./scripts/local.sh test
```

To run linting and formatting, execute the following command:
```bash
./scripts/local.sh lint
```

To clean up the virtual environment separately, execute the following command:
```bash
./scripts/local.sh clean
```

You can combine multiple commands and run them at once:
```bash
./scripts/local.sh lint test run
```

# Available Endpoints

- GET    `/api/users/` - *Get users with limit.*
- POST   `/api/users/` - *Create user.*
- GET    `/api/users/{email}` - *Get user by email.*
- PATCH  `/api/users/{user_id}` - *Partially update user.*
- DELETE `/api/users/{user_id}` - *Delete user (and all related messages).*
- GET    `/api/users/{user_id}/messages/` - *Get messages sent by a specific user.*
- POST   `/api/users/{user_id}/messages/{message_id}` - *Update message sent by a specific user.*
- DELETE `/api/users/{user_id}/messages/{message_id}` - *Delete message sent by a specific user.*

# Project structure
All application logic resides in the `app` directory. The structure of the `app` directory is following:

```
app
|-- api                  - api related logic.
|   |-- dependencies.py  - dependencies for endpoints definition.
|   |-- routes           - api routes.
|-- core                 - application configuration, middleware, exception handlers,
|                          constants and other core logic.
|-- models               - SQLmodel models for this application.
|-- services             - business logic combined with crud operations.
|-- tests                - unit tests for the application.
|-- database.py          - database configuration and session management.
|-- main.py              - FastAPI application creation and configuration.
```

`scripts` folder contains scripts for local development and potentially for CI/CD pipelines.
