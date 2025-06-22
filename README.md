
# 🍽 Restaurant API with Django and Django Rest Framework

A powerful Restaurant API built using Django and Django Rest Framework. It allows users to view menus, book tables, and place orders. Admins can manage the system using role-based access control.

---

## 📑 Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [API Endpoints](#api-endpoints)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## ✅ Features

- **Authentication:**
  - JWT-based user authentication (`signup`, `login`, `logout`)
  - Role-based permission control (Admin vs User)

- **Admin Permissions:**
  - Only Admins can Create/Update/Delete `Category`, `Item`, `Hall`, `Table`

- **User Features:**
  - View menu (categories and items)
  - Book available tables (between 10:00 and 23:00 only)
  - Place and manage their own orders

- **Swagger Docs:**
  - Full Swagger and Redoc integration for API testing and docs

- **Analytics:**
  - Admin-only endpoint to see most ordered menu items

---

## ⚙️ Technologies Used

- **Python 3.10+**
- **Django 5.x**
- **Django Rest Framework**
- **Simple JWT** (for access/refresh token auth)
- **drf-yasg** (for Swagger and Redoc docs)
- **PostgreSQL + psycopg2** (can be replaced with SQLite for development)
- **gunicorn** (for deployment)

---

## 🔗 API Endpoints

| Feature       | Method | Endpoint                       | Access      |
|---------------|--------|--------------------------------|-------------|
| Sign Up       | POST   | `/signup/`                     | Public      |
| Login         | POST   | `/login/`                      | Public      |
| Logout        | POST   | `/logout/`                     | Authenticated |
| JWT Token     | POST   | `/token/`                      | Public      |
| Token Refresh | POST   | `/token/refresh/`              | Public      |
| Token Verify  | POST   | `/token/verify/`               | Public      |
| View Profile  | GET    | `/profile/`                    | Authenticated |
| View Categories | GET  | `/categories/`                 | All         |
| Manage Categories | CRUD | `/categories/<id>/`          | Admin only  |
| View Items    | GET    | `/items/`                      | All         |
| Manage Items  | CRUD   | `/items/<id>/`                 | Admin only  |
| View Halls    | GET    | `/halls/`                      | All         |
| Manage Halls  | CRUD   | `/halls/<id>/`                 | Admin only  |
| View Tables   | GET    | `/tables/`                     | All         |
| Manage Tables | CRUD   | `/tables/<id>/`                | Admin only  |
| My Bookings   | CRUD   | `/bookings/`, `/bookings/<id>/`| Authenticated |
| My Orders     | CRUD   | `/orders/`, `/orders/<id>/`    | Authenticated |
| Analytics     | GET    | `/analytics/`                  | Admin only  |
| Swagger UI    | GET    | `/swagger/`                    | Public      |
| Redoc UI      | GET    | `/redoc/`                      | Public      |

---

## 📥 Installation

1. **Clone the repo:**

```bash
git clone https://github.com/yourusername/restaurant-api.git
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

Visit: http://127.0.0.1:8000/

4. **API Documentation:**

- Swagger: http://127.0.0.1:8000/swagger/
- Redoc: http://127.0.0.1:8000/redoc/

---

## 👥 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Steps:
1. Fork this repo
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### 🙋 Need Help?

You can contact the project owner or open an issue in the GitHub repository for support.