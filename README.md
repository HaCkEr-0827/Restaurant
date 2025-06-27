# Restaurant API with Django and Django Rest Framework

A full-featured restaurant backend API built with Django and Django REST Framework. Includes table booking, menu browsing, order creation, user authentication, and admin analytics.

---

## 🌟 Features

### ✅ User Authentication

* JWT-based signup, login, logout
* OTP verification after signup
* Password reset via OTP

### ✅ Menu Management

* Category and item CRUD
* Only admin users can manage menu

### ✅ Table Booking

* Users can book tables for a specific date and time
* Booking is only possible between 10:00 and 23:00
* Prevents double booking of the same table

### ✅ Orders

* Users can create and view orders
* Order status: pending, approved, rejected

### ✅ Admin Analytics

* Top 5 most ordered items

### ✅ API Documentation

* Swagger UI: `/swagger/`
* ReDoc UI: `/redoc/`

---

## 📊 Technologies Used

* Python 3.11+
* Django 5.x
* Django REST Framework
* SimpleJWT (JWT authentication)
* drf-yasg (Swagger)
* PostgreSQL (default DB, can switch to SQLite)
* Gunicorn (production-ready server)

---

## 🔍 API Endpoints (Shortened)

### Authentication

| Endpoint            | Method | Description           |
| ------------------- | ------ | --------------------- |
| `/signup/`          | POST   | Request OTP           |
| `/verify/`          | POST   | Verify OTP & Register |
| `/login/`           | POST   | Login                 |
| `/logout/`          | POST   | Logout                |
| `/forgot-password/` | POST   | Request reset OTP     |
| `/reset-password/`  | POST   | Set new password      |

### Categories & Items

| Endpoint            | Method         | Description            |
| ------------------- | -------------- | ---------------------- |
| `/categories/`      | GET/POST       | List or create         |
| `/categories/<id>/` | GET/PUT/DELETE | Retrieve/update/delete |
| `/items/`           | GET/POST       | List or create         |
| `/items/<id>/`      | GET/PUT/DELETE | Retrieve/update/delete |

### Table & Booking

\| `/tables/`        | GET/POST | All tables or create |
\| `/bookings/`      | GET/POST | User bookings       |
\| `/bookings/<id>/` | PUT/DELETE | Update/delete booking |

### Orders

\| `/orders/`        | GET/POST | User orders        |
\| `/orders/<id>/`   | PUT/DELETE | Update/delete order |

### Analytics (Admin only)

\| `/analytics/`     | GET     | Top 5 ordered items |

---

## 📥 Installation

1. **Clone the repo:**

```bash
git clone https://github.com/HaCkEr-0827/Restaurant.git
cd restaurant-api
```

2. **Create a virtual environment and activate it:**

```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

1. **Apply migrations:**

```bash
python manage.py migrate
```

2. **Create superuser (for admin access):**

```bash
python manage.py createsuperuser
```

3. **Run the development server:**

```bash
python manage.py runserver
```

---

## 🚧 Development

* Admin Panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)
* Swagger Docs: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
* ReDoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

---

## 🌐 Postman Collection

You can import the Postman collection using the `restaurant-api.postman_collection.json` file which includes:

* Signup & OTP verify
* Login, logout
* CRUD for Category, Item
* Booking tables
* Making orders
* Admin analytics

---

## 📄 License

MIT License. Use freely for personal and commercial projects.
