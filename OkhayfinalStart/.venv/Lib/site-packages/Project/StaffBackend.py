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


def get_distinct_role_names():
    """
    Calls the stored procedure GetDistinctRoleNames and returns distinct role names in a list.

    :param db_connection: An instance of DatabaseConnection with an established connection.
    :return: A list of distinct role names or an empty list if an error occurs.
    """
    role_names = []
    
    try:
        conn = DatabaseConnection.get_connection()
        conn.autocommit = False  # Disable autocommit for transaction
        cursor = conn.cursor()
        cursor.execute("EXEC GetDistinctRoleNames")
        
        # Fetch all results
        role_names = [row[0] for row in cursor.fetchall()]
    
    except Exception as e:
        error_message = f"An error occurred while fetching distinct role names: {str(e)}"
        show_error(error_message)
        print(traceback.format_exc())  # Log the full traceback for debugging
    
    return role_names
def get_role_id(role_name):
    try:
        # Establish database connection
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Define the SQL command to execute the stored procedure
        sql = """
            DECLARE @RoleID INT;
            EXEC GetRoleID @RoleName = ?, @RoleID = @RoleID OUTPUT;
            SELECT @RoleID AS RoleID;
        """

        # Execute the stored procedure and pass the parameters
        cursor.execute(sql, (role_name,))

        # Fetch the RoleID from the result set
        result = cursor.fetchone()
        if result:
            role_id = result[0]
            return role_id
        else:
            return None

    except Exception as e:
        print(f"An error occurred while fetching the RoleID: {e}")
        return None

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()
     
def execute_staff_transaction(first_name, last_name, cnic, joining_date,
                               city, street, state, postal_code, country, username,
                               password_hash, salary_amount, role_name):
    try:
        # Establish database connection
        conn = DatabaseConnection.get_connection()
        conn.autocommit = False  # Disable autocommit for transaction
        cursor = conn.cursor()

        # Get the RoleID based on role_name
        role_id = get_role_id(role_name)
        if role_id is None:
            raise ValueError("Invalid role name provided.")

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
            (username, password_hash, role_id)
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

        # Insert into TblStaff
        cursor.execute(
            "INSERT INTO TblStaff (FirstName, LastName, CNIC, JoiningDate, SalaryID, CredentialID, AddressID) "
            "VALUES (?, ?, ?, ?, ?, ?, ?);",
            (first_name, last_name, cnic, joining_date, salary_id, credential_id, address_id)
        )
        print("Debug: Staff record inserted successfully.")

        # Commit Transaction
        cursor.execute("COMMIT TRANSACTION;")
        conn.commit()
        print("Transaction executed successfully.")

        return True  # Indicate success

    except Exception as e:
        # Rollback Transaction in case of error
        conn.rollback()
        print(f"Transaction failed: {e}")
        print(traceback.format_exc())
        return False  # Indicate failure

    finally:
        # Close the connection
        cursor.close()
        conn.close()



def update_staff_salary(cnic, amount):
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
            WHERE SalaryID = (SELECT SalaryID FROM TblStaff WHERE CNIC = ?);
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

def update_staff_address(cnic, city, street, state, postal_code, country):
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE TblAddress
            SET city = ?, street = ?, state = ?, postal_code = ?, country = ?
            WHERE AddressID = (SELECT AddressID FROM TblStaff WHERE CNIC = ?);
        """
        cursor.execute(query, (city, street, state, postal_code, country, cnic))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Database error: {e}")
        return False


def update_staff_credentials(cnic, username, password):
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE TblCredentials
            SET Username = ?, PasswordHash = ?
            WHERE CredentialID = (SELECT CredentialID FROM TblStaff WHERE CNIC = ?);
        """
        cursor.execute(query, (username, password, cnic))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Database error: {e}")
        return False

def update_staff_personal_data(cnic, first_name, last_name, joining_date, job_status):
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Update query for the doctor table
        query = """
            UPDATE TblStaff
            SET FirstName = ?, LastName = ?, JoiningDate = ?, JobStatus = ?
            WHERE CNIC = ?;
        """
        cursor.execute(query, (first_name, last_name, joining_date, job_status, cnic))
        conn.commit()
        conn.close()

        # Check if any rows were updated
        return cursor.rowcount > 0

    except Exception as e:
        print(f"Database error: {e}")
        return False

def view_all_staff():
    try:
        # Establish database connection
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Query to fetch staff details along with salary and address information
        cursor.execute("""
            SELECT 
                st.StaffID, 
                st.FirstName, 
                st.LastName, 
                st.CNIC, 
                st.JoiningDate, 
                st.JobStatus, 
                s.Amount AS Salary,  -- Fetch salary amount from TblSalary
                c.Username AS CredentialUsername,  -- Fetch username from TblCredentials
                a.City AS AddressCity  -- Fetch city from TblAddress
            FROM TblStaff st
            INNER JOIN TblCredentials c ON st.CredentialID = c.CredentialID
            INNER JOIN TblAddress a ON st.AddressID = a.AddressID
            INNER JOIN TblSalary s ON st.SalaryID = s.SalaryID;
        """)

        # Fetch all results and return them as a list of dictionaries
        staff_list = []
        for row in cursor.fetchall():
            staff = {
                "StaffID": row[0],
                "FirstName": row[1],
                "LastName": row[2],
                "CNIC": row[3],
                "JoiningDate": row[4],
                "JobStatus": row[5],
                "Salary": row[6],  # Salary amount
                "CredentialUsername": row[7],  # Username from TblCredentials
                "AddressCity": row[8]  # City from TblAddress
            }
            staff_list.append(staff)

        return staff_list

    except Exception as e:
        print(f"Error retrieving all staff: {e}")
        return []

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()
def search_staff_by_cnic(cnic):
    try:
        # Open a connection to the database
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # Query to search for the staff member by CNIC
        query = """ 
            SELECT st.StaffID, st.FirstName, st.LastName, st.CNIC, st.JoiningDate, 
                   st.JobStatus, s.Amount AS Salary, c.Username, a.City
            FROM TblStaff st
            INNER JOIN TblSalary s ON st.SalaryID = s.SalaryID
            INNER JOIN TblCredentials c ON st.CredentialID = c.CredentialID
            INNER JOIN TblAddress a ON st.AddressID = a.AddressID
            WHERE st.CNIC = ?
        """
        cursor.execute(query, (cnic,))
        staff = cursor.fetchone()  # Fetch the first matching record

        # If a staff member is found, map the result to a dictionary
        if staff:
            staff_dict = {
                "StaffID": staff[0],
                "FirstName": staff[1],
                "LastName": staff[2],
                "CNIC": staff[3],
                "JoiningDate": staff[4],
                "JobStatus": staff[5],
                "Salary": staff[6],
                "Username": staff[7],
                "City": staff[8]
            }
            return staff_dict
        else:
            # No staff member found with the given CNIC
            return None

    except Exception as e:
        print(f"An error occurred while searching for the staff: {e}")
        return None

    finally:
        # Ensure the connection is closed properly
        if 'connection' in locals() and connection:
            connection.close()

def search_staff_by_name(cnic):
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Query to fetch doctor data
        query = """
            SELECT st.FirstName, st.LastName, st.CNIC, st.JoiningDate, st.JobStatus,
                   s.Amount, 
                   a.city, a.street, a.state, a.postal_code, a.country,
                   c.Username, c.PasswordHash
            FROM TblStaff st
            LEFT JOIN TblSalary s ON st.SalaryID = s.SalaryID
            LEFT JOIN TblAddress a ON st.AddressID = a.AddressID
            LEFT JOIN TblCredentials c ON st.CredentialID = c.CredentialID
            WHERE st.CNIC = ?;
        """
        cursor.execute(query, (cnic,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                "FirstName": result[0],
                "LastName": result[1],
                "CNIC": result[2],
                # "LicenseNo": result[3],
                "JoiningDate": result[3],
                "JobStatus": result[4],
                "Amount": result[5],
                "city": result[6],
                "street": result[7],
                "state": result[8],
                "postal_code": result[9],
                "country": result[10],
                "Username": result[11],
                "PasswordHash": result[12],
            }
        else:
            return None  # No doctor found with the provided CNIC

    except Exception as e:
        print(f"Database error: {e}")
        return None



def view_staff_data(staff_id):
    try:
        # Establish database connection
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Query to fetch doctor details along with credentials, salary, and address
        cursor.execute("""
            SELECT st.FirstName, st.LastName, st.CNIC, st.JoiningDate, 
                   s.Amount AS Salary, c.Username, c.PasswordHash, a.City, a.Street, a.State, a.postal_code, a.Country, st.Status
            FROM TblStaff st
            INNER JOIN TblCredentials c ON st.CredentialID = c.CredentialID
            INNER JOIN TblSalary s ON st.SalaryID = s.SalaryID
            INNER JOIN TblAddress a ON st.AddressID = a.AddressID
            WHERE st.StaffID = ?;
        """, (staff_id,))

        # Fetch the result and convert it to a dictionary
        result = cursor.fetchone()
        if result:
            staff_data = {
                "FirstName": result[0],
                "LastName": result[1],
                "CNIC": result[2],
                # "LicenseNo": result[3],
                "JoiningDate": result[3],
                "JobStatus": result[4],
                "Amount": result[5],
                "city": result[6],
                "street": result[7],
                "state": result[8],
                "postal_code": result[9],
                "country": result[10],
                "Username": result[11],
                "PasswordHash": result[12],
            }
            return staff_data
        else:
            return None  # Return None if no staff found with the given ID

    except Exception as e:
        print(f"Error retrieving staff data: {e}")
        return None

    finally:
        cursor.close()
        conn.close()


def view_staff_credentials(staff_id):
    try:
        # Establish database connection
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Query to fetch doctor's credentials
        cursor.execute("""
            SELECT c.Username, c.PasswordHash
            FROM TblStaff st
            INNER JOIN TblCredentials c ON st.CredentialID = c.CredentialID
            WHERE st.StaffID = ?;
        """, (staff_id,))

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
        print(f"Error retrieving staff credentials: {e}")
        return None

    finally:
        cursor.close()
        conn.close()


def view_staff_salary(staff_id):
    try:
        # Establish database connection
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Query to fetch doctor's salary
        cursor.execute("""
            SELECT s.Amount
            FROM TblStaff st
            INNER JOIN TblSalary s ON st.SalaryID = s.SalaryID
            WHERE st.StaffID = ?;
        """, (staff_id,))

        # Fetch the result and return the salary
        result = cursor.fetchone()
        if result:
            return {"Salary": result[0]}
        else:
            return None  # Return None if no salary found

    except Exception as e:
        print(f"Error retrieving staff salary: {e}")
        return None

    finally:
        cursor.close()
        conn.close()


def view_staff_address(staff_id):
    try:
        # Establish database connection
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Query to fetch doctor's address
        cursor.execute("""
            SELECT a.City, a.Street, a.State, a.postal_code, a.Country
            FROM TblStaff st
            INNER JOIN TblAddress a ON st.AddressID = a.AddressID
            WHERE st.StaffID = ?;
        """, (staff_id,))

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
        print(f"Error retrieving staff address: {e}")
        return None

    finally:
        cursor.close()
        conn.close()