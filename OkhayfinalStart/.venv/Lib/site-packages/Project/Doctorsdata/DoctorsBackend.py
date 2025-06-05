from DatabaseConnection import DatabaseConnection  # type: ignore
from PyQt5.QtWidgets import QMessageBox  # type: ignore
import traceback

# transaction_handler.py

def show_error(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Error")
    msg.setText(message)
    msg.exec_()

def execute_transaction(first_name, last_name, cnic, license_no, joining_date,
                        city, street, state, postal_code, country, username,
                        password_hash,  salary_amount):
    try:
        # Establish database connection
        conn = DatabaseConnection.get_connection()
        conn.autocommit = False  # Disable autocommit for transaction
        cursor = conn.cursor()

        # Begin Transaction
        cursor.execute("BEGIN TRANSACTION;")

        # Insert into TblAddress
        cursor.execute(
            "INSERT INTO TblAddress (city, street, state, postal_code, country) "
            "OUTPUT INSERTED.AddressID "
            "VALUES (?, ?, ?, ?, ?);",
            (city, street, state, postal_code, country)
        )
        address_id = cursor.fetchone()[0]
        print(f"Debug: Address ID = {address_id}")

        # Insert into TblCredentials
        cursor.execute(
            "INSERT INTO TblCredentials (Username, PasswordHash, RoleID) "
            "OUTPUT INSERTED.CredentialID "
            "VALUES (?, ?, ?);",
            (username, password_hash, 3)
        )
        credential_id = cursor.fetchone()[0]
        print(f"Debug: Credential ID = {credential_id}")

        # Insert into TblSalary
        cursor.execute(
            "INSERT INTO TblSalary (Amount) OUTPUT INSERTED.SalaryID VALUES (?);",
            (salary_amount,)
        )
        salary_id = cursor.fetchone()[0]
        print(f"Debug: Salary ID = {salary_id}")

        # Insert into TblDoctors
        cursor.execute(
            "INSERT INTO TblDoctors (FirstName, LastName, CNIC, LicenseNo, JoiningDate, SalaryID, CredentialID, AddressID) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
            (first_name, last_name, cnic, license_no, joining_date, salary_id, credential_id, address_id)
        )
        print("Debug: Doctor record inserted successfully.")

        # Commit Transaction
        cursor.execute("COMMIT TRANSACTION;")
        conn.commit()
        print("Transaction executed successfully.")

        return True

    except Exception as e:
        # Rollback Transaction in case of error
        conn.rollback()
        print(f"Transaction failed: {e}")
        print(traceback.format_exc())
        return False

    finally:
        # Close the connection
        cursor.close()
        conn.close()


def update_salary(cnic, amount):
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Ensure the input amount is numeric and round it to 2 decimal places
        try:
            amount = round(float(amount), 2)
        except ValueError:
            print("Invalid salary amount. Must be numeric.")
            return False

        # Update query for the salary table
        query = """
            UPDATE TblSalary
            SET Amount = ?
            WHERE SalaryID = (SELECT SalaryID FROM TblDoctors WHERE CNIC = ?);
        """
        cursor.execute(query, (amount, cnic))
        conn.commit()

        # Check if any rows were updated
        if cursor.rowcount > 0:
            print("Salary updated successfully.")
            return True
        else:
            print("No record found for the provided CNIC.")
            return False

    except Exception as e:
        print(f"Database error: {e}")
        return False
    finally:
        if conn:
            conn.close()

def update_address(cnic, city, street, state, postal_code, country):
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE TblAddress
            SET city = ?, street = ?, state = ?, postal_code = ?, country = ?
            WHERE AddressID = (SELECT AddressID FROM TblDoctors WHERE CNIC = ?);
        """
        cursor.execute(query, (city, street, state, postal_code, country, cnic))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Database error: {e}")
        return False


def update_credentials(cnic, username, password):
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE TblCredentials
            SET Username = ?, PasswordHash = ?
            WHERE CredentialID = (SELECT CredentialID FROM TblDoctors WHERE CNIC = ?);
        """
        cursor.execute(query, (username, password, cnic))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Database error: {e}")
        return False

def update_personal_data(cnic, first_name, last_name, license_no, joining_date, job_status):
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Update query for the doctor table
        query = """
            UPDATE TblDoctors
            SET FirstName = ?, LastName = ?, LicenseNo = ?, JoiningDate = ?, JobStatus = ?
            WHERE CNIC = ?;
        """
        cursor.execute(query, (first_name, last_name, license_no, joining_date, job_status, cnic))
        conn.commit()
        conn.close()

        # Check if any rows were updated
        return cursor.rowcount > 0

    except Exception as e:
        print(f"Database error: {e}")
        return False

def view_all_doctors():
    try:
        # Establish database connection
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Query to fetch doctor details along with salary and address information
        cursor.execute("""
            SELECT 
                d.DoctorID, 
                d.FirstName, 
                d.LastName, 
                d.CNIC, 
                d.LicenseNo, 
                d.JoiningDate, 
                d.JobStatus, 
                s.Amount AS Salary,  -- Fetch salary amount from TblSalary
                c.Username AS CredentialUsername,  -- Fetch username from TblCredentials
                a.City AS AddressCity  -- Fetch city from TblAddress
            FROM TblDoctors d
            INNER JOIN TblCredentials c ON d.CredentialID = c.CredentialID
            INNER JOIN TblAddress a ON d.AddressID = a.AddressID
            INNER JOIN TblSalary s ON d.SalaryID = s.SalaryID;
        """)

        # Fetch all results and return them as a list of dictionaries
        doctors = []
        for row in cursor.fetchall():
            doctor = {
                "DoctorID": row[0],
                "FirstName": row[1],
                "LastName": row[2],
                "CNIC": row[3],
                "LicenseNo": row[4],
                "JoiningDate": row[5],
                "JobStatus": row[6],
                "Salary": row[7],  # Salary amount
                "CredentialUsername": row[8],  # Username from TblCredentials
                "AddressCity": row[9]  # City from TblAddress
            }
            doctors.append(doctor)

        return doctors

    except Exception as e:
        print(f"Error retrieving all doctors: {e}")
        return []

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

def search_doctor_by_cnic(cnic):
    try:
        # Open a connection to the database
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # Query to search for the doctor by CNIC
        query = """ 
            SELECT d.DoctorID, d.FirstName, d.LastName, d.CNIC, d.LicenseNo, d.JoiningDate, 
                   d.JobStatus, s.Amount AS Salary, c.Username, a.City
            FROM TblDoctors d
            INNER JOIN TblSalary s ON d.SalaryID = s.SalaryID
            INNER JOIN TblCredentials c ON d.CredentialID = c.CredentialID
            INNER JOIN TblAddress a ON d.AddressID = a.AddressID
            WHERE d.CNIC = ?
        """
        cursor.execute(query, (cnic,))
        doctor = cursor.fetchone()  # Fetch the first matching record

        # If a doctor is found, map the result to a dictionary
        if doctor:
            doctor_dict = {
                "DoctorID": doctor[0],
                "FirstName": doctor[1],
                "LastName": doctor[2],
                "CNIC": doctor[3],
                "LicenseNo": doctor[4],
                "JoiningDate": doctor[5],
                "JobStatus": doctor[6],
                "Salary": doctor[7],
                "Username": doctor[8],
                "City": doctor[9]
            }
            return doctor_dict
        else:
            # No doctor found with the given CNIC
            return None

    except Exception as e:
        print(f"An error occurred while searching for the doctor: {e}")
        return None

    finally:
        # Ensure the connection is closed properly
        if 'connection' in locals() and connection:
            connection.close()


def search_doctor_by_name(cnic):
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Query to fetch doctor data
        query = """
            SELECT d.FirstName, d.LastName, d.CNIC, d.LicenseNo, d.JoiningDate, d.JobStatus,
                   s.Amount, 
                   a.city, a.street, a.state, a.postal_code, a.country,
                   c.Username, c.PasswordHash
            FROM TblDoctors d
            LEFT JOIN TblSalary s ON d.SalaryID = s.SalaryID
            LEFT JOIN TblAddress a ON d.AddressID = a.AddressID
            LEFT JOIN TblCredentials c ON d.CredentialID = c.CredentialID
            WHERE d.CNIC = ?;
        """
        cursor.execute(query, (cnic,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                "FirstName": result[0],
                "LastName": result[1],
                "CNIC": result[2],
                "LicenseNo": result[3],
                "JoiningDate": result[4],
                "JobStatus": result[5],
                "Amount": result[6],
                "city": result[7],
                "street": result[8],
                "state": result[9],
                "postal_code": result[10],
                "country": result[11],
                "Username": result[12],
                "PasswordHash": result[13],
            }
        else:
            return None  # No doctor found with the provided CNIC

    except Exception as e:
        print(f"Database error: {e}")
        return None



def view_doctor_data(doctor_id):
    try:
        # Establish database connection
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Query to fetch doctor details along with credentials, salary, and address
        cursor.execute("""
            SELECT d.FirstName, d.LastName, d.CNIC, d.LicenseNo, d.JoiningDate, 
                   s.Amount AS Salary, c.Username, c.PasswordHash, a.City, a.Street, a.State, a.postal_code, a.Country, d.Status
            FROM TblDoctors d
            INNER JOIN TblCredentials c ON d.CredentialID = c.CredentialID
            INNER JOIN TblSalary s ON d.SalaryID = s.SalaryID
            INNER JOIN TblAddress a ON d.AddressID = a.AddressID
            WHERE d.DoctorID = ?;
        """, (doctor_id,))

        # Fetch the result and convert it to a dictionary
        result = cursor.fetchone()
        if result:
            doctor_data = {
                "FirstName": result[0],
                "LastName": result[1],
                "CNIC": result[2],
                "LicenseNo": result[3],
                "JoiningDate": result[4],
                "Salary": result[5],
                "Username": result[6],
                "PasswordHash": result[7],
                "City": result[8],
                "Street": result[9],
                "State": result[10],
                "PostalCode": result[11],
                "Country": result[12],
                "Status": result[13]
            }
            return doctor_data
        else:
            return None  # Return None if no doctor found with the given ID

    except Exception as e:
        print(f"Error retrieving doctor data: {e}")
        return None

    finally:
        cursor.close()
        conn.close()


def view_doctor_credentials(doctor_id):
    try:
        # Establish database connection
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Query to fetch doctor's credentials
        cursor.execute("""
            SELECT c.Username, c.PasswordHash
            FROM TblDoctors d
            INNER JOIN TblCredentials c ON d.CredentialID = c.CredentialID
            WHERE d.DoctorID = ?;
        """, (doctor_id,))

        # Fetch the result and return it as a dictionary
        result = cursor.fetchone()
        if result:
            credentials = {
                "Username": result[0],
                "PasswordHash": result[1]
            }
            return credentials
        else:
            return None  # Return None if no credentials found

    except Exception as e:
        print(f"Error retrieving doctor credentials: {e}")
        return None

    finally:
        cursor.close()
        conn.close()


def view_doctor_salary(doctor_id):
    try:
        # Establish database connection
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Query to fetch doctor's salary
        cursor.execute("""
            SELECT s.Amount
            FROM TblDoctors d
            INNER JOIN TblSalary s ON d.SalaryID = s.SalaryID
            WHERE d.DoctorID = ?;
        """, (doctor_id,))

        # Fetch the result and return the salary
        result = cursor.fetchone()
        if result:
            return {"Salary": result[0]}
        else:
            return None  # Return None if no salary found

    except Exception as e:
        print(f"Error retrieving doctor salary: {e}")
        return None

    finally:
        cursor.close()
        conn.close()


def view_doctor_address(doctor_id):
    try:
        # Establish database connection
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Query to fetch doctor's address
        cursor.execute("""
            SELECT a.City, a.Street, a.State, a.postal_code, a.Country
            FROM TblDoctors d
            INNER JOIN TblAddress a ON d.AddressID = a.AddressID
            WHERE d.DoctorID = ?;
        """, (doctor_id,))

        # Fetch the result and return the address
        result = cursor.fetchone()
        if result:
            address = {
                "City": result[0],
                "Street": result[1],
                "State": result[2],
                "PostalCode": result[3],
                "Country": result[4]
            }
            return address
        else:
            return None  # Return None if no address found

    except Exception as e:
        print(f"Error retrieving doctor address: {e}")
        return None

    finally:
        cursor.close()
        conn.close()