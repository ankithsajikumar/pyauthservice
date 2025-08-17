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

## License

MIT License