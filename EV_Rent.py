import mysql.connector
from datetime import datetime, timedelta
from typing import Optional

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Bushra7755@",
    database="student_db"
)
cursor = conn.cursor()

# Database schema creation
def create_tables():
    """Create all necessary tables for the EV/Bike rental system"""
    
    # Stations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stations (
        station_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        location VARCHAR(255) NOT NULL,
        capacity INT NOT NULL,
        current_bikes INT DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Bikes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bikes (
        bike_id INT AUTO_INCREMENT PRIMARY KEY,
        bike_type ENUM('Electric', 'Regular') NOT NULL,
        model VARCHAR(100) NOT NULL,
        station_id INT,
        status ENUM('Available', 'Rented', 'Maintenance', 'Damaged') DEFAULT 'Available',
        battery_level INT DEFAULT 100,
        last_maintenance DATE,
        total_rentals INT DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (station_id) REFERENCES stations(station_id)
    )
    """)
    
    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(15) NOT NULL,
        license_number VARCHAR(50),
        total_rentals INT DEFAULT 0,
        total_spent DECIMAL(10,2) DEFAULT 0.00,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Rentals table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rentals (
        rental_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        bike_id INT NOT NULL,
        start_station_id INT NOT NULL,
        end_station_id INT,
        start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        end_time TIMESTAMP NULL,
        duration_minutes INT,
        cost DECIMAL(8,2),
        status ENUM('Active', 'Completed', 'Cancelled') DEFAULT 'Active',
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (bike_id) REFERENCES bikes(bike_id),
        FOREIGN KEY (start_station_id) REFERENCES stations(station_id),
        FOREIGN KEY (end_station_id) REFERENCES stations(station_id)
    )
    """)
    
    # Repairs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS repairs (
        repair_id INT AUTO_INCREMENT PRIMARY KEY,
        bike_id INT NOT NULL,
        issue_type ENUM('Battery', 'Brake', 'Tire', 'Chain', 'Electronics', 'Other') NOT NULL,
        description TEXT,
        reported_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        repair_date TIMESTAMP NULL,
        cost DECIMAL(8,2),
        status ENUM('Reported', 'In Progress', 'Completed') DEFAULT 'Reported',
        FOREIGN KEY (bike_id) REFERENCES bikes(bike_id)
    )
    """)
    
    conn.commit()
    print("Database tables created successfully!")

# Station Management
def add_station():
    """Add a new station"""
    name = input("Enter station name: ")
    location = input("Enter station location: ")
    capacity = int(input("Enter station capacity: "))
    
    query = "INSERT INTO stations (name, location, capacity) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, location, capacity))
    conn.commit()
    print("Station added successfully!\n")

def view_stations():
    """View all stations with current bike count"""
    cursor.execute("""
    SELECT s.station_id, s.name, s.location, s.capacity, 
           COUNT(b.bike_id) as current_bikes
    FROM stations s
    LEFT JOIN bikes b ON s.station_id = b.station_id AND b.status = 'Available'
    GROUP BY s.station_id
    """)
    
    results = cursor.fetchall()
    print("\n=== STATIONS ===")
    for station in results:
        print(f"ID: {station[0]}, Name: {station[1]}, Location: {station[2]}")
        print(f"Capacity: {station[3]}, Available Bikes: {station[4]}")
        print("-" * 40)

# Bike Management
def add_bike():
    """Add a new bike"""
    bike_type = input("Enter bike type (Electric/Regular): ")
    model = input("Enter bike model: ")
    
    # Show available stations
    cursor.execute("SELECT station_id, name FROM stations")
    stations = cursor.fetchall()
    print("\nAvailable Stations:")
    for station in stations:
        print(f"{station[0]}: {station[1]}")
    
    station_id = int(input("Enter station ID: "))
    battery_level = 100 if bike_type.lower() == 'electric' else None
    
    query = "INSERT INTO bikes (bike_type, model, station_id, battery_level) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (bike_type, model, station_id, battery_level))
    conn.commit()
    print("Bike added successfully!\n")

def view_bikes():
    """View all bikes with their current status"""
    cursor.execute("""
    SELECT b.bike_id, b.bike_type, b.model, s.name as station_name, 
           b.status, b.battery_level, b.total_rentals
    FROM bikes b
    LEFT JOIN stations s ON b.station_id = s.station_id
    ORDER BY b.bike_id
    """)
    
    results = cursor.fetchall()
    print("\n=== BIKES ===")
    for bike in results:
        print(f"ID: {bike[0]}, Type: {bike[1]}, Model: {bike[2]}")
        print(f"Station: {bike[3] if bike[3] else 'N/A'}, Status: {bike[4]}")
        print(f"Battery: {bike[5] if bike[5] else 'N/A'}%, Total Rentals: {bike[6]}")
        print("-" * 40)

def update_bike_status():
    """Update bike status (maintenance, damaged, etc.)"""
    bike_id = int(input("Enter bike ID: "))
    print("Status options: Available, Rented, Maintenance, Damaged")
    new_status = input("Enter new status: ")
    
    query = "UPDATE bikes SET status = %s WHERE bike_id = %s"
    cursor.execute(query, (new_status, bike_id))
    conn.commit()
    print("Bike status updated successfully!\n")

# User Management
def add_user():
    """Add a new user"""
    name = input("Enter user name: ")
    email = input("Enter email: ")
    phone = input("Enter phone number: ")
    license_number = input("Enter license number (optional): ")
    
    query = "INSERT INTO users (name, email, phone, license_number) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, email, phone, license_number if license_number else None))
    conn.commit()
    print("User added successfully!\n")

def view_users():
    """View all users"""
    cursor.execute("SELECT * FROM users ORDER BY user_id")
    results = cursor.fetchall()
    
    print("\n=== USERS ===")
    for user in results:
        print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
        print(f"Phone: {user[3]}, License: {user[4] if user[4] else 'N/A'}")
        print(f"Total Rentals: {user[5]}, Total Spent: ${user[6]}")
        print("-" * 40)

# Rental Management
def start_rental():
    """Start a new rental"""
    user_id = int(input("Enter user ID: "))
    
    # Show available bikes
    cursor.execute("""
    SELECT b.bike_id, b.bike_type, b.model, s.name as station_name, b.battery_level
    FROM bikes b
    JOIN stations s ON b.station_id = s.station_id
    WHERE b.status = 'Available'
    """)
    
    available_bikes = cursor.fetchall()
    if not available_bikes:
        print("No bikes available for rental!\n")
        return
    
    print("\nAvailable Bikes:")
    for bike in available_bikes:
        battery_info = f", Battery: {bike[4]}%" if bike[4] else ""
        print(f"ID: {bike[0]}, Type: {bike[1]}, Model: {bike[2]}, Station: {bike[3]}{battery_info}")
    
    bike_id = int(input("Enter bike ID to rent: "))
    
    # Get bike's current station
    cursor.execute("SELECT station_id FROM bikes WHERE bike_id = %s", (bike_id,))
    station_id = cursor.fetchone()[0]
    
    # Start rental
    query = "INSERT INTO rentals (user_id, bike_id, start_station_id) VALUES (%s, %s, %s)"
    cursor.execute(query, (user_id, bike_id, station_id))
    
    # Update bike status
    cursor.execute("UPDATE bikes SET status = 'Rented', station_id = NULL WHERE bike_id = %s", (bike_id,))
    
    conn.commit()
    print("Rental started successfully!\n")

def end_rental():
    """End an active rental"""
    rental_id = int(input("Enter rental ID: "))
    
    # Show available stations for return
    cursor.execute("SELECT station_id, name FROM stations")
    stations = cursor.fetchall()
    print("\nAvailable Return Stations:")
    for station in stations:
        print(f"{station[0]}: {station[1]}")
    
    end_station_id = int(input("Enter return station ID: "))
    
    # Get rental details
    cursor.execute("""
    SELECT r.bike_id, r.start_time, b.bike_type
    FROM rentals r
    JOIN bikes b ON r.bike_id = b.bike_id
    WHERE r.rental_id = %s AND r.status = 'Active'
    """, (rental_id,))
    
    rental_info = cursor.fetchone()
    if not rental_info:
        print("Rental not found or already completed!\n")
        return
    
    bike_id, start_time, bike_type = rental_info
    end_time = datetime.now()
    duration_minutes = int((end_time - start_time).total_seconds() / 60)
    
    # Calculate cost (Electric: $0.50/min, Regular: $0.30/min)
    rate_per_minute = 0.50 if bike_type == 'Electric' else 0.30
    cost = duration_minutes * rate_per_minute
    
    # Update rental
    query = """
    UPDATE rentals 
    SET end_time = %s, end_station_id = %s, duration_minutes = %s, cost = %s, status = 'Completed'
    WHERE rental_id = %s
    """
    cursor.execute(query, (end_time, end_station_id, duration_minutes, cost, rental_id))
    
    # Update bike status and station
    cursor.execute("UPDATE bikes SET status = 'Available', station_id = %s, total_rentals = total_rentals + 1 WHERE bike_id = %s", 
                   (end_station_id, bike_id))
    
    # Update user statistics
    cursor.execute("UPDATE users SET total_rentals = total_rentals + 1, total_spent = total_spent + %s WHERE user_id = (SELECT user_id FROM rentals WHERE rental_id = %s)", 
                   (cost, rental_id))
    
    conn.commit()
    print(f"Rental completed! Duration: {duration_minutes} minutes, Cost: ${cost:.2f}\n")

def view_active_rentals():
    """View all active rentals"""
    cursor.execute("""
    SELECT r.rental_id, u.name, b.bike_type, b.model, s.name as start_station, r.start_time
    FROM rentals r
    JOIN users u ON r.user_id = u.user_id
    JOIN bikes b ON r.bike_id = b.bike_id
    JOIN stations s ON r.start_station_id = s.station_id
    WHERE r.status = 'Active'
    ORDER BY r.start_time
    """)
    
    results = cursor.fetchall()
    print("\n=== ACTIVE RENTALS ===")
    for rental in results:
        duration = datetime.now() - rental[5]
        duration_str = str(duration).split('.')[0]  # Remove microseconds
        print(f"Rental ID: {rental[0]}, User: {rental[1]}")
        print(f"Bike: {rental[2]} {rental[3]}, Start Station: {rental[4]}")
        print(f"Duration: {duration_str}")
        print("-" * 40)

# Repair Management
def report_damage():
    """Report bike damage"""
    bike_id = int(input("Enter bike ID: "))
    print("Issue types: Battery, Brake, Tire, Chain, Electronics, Other")
    issue_type = input("Enter issue type: ")
    description = input("Enter description: ")
    
    query = "INSERT INTO repairs (bike_id, issue_type, description) VALUES (%s, %s, %s)"
    cursor.execute(query, (bike_id, issue_type, description))
    
    # Update bike status to damaged
    cursor.execute("UPDATE bikes SET status = 'Damaged' WHERE bike_id = %s", (bike_id,))
    
    conn.commit()
    print("Damage reported successfully!\n")

def view_repairs():
    """View all repair records"""
    cursor.execute("""
    SELECT r.repair_id, b.bike_type, b.model, r.issue_type, r.description, 
           r.reported_date, r.status, r.cost
    FROM repairs r
    JOIN bikes b ON r.bike_id = b.bike_id
    ORDER BY r.reported_date DESC
    """)
    
    results = cursor.fetchall()
    print("\n=== REPAIR RECORDS ===")
    for repair in results:
        print(f"Repair ID: {repair[0]}, Bike: {repair[1]} {repair[2]}")
        print(f"Issue: {repair[3]}, Status: {repair[6]}")
        print(f"Description: {repair[4]}")
        print(f"Reported: {repair[5]}, Cost: ${repair[7] if repair[7] else 'N/A'}")
        print("-" * 40)

def complete_repair():
    """Mark repair as completed"""
    repair_id = int(input("Enter repair ID: "))
    cost = float(input("Enter repair cost: "))
    
    query = "UPDATE repairs SET status = 'Completed', repair_date = NOW(), cost = %s WHERE repair_id = %s"
    cursor.execute(query, (cost, repair_id))
    
    # Get bike ID and update status
    cursor.execute("SELECT bike_id FROM repairs WHERE repair_id = %s", (repair_id,))
    bike_id = cursor.fetchone()[0]
    cursor.execute("UPDATE bikes SET status = 'Available' WHERE bike_id = %s", (bike_id,))
    
    conn.commit()
    print("Repair completed successfully!\n")

# Analytics Functions
def popular_stations():
    """Show most popular stations by rental count"""
    cursor.execute("""
    SELECT s.name, s.location, COUNT(r.rental_id) as rental_count
    FROM stations s
    LEFT JOIN rentals r ON s.station_id = r.start_station_id
    GROUP BY s.station_id
    ORDER BY rental_count DESC
    LIMIT 10
    """)
    
    results = cursor.fetchall()
    print("\n=== MOST POPULAR STATIONS ===")
    for i, station in enumerate(results, 1):
        print(f"{i}. {station[0]} ({station[1]}) - {station[2]} rentals")

def problematic_bikes():
    """Show bikes with most repair issues"""
    cursor.execute("""
    SELECT b.bike_id, b.bike_type, b.model, COUNT(r.repair_id) as issue_count,
           s.name as current_station
    FROM bikes b
    LEFT JOIN repairs r ON b.bike_id = r.bike_id
    LEFT JOIN stations s ON b.station_id = s.station_id
    GROUP BY b.bike_id
    HAVING issue_count > 0
    ORDER BY issue_count DESC
    LIMIT 10
    """)
    
    results = cursor.fetchall()
    print("\n=== BIKES WITH MOST ISSUES ===")
    for bike in results:
        print(f"Bike ID: {bike[0]}, Type: {bike[1]}, Model: {bike[2]}")
        print(f"Issues: {bike[3]}, Current Station: {bike[4] if bike[4] else 'Not at station'}")
        print("-" * 40)

def rental_analytics():
    """Show rental analytics"""
    # Average rental time
    cursor.execute("""
    SELECT AVG(duration_minutes) as avg_duration, 
           COUNT(*) as total_rentals,
           SUM(cost) as total_revenue
    FROM rentals 
    WHERE status = 'Completed'
    """)
    
    avg_stats = cursor.fetchone()
    
    # Most active users
    cursor.execute("""
    SELECT u.name, u.total_rentals, u.total_spent
    FROM users u
    ORDER BY u.total_rentals DESC
    LIMIT 5
    """)
    
    top_users = cursor.fetchall()
    
    print("\n=== RENTAL ANALYTICS ===")
    print(f"Average Rental Duration: {avg_stats[0]:.1f} minutes" if avg_stats[0] else "No completed rentals")
    print(f"Total Completed Rentals: {avg_stats[1]}")
    print(f"Total Revenue: ${avg_stats[2]:.2f}" if avg_stats[2] else "$0.00")
    
    print("\nTop Users:")
    for user in top_users:
        print(f"{user[0]} - {user[1]} rentals, ${user[2]:.2f} spent")

# Main Menu System
def main_menu():
    """Main menu for the EV/Bike rental system"""
    
    # Create tables on startup
    create_tables()
    
    while True:
        print("\n" + "="*50)
        print("    EV/BIKE RENTAL MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Station Management")
        print("2. Bike Management") 
        print("3. User Management")
        print("4. Rental Management")
        print("5. Repair Management")
        print("6. Analytics & Reports")
        print("7. Exit")
        print("-"*50)
        
        choice = input("Choose an option (1-7): ")
        
        if choice == "1":
            station_menu()
        elif choice == "2":
            bike_menu()
        elif choice == "3":
            user_menu()
        elif choice == "4":
            rental_menu()
        elif choice == "5":
            repair_menu()
        elif choice == "6":
            analytics_menu()
        elif choice == "7":
            print("Thank you for using EV/Bike Rental System!")
            break
        else:
            print("Invalid choice. Please try again.")

def station_menu():
    """Station management submenu"""
    while True:
        print("\n=== STATION MANAGEMENT ===")
        print("1. Add Station")
        print("2. View All Stations")
        print("3. Back to Main Menu")
        
        choice = input("Choose an option: ")
        if choice == "1":
            add_station()
        elif choice == "2":
            view_stations()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

def bike_menu():
    """Bike management submenu"""
    while True:
        print("\n=== BIKE MANAGEMENT ===")
        print("1. Add Bike")
        print("2. View All Bikes")
        print("3. Update Bike Status")
        print("4. Back to Main Menu")
        
        choice = input("Choose an option: ")
        if choice == "1":
            add_bike()
        elif choice == "2":
            view_bikes()
        elif choice == "3":
            update_bike_status()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

def user_menu():
    """User management submenu"""
    while True:
        print("\n=== USER MANAGEMENT ===")
        print("1. Add User")
        print("2. View All Users")
        print("3. Back to Main Menu")
        
        choice = input("Choose an option: ")
        if choice == "1":
            add_user()
        elif choice == "2":
            view_users()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

def rental_menu():
    """Rental management submenu"""
    while True:
        print("\n=== RENTAL MANAGEMENT ===")
        print("1. Start Rental")
        print("2. End Rental")
        print("3. View Active Rentals")
        print("4. Back to Main Menu")
        
        choice = input("Choose an option: ")
        if choice == "1":
            start_rental()
        elif choice == "2":
            end_rental()
        elif choice == "3":
            view_active_rentals()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

def repair_menu():
    """Repair management submenu"""
    while True:
        print("\n=== REPAIR MANAGEMENT ===")
        print("1. Report Damage")
        print("2. View All Repairs")
        print("3. Complete Repair")
        print("4. Back to Main Menu")
        
        choice = input("Choose an option: ")
        if choice == "1":
            report_damage()
        elif choice == "2":
            view_repairs()
        elif choice == "3":
            complete_repair()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

def analytics_menu():
    """Analytics and reports submenu"""
    while True:
        print("\n=== ANALYTICS & REPORTS ===")
        print("1. Most Popular Stations")
        print("2. Bikes with Most Issues")
        print("3. Rental Analytics")
        print("4. Back to Main Menu")
        
        choice = input("Choose an option: ")
        if choice == "1":
            popular_stations()
        elif choice == "2":
            problematic_bikes()
        elif choice == "3":
            rental_analytics()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

# Run the application
if __name__ == "__main__":
    try:
        main_menu()
    finally:
        cursor.close()
        conn.close()
