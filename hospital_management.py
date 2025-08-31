import mysql.connector
from mysql.connector import Error
import csv

def display_heading():
    """
    Displays a dynamic heading for the Hospital Management System.
    """
    print("=" * 50)
    print(" " * 10 + "Hospital Management System")
    print("=" * 50)

def setupDatabase():
    """
    Automatically creates the database and tables if they don't exist.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS hospital_db")
            print("Database 'hospital_db' is ready!")
            # Use the database
            cursor.execute("USE hospital_db")
            # Create patients, doctors, and appointments tables if they don't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    PatientID VARCHAR(50) PRIMARY KEY,
                    PatientName VARCHAR(100),
                    Age INT,
                    Gender VARCHAR(20),
                    Disease VARCHAR(100)
                )
            """)
            print("Table 'patients' is ready!")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS doctors (
                    DoctorID VARCHAR(50) PRIMARY KEY,
                    DoctorName VARCHAR(100),
                    Specialization VARCHAR(100),
                    Schedule VARCHAR(100)
                )
            """)
            print("Table 'doctors' is ready!")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    AppointmentID INT AUTO_INCREMENT PRIMARY KEY,
                    PatientID VARCHAR(50),
                    DoctorID VARCHAR(50),
                    AppointmentTime DATETIME,
                    FOREIGN KEY (PatientID) REFERENCES patients(PatientID),
                    FOREIGN KEY (DoctorID) REFERENCES doctors(DoctorID)
                )
            """)
            print("Table 'appointments' is ready!")
    except Error as e:
        print(f"Error during database setup: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Database setup complete.")

def exportToCSV(table):
    """
    Exports the records of the given table to a CSV file.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='hospital_db',
            user='root',
            password='1234'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            # Execute query to fetch all records from the table
            cursor.execute(f"SELECT * FROM {table}")
            records = cursor.fetchall()
            # Writing records to the CSV file
            with open(f'{table}.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                # Write header based on table
                if table == 'patients':
                    writer.writerow(["PatientID", "PatientName", "Age", "Gender", "Disease"])
                elif table == 'doctors':
                    writer.writerow(["DoctorID", "DoctorName", "Specialization", "Schedule"])
                elif table == 'appointments':
                    writer.writerow(["AppointmentID", "PatientID", "DoctorID", "AppointmentTime"])
                writer.writerows(records)
            print(f"Records exported to '{table}.csv' successfully!")
    except Error as e:
        print(f"Error during CSV export: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def newPatient():
    """
    Adds a new patient record.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='hospital_db',
            user='root',
            password='1234'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            print("Add a new Patient Record:")
            print("==========================")
            # Input patient details
            patient_id = input("Enter Patient ID: ")
            patient_name = input("Enter Patient Name: ")
            age = int(input("Enter Age: "))
            gender = input("Enter Gender: ")
            disease = input("Enter Disease: ")
            # Insert record into the MySQL table
            query = """
                INSERT INTO patients (PatientID, PatientName, Age, Gender, Disease)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (patient_id, patient_name, age, gender, disease)
            cursor.execute(query, values)
            connection.commit()
            print("Patient Record Saved")
            exportToCSV("patients") # Update CSV
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def newDoctor():
    """
    Adds a new doctor record.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='hospital_db',
            user='root',
            password='1234'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            print("Add a new Doctor Record:")
            print("==========================")
            # Input doctor details
            doctor_id = input("Enter Doctor ID: ")
            doctor_name = input("Enter Doctor Name: ")
            specialization = input("Enter Specialization: ")
            schedule = input("Enter Schedule: ")
            # Insert record into the MySQL table
            query = """
                INSERT INTO doctors (DoctorID, DoctorName, Specialization, Schedule)
                VALUES (%s, %s, %s, %s)
            """
            values = (doctor_id, doctor_name, specialization, schedule)
            cursor.execute(query, values)
            connection.commit()
            print("Doctor Record Saved")
            exportToCSV("doctors") # Update CSV
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def newAppointment():
    """
    Adds a new appointment record.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='hospital_db',
            user='root',
            password='1234'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            print("Book a new Appointment:")
            print("========================")
            # Input appointment details
            patient_id = input("Enter Patient ID: ")
            doctor_id = input("Enter Doctor ID: ")
            appointment_time = input("Enter Appointment Time (YYYY-MM-DD HH:MM:SS): ")
            # Insert record into the MySQL table
            query = """
                INSERT INTO appointments (PatientID, DoctorID, AppointmentTime)
                VALUES (%s, %s, %s)
            """
            values = (patient_id, doctor_id, appointment_time)
            cursor.execute(query, values)
            connection.commit()
            print("Appointment Booked")
            exportToCSV("appointments") # Update CSV
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def listPatients():
    """
    Lists all patient record
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='hospital_db',
            user='root',
            password='1234'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            print("List of All Patient Records:")
            print("=============================")
            # Fetch all records
            query = "SELECT * FROM patients"
            cursor.execute(query)
            records = cursor.fetchall()
            if records:
                for record in records:
                    print(f"PatientID: {record[0]}, Name: {record[1]}, Age: {record[2]}, Gender: {record[3]}, Disease: {record[4]}")
            else:
                print("No patient records found!")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Main Execution
if __name__ == "__main__":
    display_heading() # Display the heading dynamically
    setupDatabase()
    while True:
        print("\nMenu:")
        print("1. Add New Patient")
        print("2. Add New Doctor")
        print("3. Book an Appointment")
        print("4. List All Patients")
        print("5. Export Patient Data to CSV")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            newPatient()
        elif choice == '2':
            newDoctor()
        elif choice == '3':
            newAppointment()
        elif choice == '4':
            listPatients()
        elif choice == '5':
            exportToCSV("patients")
        elif choice == '6':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")