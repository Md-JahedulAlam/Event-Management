# Event Management

A Django REST Framework backend for an event booking/management system — handles event listings, categories, ticket bookings (with QR code generation), and JWT-based authentication.

**Repository:** https://github.com/Md-JahedulAlam/Event-Management
**Live API:** https://event-management-m58t.onrender.com/

## Tech Stack

- **Django 6.1.1** — core web framework
- **Django REST Framework 3.18.1** — RESTful API layer
- **djangorestframework-simplejwt** + **PyJWT** — JWT authentication
- **django-cors-headers** — CORS support for frontend integration
- **django-filter** — queryset filtering/search/ordering
- **Pillow** + **django-cleanup** — image uploads with automatic cleanup of orphaned files
- **psycopg2-binary** — PostgreSQL driver (for production use)
- **qrcode** — QR code generation for booking tickets
- **gunicorn** + **whitenoise** — production server & static file serving

---

## 1. Project Setup

### Prerequisites
- Python 3.x
- pip

### Steps

```bash
# Clone the repository
git clone https://github.com/Md-JahedulAlam/Event-Management.git
cd Event-Management

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Move into the Django project directory
cd event_management

# Apply migrations
python manage.py migrate

# Create a superuser (for /admin/ access)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

The API is served at `http://127.0.0.1:8000/`. The Django admin panel is available at `/admin/`.

> Note: as shipped, the project uses **SQLite** (`db.sqlite3`) by default, so no external database setup is required to run it locally.

---

## 2. API Endpoints

Base path (local): `http://127.0.0.1:8000/`
Base path (live): `https://event-management-m58t.onrender.com/`

### Auth (`/auth/`)

| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| POST | `/auth/register/` | Register a new user (`username`, `email`, `phone_number`, `password`) | No |
| POST | `/auth/login/` | Obtain JWT access + refresh tokens | No |

### Categories (`/category/`) — via DRF router

| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| GET | `/category/` | List all categories | No |
| POST | `/category/` | Create a category | Yes (admin) |
| GET | `/category/{id}/` | Retrieve a category | No |
| PUT/PATCH | `/category/{id}/` | Update a category | Yes (admin) |
| DELETE | `/category/{id}/` | Delete a category | Yes (admin) |

### Events (`/event/`) — via DRF router

| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| GET | `/event/` | List events (upcoming only for non-staff users). Supports `?category=<id>`, `?search=<title>`, `?ordering=price` / `?ordering=event_date` | No |
| POST | `/event/` | Create an event (title, description, category, location, date, time, seats, price, image) | Yes (admin) |
| GET | `/event/{id}/` | Retrieve a single event | No |
| PUT/PATCH | `/event/{id}/` | Update an event | Yes (admin) |
| DELETE | `/event/{id}/` | Delete an event | Yes (admin) |

### Bookings

| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| GET | `/bookings/` | List all bookings | Yes |
| POST | `/bookings/` | Book tickets for an event (`event`, `number_of_tickets`) — generates a QR code and decrements available seats | Yes |
| PATCH | `/bookings/{booking_id}/status/` | Update a booking | Yes |
| GET | `/my-bookings/` | List the logged-in user's own bookings. Supports `?event=<id>`, `?number_of_tickets=<n>` | Yes |
| DELETE | `/my-bookings/{booking_id}/cancel/` | Cancel a booking and restore available seats | Yes |

### Admin

| Method | Endpoint | Description |
|---|---|---|
| — | `/admin/` | Django admin panel |

---

## 3. Authentication Flow

Authentication is JWT-based, via **djangorestframework-simplejwt**.

1. **Register** — `POST /auth/register/` with `username`, `email`, `phone_number`, `password`. Users are created with `role = "user"` by default (an `"admin"` role also exists on the `User` model).
2. **Login** — `POST /auth/login/` with `email` and `password` returns an `access` and a `refresh` token. The access token embeds custom claims: `user_id`, `email`, `phone_number`, and `role`.
3. **Authenticated requests** — send the access token as a header on protected endpoints:
   ```
   Authorization: Bearer <access_token>
   ```
4. **Token lifetime** — both access and refresh tokens are currently configured to expire after **7 days** (`SIMPLE_JWT` in `settings.py`).
5. **Permissions**:
   - `IsAdminOrReadOnly` (used on Category/Event): anyone can `GET`; write operations require an authenticated staff user with `role = "admin"`.
   - `IsAuthenticated` (used on all Booking endpoints): requires a logged-in user.

> ⚠️ As currently implemented, the project does **not** expose a `/auth/refresh/` endpoint (SimpleJWT's `TokenRefreshView` isn't wired into `urls.py`), so clients can't refresh an expired access token without logging in again — worth adding if you extend this project.

---

## 4. Environment Variables

As shipped, the project **does not read any environment variables** — `SECRET_KEY`, `DEBUG`, and the database configuration are hardcoded directly in `event_management/settings.py`, and it currently defaults to SQLite. For any real deployment, it's strongly recommended to externalize these instead. Suggested variables to introduce (e.g. via `django-environ` or `python-decouple`):

| Variable | Purpose | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key | `django-insecure-...` (replace in production) |
| `DEBUG` | Debug mode toggle | `False` in production |
| `ALLOWED_HOSTS` | Comma-separated allowed hostnames | `yourapp.onrender.com,127.0.0.1` |
| `DATABASE_URL` | PostgreSQL connection string (used with `psycopg2-binary`) | `postgres://user:pass@host:5432/dbname` |
| `CORS_ALLOWED_ORIGINS` | Allowed frontend origin(s) | `https://your-frontend.com` |
| `ACCESS_TOKEN_LIFETIME_DAYS` / `REFRESH_TOKEN_LIFETIME_DAYS` | JWT lifetimes | `1` / `7` |

---

## 5. Deployment

The project ships with `gunicorn` and `whitenoise`, and is already deployed on **Render** at **https://event-management-m58t.onrender.com/** (its domain is listed in `ALLOWED_HOSTS`).

General steps for a Render-style deployment:

1. **Push the repo** to GitHub (already done).
2. **Create a new Web Service** on Render (or Railway/Heroku-equivalent), pointing at this repository, with the root/build directory set to `event_management/`.
3. **Build command:**
   ```bash
   pip install -r requirements.txt
   python manage.py collectstatic --noinput
   python manage.py migrate
   ```
4. **Start command:**
   ```bash
   gunicorn event_management.wsgi:application
   ```
5. **Set environment variables** on the hosting platform (see section 4) — at minimum `SECRET_KEY`, `DEBUG=False`, and `ALLOWED_HOSTS` for your deployed domain.
6. **Database:** attach a managed PostgreSQL instance and point `DATABASES` (or `DATABASE_URL`) to it — `psycopg2-binary` is already included for this.
7. **Static & media files:** `whitenoise` serves static files automatically; for uploaded media (event images, QR codes) in production, consider external storage (e.g. S3) since most PaaS filesystems are ephemeral.
8. **CORS:** update `CORS_ALLOWED_ORIGINS` to your deployed frontend URL (currently hardcoded to `http://localhost:5173`).

---

## License

No license specified yet.
