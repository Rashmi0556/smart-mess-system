# 🍱 Smart Mess & Meal Subscription System

A web application for managing hostel mess subscriptions, menus, attendance, and billing.

Built with **Python + Flask + MySQL + Bootstrap**

---

## Features

### Student
- Register and login
- Subscribe to a mess and meal plan (veg/non-veg)
- View today's menu based on their meal type
- View attendance history
- View and pay monthly bill (calculated from attendance)

### Mess Admin
- Login and manage their mess
- Add and edit weekly menu (veg + non-veg)
- Mark daily attendance for subscribers
- View all active subscribers

---

## Tech Stack

| Layer    | Technology        |
|----------|-------------------|
| Backend  | Python, Flask     |
| Database | MySQL             |
| ORM      | SQLAlchemy        |
| Frontend | Bootstrap 5       |
| Auth     | Flask sessions, Werkzeug |

---

## Database Design (8 Tables)

- `STUDENT` — student accounts
- `MESS` — mess details
- `MESS_ADMIN` — admin accounts per mess
- `MEAL_PLAN` — veg/non-veg plans with pricing
- `SUBSCRIPTION` — links student to mess and plan
- `MENU` — weekly menu per mess (veg + non-veg rows)
- `ATTENDANCE` — daily meal attendance per student
- `PAYMENT` — billing records per student

## DBMS Concepts Covered

- Normalization (1NF → 3NF)
- Multi-table joins
- Triggers (auto-expire subscription, auto-create payment)
- Stored procedure (monthly bill calculation)
- Views (active subscribers, today's menu)
- Transactions (atomic payment recording)
- Foreign keys and referential integrity
- Role-based access (student vs mess admin)

---

## Project Structure
smart-mess-system/
├── app/
│   ├── init.py
│   ├── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── student.py
│   │   ├── admin.py
│   │   └── payment.py
│   └── templates/
│       ├── base.html
│       ├── auth/
│       ├── student/
│       ├── admin/
│       └── payment/
├── config.py
├── run.py
└── requirements.txt
---

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/Rashmi0556/smart-mess-system.git
cd smart-mess-system
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

### 3. Setup MySQL
- Create database: `CREATE DATABASE mess_system;`
- Run the SQL schema script to create all 8 tables
- Add a mess and admin account

### 4. Configure environment
Create a `.env` file:
SECRET_KEY=your_secret_key
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_DB=mess_system
### 5. Run the app
```bash
python run.py
```

Visit `http://127.0.0.1:5000`

---

## Test Credentials

| Role | Email | Password |
|------|-------|----------|
| Mess Admin | admin@mess.com | admin123 |
| Student | register at /register | your choice |