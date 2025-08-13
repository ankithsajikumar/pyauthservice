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
  - `POST /api/users/` — Create user  
  - `GET /api/users/<id>/` — Retrieve user  
  - `PUT/PATCH /api/users/<id>/` — Update user  
  - `DELETE /api/users/<id>/` — Delete user  

- **JWT Authentication:**  
  - `POST /api/token/` — Obtain JWT token  
  - `POST /api/token/refresh/` — Refresh JWT token  

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