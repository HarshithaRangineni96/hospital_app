# 🏥 Hospital Admissions Application

A full-stack web application for managing hospital patient admissions, built with Python, Flask, SQLAlchemy, and MySQL.

---

## Project Description

This application allows hospital staff to manage patients, doctors, and admissions through a clean web interface. It supports full CRUD operations, enforces data integrity through server-side validation and foreign key constraints, and provides an aggregate summary dashboard.

**Intended users:** Hospital administrative staff.

---

## Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Language  | Python 3                          |
| Backend   | Flask                             |
| ORM       | Flask-SQLAlchemy                  |
| Database  | MySQL                             |
| Driver    | PyMySQL                           |
| Frontend  | HTML5, Bootstrap 5, Jinja2        |
| Version Control | Git                         |

---

## Installation Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd hospital_app
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Database Setup

### 1. Create the MySQL database
```sql
CREATE DATABASE hospital_db;
```

### 2. Run the schema script
```bash
mysql -u root -p hospital_db < schema.sql
```

### 3. Update the database connection in `app.py`
```python
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://YOUR_USER:YOUR_PASSWORD@localhost/hospital_db"
)
```

---

## Usage

### Start the development server
```bash
python app.py
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

### Main Features

| Page        | URL           | Description                                   |
|-------------|---------------|-----------------------------------------------|
| Dashboard   | `/`           | Aggregate stats: totals, avg stay, top doctor |
| Patients    | `/patients`   | Add, view, delete patients                    |
| Doctors     | `/doctors`    | Add, view, delete doctors                     |
| Admissions  | `/admissions` | Record admissions, discharge patients, delete |

---

## Key Features Implemented

- **Multi-Table CRUD** across Patients, Doctors, and Admissions
- **One-to-Many Relationship**: Each patient/doctor can have many admissions
- **Transaction Logic**: Deleting a patient cascades to their admissions atomically
- **Server-Side Validation**: Empty fields, duplicate patient names are rejected
- **Summary Dashboard**: Uses `COUNT`, `AVG`, `DATEDIFF`, `MAX` SQL aggregates
- **3NF Compliance**: `stay_length` is computed at query time, not stored
