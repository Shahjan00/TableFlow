# TableFlow

TableFlow is a Django REST API for QR-based restaurant ordering. It lets shop owners create shops, tables, and menus, generate QR codes for each table, assign staff to locations, and manage incoming orders in a simple role-based workflow.

This project is built for the common dine-in flow:

1. An owner creates a shop and its menu.
2. The owner creates tables and gets a unique QR code for each one.
3. A guest scans the QR code to view the table-specific menu.
4. The guest submits an order without logging in.
5. Owners and staff track and update order status from `pending` to `ready` to `completed`.

## Why This Project Exists

Restaurants often need a lightweight ordering backend before they need a full POS. TableFlow focuses on the operational core:

- QR-based table discovery
- Menu delivery by table
- Order creation tied to a shop and table
- Owner/staff access control
- JWT authentication for protected management routes

## Features

- Custom user model with role support for `owner`, `staff`, and `other`
- JWT auth using SimpleJWT
- Shop creation and management for owners
- Table creation with generated QR code images
- Menu management per shop
- Staff assignment to specific shops
- Role-aware order access for owners and staff
- Public QR endpoints for customer menu viewing and order placement
- PostgreSQL-ready database configuration via `DATABASE_URL`
- Static file serving with WhiteNoise
- Railway-friendly deployment setup via `Procfile`

## Tech Stack

- Python
- Django 6
- Django REST Framework
- SimpleJWT
- PostgreSQL via `dj-database-url`
- Pillow + `qrcode` for QR image generation
- WhiteNoise
- Gunicorn

## Project Structure

```text
TableFlow/
├── Order_Management/   # Django project settings and root URL config
├── accounts/           # Custom user model, registration, JWT auth routes
├── shops/              # Shops, tables, menus, staff assignment
├── orders/             # Order creation, status updates, QR-facing endpoints
├── core/               # Basic root endpoint
├── manage.py
├── requirements.txt
└── Procfile
```

## Roles And Access

### Owner

- Register and authenticate
- Create and list their own shops
- Create and list tables for their own shops
- Create and list menu items for their own shops
- Assign staff members to a shop
- View, update, and delete orders for shops they own

### Staff

- Authenticate
- Access orders for shops they have been assigned to
- Update order status

### Customer

- No authentication required
- View a menu through a table QR token
- Place an order through a table QR token

## API Overview

Base route groups:

- `/auth/`
- `/shops/`
- `/orders/`
- `/`

### Authentication

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/auth/register/` | Register a new user |
| `POST` | `/auth/token/` | Get JWT access and refresh tokens |
| `POST` | `/auth/token/refresh` | Refresh access token |

### Shops

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/shops/shop/` | List shops owned by the authenticated owner |
| `POST` | `/shops/shop/` | Create a shop |
| `GET` | `/shops/menu/?shop=<shop_id>` | List menu items for the owner’s shop |
| `POST` | `/shops/menu/` | Create a menu item |
| `GET` | `/shops/tables/?shop=<shop_id>` | List tables for the owner’s shop |
| `POST` | `/shops/tables/` | Create a table and generate a QR image |
| `POST` | `/shops/<shop_id>/add-staff/` | Assign a staff user to a shop |

### Orders

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/orders/?shop=<shop_id>` | List accessible orders for owner or staff |
| `POST` | `/orders/` | Create an order for a shop/table pair |
| `GET` | `/orders/<id>` | Retrieve one order |
| `PATCH` | `/orders/<id>` | Update order status |
| `DELETE` | `/orders/<id>` | Delete an order |
| `GET` | `/orders/menu/<qr_token>/` | Public menu lookup from table QR token |
| `POST` | `/orders/order/<qr_token>/` | Public order creation from table QR token |

## Example Request Payloads

### Register a user

```json
{
  "email": "owner@example.com",
  "name": "Table Owner",
  "phone": "1234567890",
  "address": "Main Street",
  "role": "owner",
  "password": "strong-password"
}
```

### Create a shop

```json
{
  "name": "Cafe Nova",
  "phone": "1234567890",
  "address": "42 Market Street",
  "is_active": true
}
```

### Create a menu item

```json
{
  "shop": 1,
  "name": "Cappuccino",
  "price": "4.50",
  "is_available": true
}
```

### Create a table

```json
{
  "shop": 1,
  "table_name": "Table 1",
  "is_active": true
}
```

### Create an order

```json
{
  "shop": 1,
  "table": 2,
  "items": [
    {
      "menu_item": 3,
      "quantity": 2
    },
    {
      "menu_item": 5,
      "quantity": 1
    }
  ]
}
```

### Update order status

```json
{
  "status": "ready"
}
```

Valid order statuses:

- `pending`
- `ready`
- `completed`

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/TableFlow.git
cd TableFlow
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file or export environment variables in your shell.

Required values:

```env
SECRET_KEY=your-django-secret-key
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DB_NAME
```

Notes:

- `DEBUG` is currently hardcoded to `False` in settings.
- `ALLOWED_HOSTS` is currently open with `['*']`.
- The app is configured to use a custom user model: `accounts.User`.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## Authentication Example

Get a token:

```bash
curl -X POST http://127.0.0.1:8000/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "owner@example.com",
    "password": "strong-password"
  }'
```

Use the access token on protected endpoints:

```bash
curl -X GET http://127.0.0.1:8000/shops/shop/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Typical Flow

### Owner flow

1. Register as an `owner`
2. Get a JWT token
3. Create a shop
4. Add menu items
5. Add tables and collect generated QR codes
6. Optionally assign staff to that shop
7. Monitor and update incoming orders

### Customer flow

1. Scan a table QR code
2. Load `/orders/menu/<qr_token>/`
3. Submit an order to `/orders/order/<qr_token>/`

## Deployment Notes

This repo already includes deployment-friendly pieces:

- `Procfile` for process startup
- WhiteNoise middleware for static assets
- `dj_database_url` for database configuration
- `gunicorn` in dependencies

There is also a trusted origin configured for:

```text
https://tableflow-production.up.railway.app
```

That suggests Railway is the intended hosting target.

## Current Limitations

These are worth knowing if you plan to keep building on the project:

- QR codes currently encode `http://127.0.0.1:8000/orders/menu/<qr_token>/`, which is great for local development but should be made environment-aware for production.
- There is no browsable API documentation or OpenAPI schema yet.
- Automated tests are currently placeholders.
- `DEBUG` is hardcoded to `False`, which is not ideal for local development.
- The root route only returns a simple `"Working Fine"` response.

## Roadmap Ideas

- Add Swagger or DRF Spectacular documentation
- Make the QR base URL configurable via environment variable
- Add permissions classes instead of per-view role checks
- Add validation around staff assignment and duplicate resources
- Add analytics for table activity and order volume
- Add a customer-facing frontend for menu browsing and live order status
- Add test coverage for auth, shops, tables, menus, and orders

## Contributing

If you want to improve TableFlow:

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Add or update tests
5. Open a pull request

## License

Add your preferred license here, for example `MIT`.

---

If you want, I can also turn this into a more polished GitHub profile-style README with badges, a hero section, sample cURL snippets, and a stronger portfolio tone.
