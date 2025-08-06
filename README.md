# 🚲 EV/Bike Rental Management System

A command-line-based Python application that manages Electric and Regular bike rentals, repairs, user records, and analytics using a MySQL backend.

---

## 📋 Features

### ✅ Station Management
- Add new stations
- View station details with available bike count

### 🚲 Bike Management
- Add bikes (Electric or Regular)
- View all bikes with status, location, and battery level
- Update bike status (Available, Rented, Maintenance, Damaged)

### 👤 User Management
- Register new users
- View user records with rental history

### ⏱️ Rental Management
- Start and end rentals
- View active rentals
- Auto-calculate cost and duration

### 🛠️ Repair Management
- Report damaged bikes
- View repair history
- Complete and log repair details

### 📊 Analytics & Reports
- Most popular stations
- Bikes with the most repair issues
- Average rental duration, total revenue, and top users

---

## 🛠️ Setup Instructions

### 1. Prerequisites

- Python 3.7+
- MySQL server running on `localhost`
- MySQL user with privileges (default: `root`)
- MySQL database named `student_db`

### 2. Install Python Dependencies

```bash
pip install mysql-connector-python
3. Create the Database in MySQL
sql
Copy
Edit
CREATE DATABASE student_db;
4. Update MySQL Credentials
Edit the connection block in your script if necessary:

python
Copy
Edit
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YourPasswordHere",
    database="student_db"
)
🚀 Running the Application
bash
Copy
Edit
python your_script_name.py
On first run, it will automatically create the required tables in the database.

📂 Project Structure
bash
Copy
Edit
EV_Bike_Rental/
├── bike_rental.py         # Main application logic
└── README.md              # This file
🧠 Design Overview
Database Tables:

stations: Station info and capacity

bikes: Bikes and their status/location

users: Registered users

rentals: Rental history

repairs: Repair logs

Cost Calculation:

Regular Bike: $0.30/minute

Electric Bike: $0.50/minute

Real-Time Updates:

Tracks battery levels, bike status, station availability, and rental stats dynamically.

📈 Analytics Preview
Top Stations by rental volume

Most Repaired Bikes

Rental Insights:

Average rental duration

Total revenue

Top 5 users

❗ Notes
Uses CURRENT_TIMESTAMP for datetime fields.

Validations are basic – extend as needed.

Enum values prevent invalid status entries in the database.

🤝 Contributions
You're welcome to improve the system by:

Adding a GUI (Tkinter or PyQt)

Integrating a REST API (Flask or FastAPI)

Adding unit tests

Improving reporting with charts

📄 License
This project is for educational purposes. No commercial license attached. Use it at your discretion.

yaml
Copy
Edit
