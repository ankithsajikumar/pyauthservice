# PyAuthService

A Django-based authentication service providing SSO (Single Sign-On) and user management APIs, supporting both OAuth2 and JWT authentication.

---

## Features

- Custom user model
- User management API (CRUD)
- OAuth2 and JWT authentication support
- Admin interface

---

## Getting Started

### 1. Clone the repository

```sh
git clone https://github.com/ankithsajikumar/pyauthservice.git
cd pyauthservice
```

### 2. Set up a virtual environment

```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. Install requirements

```sh
pip install -r requirements.txt
```

### 4. Apply migrations

```sh
python manage.py migrate
```

### 5. Create a superuser

```sh
python manage.py createsuperuser
```

### 6. Run the development server

```sh
python manage.py runserver
```

### MISC: Deactivate venv

```sh
deactivate
```

### MISC: Store dependencies

```sh
pip freeze > requirements.txt
```

---

## API Endpoints

- **Root Redirect:**  
  - `GET /` — Redirects to the configured `HOME_URL`  
    ```sh
    curl -v https://domain/
    ```
    > You will receive an HTTP 302 redirect to the URL set as `HOME_URL`.

- **User Management:**  
  - `GET /api/users/` — List users  
    ```sh
    curl -H "Authorization: Bearer <access_token>" https://domain/api/users/
    ```
  - `POST /api/users/` — Create user  
    ```sh
    curl -X POST https://domain/api/users/ \
      -H "Content-Type: application/json" \
      -d '{
        "username": "newuser",
        "password": "newpassword",
        "email": "newuser@example.com",
        "first_name": "First Name",
        "last_name": "Last Name"
      }'
    ```
    > Only staff users can set `is_staff` or `is_active` fields. Required fields are `username`, `password`, `email`.

  - `GET /api/users/<id>/` — Retrieve user  
    ```sh
    curl -H "Authorization: Bearer <access_token>" https://domain/api/users/1/
    ```
  - `PUT/PATCH /api/users/<id>/` — Update user  
    ```sh
    curl -X PATCH https://domain/api/users/1/ \
      -H "Authorization: Bearer <access_token>" \
      -H "Content-Type: application/json" \
      -d '{"first_name": "UpdatedName"}'
    ```
  - `DELETE /api/users/<id>/` — Delete user  
    ```sh
    curl -X DELETE https://domain/api/users/1/ \
      -H "Authorization: Bearer <access_token>"
    ```

  - `GET /auth/me/` — Get current authenticated user's info  
    ```sh
    curl -H "Authorization: Bearer <access_token>" https://domain/auth/me/
    ```
    > Returns the authenticated user's details.

- **JWT Authentication:**  
  - `POST /api/token/` — Obtain JWT token  
    ```sh
    curl -X POST https://domain/api/token/ \
      -H "Content-Type: application/json" \
      -d '{"username": "youruser", "password": "yourpassword"}'
    ```
  - `POST /api/token/refresh/` — Refresh JWT token  
    ```sh
    curl -X POST https://domain/api/token/refresh/ \
      -H "Content-Type: application/json" \
      -d '{"refresh": "<your_refresh_token>"}'
    ```

- **OAuth2:**  
  - `/o/` — OAuth2 endpoints (see [django-oauth-toolkit docs](https://django-oauth-toolkit.readthedocs.io/en/latest/))

- **Status:**  
  - `GET /api/status/` — Server status (requires service token)  
    ```sh
    curl -H "<service_api_token_key>: <service_api_token>" https://domain/api/status/
    ```
    > Returns:  
    > `{ "status": "ok", "service": "pyauthservice" }`  
    >  
    > Use the value of `SERVICE_API_TOKEN` as `<service_api_token>`.

---

## Authentication

- **JWT:**  
  Obtain a token via `/api/token/` and use it in the `Authorization` header:  
  ```
  Authorization: Bearer <access_token>
  ```

- **OAuth2:**  
  Standard OAuth2 flows are available at `/o/`.

---

## Useful Django Commands

- Run development server:  
  `python manage.py runserver`
- Make migrations:  
  `python manage.py makemigrations`
- Apply migrations:  
  `python manage.py migrate`
- Create superuser:  
  `python manage.py createsuperuser`
- Open Django shell:  
  `python manage.py shell`
- Collect static files:  
  `python manage.py collectstatic`

---

## Project Structure

```
pyauthservice/
├── manage.py
├── requirements.txt
├── README.md
├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
└── pyauthservice/
    ├── settings.py
    ├── urls.py
    └── ...
```

---

## Environment Variables (`.env`)

This project uses a `.env` file to manage sensitive settings and environment-specific configuration.  
Create a `.env` file in your project root (same directory as `manage.py`) with the following variables:

| Variable             | Description                                      |
|----------------------|--------------------------------------------------|
| `SECRET_KEY`         | Django secret key for cryptographic signing      |
| `DEBUG`              | Set to `True` for development, `False` for prod  |
| `SERVICE_API_TOKEN`  | Token required for accessing special endpoints   |

**Example `.env` file:**
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
SERVICE_API_TOKEN=your-status-api-token
```

> **Note:** Never commit your `.env` file with real secrets to version control. Use `.env.example` as a template.

---

### GitHub Actions Deploy Prerequisites

Before running the deploy workflow, set the following in your repository:

#### Repository Variables (`Settings > Variables > Actions`)
- `CONSOLE_USER_ID`: PythonAnywhere username
- `SERVICE_API_TOKEN_KEY`: The header key for your status API token

#### Repository Secrets (`Settings > Secrets > Actions`)
- `CONSOLE_API_KEY`: PythonAnywhere API token (get from your PythonAnywhere account)
- `SERVICE_API_TOKEN`: The value of your status API token (should match `SERVICE_API_TOKEN` in your `.env` and Django settings)

These are required for the workflow to authenticate with PythonAnywhere and to check your server

## License

MIT License