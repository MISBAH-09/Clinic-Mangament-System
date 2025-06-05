from DatabaseConnection import DatabaseConnection #type ignore
from PyQt5.QtWidgets import QMessageBox


def show_error(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Error")
    msg.setText(message)
    msg.exec_()

def show_success(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Success")
    msg.setText(message)
    msg.exec_()





def insert_medicine(medicine_name, active_ingredient, dosage, drug_type):
        """Inserts a new medicine record into TblMedicines."""
        try:
            # Establish connection to the database
            connection = DatabaseConnection.get_connection()
            cursor = connection.cursor()

            query = """
                INSERT INTO TblMedicines (MedicineName, ActiveIngredient, Dosage, DrugType) 
                VALUES (?,?,?,?)
            """
            cursor.execute(query, (medicine_name, active_ingredient, dosage, drug_type))
            # Commit the transaction
            connection.commit()

            # Show success message
            show_success("Patient data has been successfully saved.")
            return True  # Return True if insertion is successful

        except Exception as e:
            # Show error message if an exception occurs
            show_error(f"An error occurred while saving patient data: {e}")
            return False  # Return False if there is an error

        finally:
            # Ensure the database connection is closed
            if 'connection' in locals() and connection:
                connection.close()


def search_medicine_for_delete(medicine_name):
    """Search medicine from TblMedicines."""
    try:
        # Establish connection to the database
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # SQL Server syntax for executing stored procedure with a parameter
        query = "EXEC search_medicine_by_name @medicine_name = ?"
        cursor.execute(query, (medicine_name,))

        # Fetch the results (if any)
        result = cursor.fetchall()

        # If the result is empty, return None
        if not result:
            print(f"No results found for medicine: {medicine_name}")
            return None

        # If there are results, return the first one (assuming there is only one)
        return result[0]  # Assuming you want the first row if multiple rows are returned

    except Exception as e:
        print(f"An error occurred while searching for the medicine: {e}")
        show_error(f"An error occurred while searching medicine: {e}")
        return None  # Return None if there's an error
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()

def search_medicine_by_name(test_name):
    """Search test by name from TblTests."""
    try:
        # Establish connection to the database
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # SQL Server syntax for executing stored procedure with a parameter
        query = "EXEC search_medicine_by_name @medicine_name = ?"
        cursor.execute(query, (test_name,))

        # Fetch the results (if any)
        result = cursor.fetchall()

        # If the result is empty, return None
        if not result:
            print(f"No results found for test: {test_name}")
            return None

        # Return the first result (assuming the search should return only one test)
        # result[0] contains the first row (TestID, TestName)
        return {"MedicineID": result[0][0], "MedicineName": result[0][1], "ActiveIngredient": result[0][2], "Dosage": result[0][3], "DrugType": result[0][4] }  # Return as a dictionary

    except Exception as e:
        print(f"An error occurred while searching for the test: {e}")
        show_error(f"An error occurred while searching for the test: {e}")
        return None  # Return None if there's an error
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()



def delete_medicine_by_name(medicine_name):
    """Delete a medicine from TblMedicines by its name."""
    try:
        # Establish connection to the database
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # SQL query to delete the medicine by its name using parameterized query
        delete_query = "DELETE FROM TblMedicines WHERE MedicineName = ?"

        # Execute the query with the parameter
        cursor.execute(delete_query, (medicine_name,))  # Note the tuple (medicine_name,)

        # Commit the transaction to apply changes
        connection.commit()

        # Check if any rows were affected (i.e., the medicine was deleted)
        if cursor.rowcount > 0:
            print(f"Medicine '{medicine_name}' deleted successfully.")
            return True
        else:
            print(f"Medicine '{medicine_name}' not found.")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        # Ensure the database connection is closed
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()

def insert_tests(test_names):
    """Inserts multiple tests into the TblTests table using MySQL."""
    try:
        # Get database connection
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # MySQL uses %s as the placeholder for parameterized queries
        query = """
            INSERT INTO TblTests (TestName) 
            VALUES (?)
        """

        # Loop through test_names to insert each test
        for test_name in test_names:
            cursor.execute(query, (test_name,))  # Pass parameters as a tuple

        # Commit the transaction
        connection.commit()

        print("Test details have been successfully submitted.")
        return True  # Indicate success

    except Exception as e:
        # Log the error details for debugging
        print(f"Error type: {type(e).__name__}, Error: {e}")
        return False  # Indicate failure

    finally:
        # Ensure the connection is closed
        if 'connection' in locals() and connection:
            connection.close()


def search_test_for_delete(test_name):
    """Search medicine from TblMedicines."""
    try:
        # Establish connection to the database
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # SQL Server syntax for executing stored procedure with a parameter
        query = "EXEC search_test_by_name @test_name = ?"
        cursor.execute(query, (test_name,))

        # Fetch the results (if any)
        result = cursor.fetchall()

        # If the result is empty, return None
        if not result:
            print(f"No results found for medicine: {test_name}")
            return None

        # If there are results, return the first one (assuming there is only one)
        return result[0]  # Assuming you want the first row if multiple rows are returned

    except Exception as e:
        print(f"An error occurred while searching for the test: {e}")
        show_error(f"An error occurred while searching test: {e}")
        return None  # Return None if there's an error
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()

def search_test_by_name(test_name):
    """Search test by name from TblTests."""
    try:
        # Establish connection to the database
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # SQL Server syntax for executing stored procedure with a parameter
        query = "EXEC search_test_by_name @test_name = ?"
        cursor.execute(query, (test_name,))

        # Fetch the results (if any)
        result = cursor.fetchall()

        # If the result is empty, return None
        if not result:
            print(f"No results found for test: {test_name}")
            return None

        # Return the first result (assuming the search should return only one test)
        # result[0] contains the first row (TestID, TestName)
        return {"TestID": result[0][0], "TestName": result[0][1]}  # Return as a dictionary

    except Exception as e:
        print(f"An error occurred while searching for the test: {e}")
        show_error(f"An error occurred while searching for the test: {e}")
        return None  # Return None if there's an error
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()

import sqlite3

# Assuming you have a DatabaseConnection class with a get_connection method.
# If not, replace the connection code with your own database connection logic.


def search_medicine_for_update(medicine_id=None, medicine_name=None):
    try:
        # Connect to the database
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Build the SQL query based on the available parameters (ID or Name)
        if medicine_id:
            query = """
                SELECT MedicineID, MedicineName, ActiveIngredient, Dosage, DrugType
                FROM TblMedicines
                WHERE MedicineID = ?
            """
            cursor.execute(query, (medicine_id,))
        elif medicine_name:
            query = """
                SELECT MedicineID, MedicineName, ActiveIngredient, Dosage, DrugType
                FROM TblMedicines
                WHERE MedicineName LIKE ?
            """
            cursor.execute(query, (f"%{medicine_name}%",))
        else:
            raise ValueError("Either Medicine ID or Medicine Name must be provided.")

        # Fetch the result
        medicine = cursor.fetchone()

        if medicine:
            return medicine
        else:
            return None  # No match found

    except Exception as e:
        print(f"Error in search_medicine_for_update: {e}")
        raise

    finally:
        # Close the connection
        if conn:
            conn.close()


def delete_test_by_name(test_name):
    """Delete a medicine from TblMedicines by its name."""
    try:
        # Establish connection to the database
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # SQL query to delete the medicine by its name using parameterized query
        delete_query = "DELETE FROM TblTests WHERE TestName = ?"

        # Execute the query with the parameter
        cursor.execute(delete_query, (test_name,))  # Note the tuple (medicine_name,)

        # Commit the transaction to apply changes
        connection.commit()

        # Check if any rows were affected (i.e., the medicine was deleted)
        if cursor.rowcount > 0:
            print(f"Medicine '{test_name}' deleted successfully.")
            return True
        else:
            print(f"Medicine '{test_name}' not found.")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        # Ensure the database connection is closed
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()

def view_tests():
    try:
        # Establish database connection
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Query to fetch test details from the TblTests table
        cursor.execute("SELECT TestID, TestName FROM TblTests")

        # Fetch all results and return them as a list of dictionaries
        tests = []
        for row in cursor.fetchall():
            test = {
                "TestID": row[0],
                "TestName": row[1],
            }
            tests.append(test)

        print("Fetched Test Data:", tests)  # Debugging line to print fetched data
        return tests

    except Exception as e:
        print(f"Error retrieving test data: {e}")
        return []

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

def view_medicines():
    try:
        # Establish database connection
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Query to fetch test details from the TblTests table
        cursor.execute("SELECT MedicineID, MedicineName, ActiveIngredient, Dosage, DrugType FROM TblMedicines")

        # Fetch all results and return them as a list of dictionaries
        medicines = []
        for row in cursor.fetchall():
            test = {
                "MedicineID": row[0],
                "MedicineName": row[1],
                "ActiveIngredient": row[2],
                "Dosage": row[3],
                "DrugType": row[4],
            }
            medicines.append(test)

        print("Fetched Test Data:", medicines)  # Debugging line to print fetched data
        return medicines

    except Exception as e:
        print(f"Error retrieving test data: {e}")
        return []

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()


def update_medicine_inventory(medicine_id, name, active_ingredient, dosage, drug_type):
    try:
        # Connect to your database
        conn = DatabaseConnection.get_connection()  # Ensure DatabaseConnection is correctly implemented
        cursor = conn.cursor()

        # SQL query to update the medicine record based on both MedicineID and MedicineName
        cursor.execute("""
            UPDATE TblMedicines
            SET MedicineName = ?, ActiveIngredient = ?, Dosage = ?, DrugType = ?
            WHERE MedicineID = ? AND MedicineName = ?
        """, (name, active_ingredient, dosage, drug_type, medicine_id, name))  # Using both ID and name as conditions

        # Commit the changes
        conn.commit()

        if cursor.rowcount == 0:
            raise Exception("No matching medicine found with the provided ID and name.")

        print(f"Medicine with ID {medicine_id} and Name {name} updated successfully.")

    except Exception as e:
        print(f"Error in update_medicine_inventory: {e}")
        raise  # Raise the exception to propagate it to the frontend

    finally:
        # Close the connection
        if conn:
            conn.close()
