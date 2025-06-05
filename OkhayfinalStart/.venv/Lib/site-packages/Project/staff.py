from DatabaseConnection import DatabaseConnection

def fetch_all_roles():
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT RoleName FROM TblRoles")
        roles = cursor.fetchall()
        return [role[0] for role in roles]
    except Exception as e:
        print(f"Error fetching roles: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def select_role_id(roleName):
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TblRoles WHERE RoleName = ?", (roleName,))
    roleid = cursor.fetchone()
    return roleid

def execute_transaction(first_name, last_name, cnic, joining_date, 
                        city, street, state, postal_code, country, username, 
                        password_hash, role_id, salary_amount):
    try:
        conn = DatabaseConnection.get_connection()
        conn.autocommit = False
        cursor = conn.cursor()
        cursor.execute("BEGIN TRANSACTION;")

        cursor.execute(
            "INSERT INTO TblAddress (city, street, state, postal_code, country) "
            "OUTPUT INSERTED.AddressID "
            "VALUES (?, ?, ?, ?, ?);",
            (city, street, state, postal_code, country)
        )
        address_id = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO TblCredentials (Username, PasswordHash, RoleID) "
            "OUTPUT INSERTED.CredentialID "
            "VALUES (?, ?, ?);",
            (username, password_hash, role_id)
        )
        credential_id = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO TblSalary (Amount) OUTPUT INSERTED.SalaryID VALUES (?);",
            (salary_amount,)
        )
        salary_id = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO TblStaff (FirstName, LastName, CNIC, JoiningDate, SalaryID, CredentialID, AddressID, Status) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, 'active');",
            (first_name, last_name, cnic, joining_date, salary_id, credential_id, address_id)
        )

        cursor.execute("COMMIT TRANSACTION;")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Transaction failed: {e}")
    finally:
        cursor.close()
        conn.close()

def update_salary(staff_id, new_salary):
    try:
        conn = DatabaseConnection.get_connection()
        conn.autocommit = False
        cursor = conn.cursor()
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute(
            "UPDATE TblSalary SET Amount = ? WHERE SalaryID = (SELECT SalaryID FROM TblStaff WHERE StaffID = ?);",
            (new_salary, staff_id)
        )
        cursor.execute("COMMIT TRANSACTION;")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Transaction failed: {e}")
    finally:
        cursor.close()
        conn.close()

def update_address(staff_id, new_city, new_street, new_state, new_postal_code, new_country):
    try:
        conn = DatabaseConnection.get_connection()
        conn.autocommit = False
        cursor = conn.cursor()
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute(
            "UPDATE TblAddress SET city = ?, street = ?, state = ?, postal_code = ?, country = ? "
            "WHERE AddressID = (SELECT AddressID FROM TblStaff WHERE StaffID = ?);",
            (new_city, new_street, new_state, new_postal_code, new_country, staff_id)
        )
        cursor.execute("COMMIT TRANSACTION;")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Transaction failed: {e}")
    finally:
        cursor.close()
        conn.close()

def update_username(staff_id, new_username):
    try:
        conn = DatabaseConnection.get_connection()
        conn.autocommit = False
        cursor = conn.cursor()
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute(
            "UPDATE TblCredentials SET Username = ? "
            "WHERE CredentialID = (SELECT CredentialID FROM TblStaff WHERE StaffID = ?);",
            (new_username, staff_id)
        )
        cursor.execute("COMMIT TRANSACTION;")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Transaction failed: {e}")
    finally:
        cursor.close()
        conn.close()

def update_password(staff_id, new_password_hash):
    try:
        conn = DatabaseConnection.get_connection()
        conn.autocommit = False
        cursor = conn.cursor()
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute(
            "UPDATE TblCredentials SET PasswordHash = ? "
            "WHERE CredentialID = (SELECT CredentialID FROM TblStaff WHERE StaffID = ?);",
            (new_password_hash, staff_id)
        )
        cursor.execute("COMMIT TRANSACTION;")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Transaction failed: {e}")
    finally:
        cursor.close()
        conn.close()

def deactivate_staff(staff_id):
    try:
        conn = DatabaseConnection.get_connection()
        conn.autocommit = False
        cursor = conn.cursor()
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute(
            "UPDATE TblStaff SET Status = 'inactive' WHERE StaffID = ?;",
            (staff_id,)
        )
        cursor.execute("COMMIT TRANSACTION;")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Transaction failed: {e}")
    finally:
        cursor.close()
        conn.close()


def view_all_staff():
    try:
        # Establish database connection
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Query to fetch staff details along with address and credentials
        cursor.execute("""
            SELECT s.StaffID, s.FirstName, s.LastName, s.Status, c.Username, a.City
            FROM TblStaff s
            INNER JOIN TblCredentials c ON s.CredentialID = c.CredentialID
            INNER JOIN TblAddress a ON s.AddressID = a.AddressID;
        """)

        # Fetch all results and return them as a list of dictionaries
        staff_list = []
        for row in cursor.fetchall():
            staff = {
                "StaffID": row[0],
                "FirstName": row[1],
                "LastName": row[2],
                "Status": row[3],
                "Username": row[4],
                "City": row[5]
            }
            staff_list.append(staff)

        return staff_list

    except Exception as e:
        print(f"Error retrieving all staff: {e}")
        return []

    finally:
        cursor.close()
        conn.close()



def view_staff_data(staff_id):
    try:
        # Establish database connection
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Query to fetch staff details with credentials and address
        cursor.execute("""
            SELECT s.FirstName, s.LastName, s.CNIC, s.JoiningDate, 
                   c.Username, a.City, a.Street, a.State, a.postal_code, a.Country, s.Status
            FROM TblStaff s
            INNER JOIN TblCredentials c ON s.CredentialID = c.CredentialID
            INNER JOIN TblAddress a ON s.AddressID = a.AddressID
            WHERE s.StaffID = ?;
        """, (staff_id,))

        # Fetch the result and convert it to a dictionary
        result = cursor.fetchone()
        if result:
            staff_data = {
                "FirstName": result[0],
                "LastName": result[1],
                "CNIC": result[2],
                "JoiningDate": result[3],
                "Username": result[4],
                "City": result[5],
                "Street": result[6],
                "State": result[7],
                "PostalCode": result[8],
                "Country": result[9],
                "Status": result[10]
            }
            return staff_data
        else:
            return None

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

        # Query to fetch staff credentials
        cursor.execute("""
            SELECT c.Username, c.PasswordHash
            FROM TblStaff s
            INNER JOIN TblCredentials c ON s.CredentialID = c.CredentialID
            WHERE s.StaffID = ?;
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
            return None

    except Exception as e:
        print(f"Error retrieving staff credentials: {e}")
        return None

    finally:
        cursor.close()
        conn.close()


def view_staff_address(staff_id):
    try:
        # Establish database connection
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Query to fetch staff address
        cursor.execute("""
            SELECT a.City, a.Street, a.State, a.postal_code, a.Country
            FROM TblStaff s
            INNER JOIN TblAddress a ON s.AddressID = a.AddressID
            WHERE s.StaffID = ?;
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
            return None

    except Exception as e:
        print(f"Error retrieving staff address: {e}")
        return None

    finally:
        cursor.close()
        conn.close()



def view_staff_by_role(role_name):
    try:
        # Establish database connection
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Query to fetch staff details based on the role name
        cursor.execute("""
            SELECT s.StaffID, s.FirstName, s.LastName, s.Status, c.Username, a.City, r.RoleName
            FROM TblStaff s
            INNER JOIN TblCredentials c ON s.CredentialID = c.CredentialID
            INNER JOIN TblAddress a ON s.AddressID = a.AddressID
            INNER JOIN TblRoles r ON s.RoleID = r.RoleID
            WHERE r.RoleName = ?;
        """, (role_name,))

        # Fetch all results and return them as a list of dictionaries
        staff_list = []
        for row in cursor.fetchall():
            staff = {
                "StaffID": row[0],
                "FirstName": row[1],
                "LastName": row[2],
                "Status": row[3],
                "Username": row[4],
                "City": row[5],
                "RoleName": row[6]
            }
            staff_list.append(staff)

        return staff_list

    except Exception as e:
        print(f"Error retrieving staff by role '{role_name}': {e}")
        return []

    finally:
        cursor.close()
        conn.close()
