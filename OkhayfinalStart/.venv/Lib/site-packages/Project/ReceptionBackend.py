from DatabaseConnection import DatabaseConnection  # type: ignore
from PyQt5.QtWidgets import QMessageBox  # type: ignore


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

def all_doctors():
    try:
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT DoctorID, FirstName, LastName FROM TblDoctors;")
        doctors = cursor.fetchall()

        doctor_list = []
        for doctor in doctors:
            doctor_dict = {'DoctorID': doctor[0], 'FirstName': doctor[1], 'LastName': doctor[2]}
            doctor_list.append(doctor_dict)

        return doctor_list
    except Exception as e:
        show_error(f"Error fetching doctors: {e}")
        return []  # Return an empty list if there's an error

def get_doctor_id_from_full_name(full_name):
    try:
        # Open a connection to the database
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # Split the full name into first name and last name
        names = full_name.split(" ", 1)
        if len(names) != 2:
            raise ValueError("Invalid full name format. Ensure it includes both first and last name.")

        first_name, last_name = names

        # Query to call the stored procedure to get the doctor ID
        query = """
            DECLARE @DoctorID INT;
            EXEC GetDoctorID @FirstName = ?, @LastName = ?, @DoctorID = @DoctorID OUTPUT;
            SELECT @DoctorID;
        """
        cursor.execute(query, (first_name, last_name))

        # Fetch the doctor ID
        result = cursor.fetchone()
        doctor_id = result[0] if result else None

        # Return the doctor ID
        return doctor_id

    except ValueError as ve:
        print(f"Value Error: {ve}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        # Ensure the database connection is closed
        if 'connection' in locals() and connection:
            connection.close()

def save_visit_data(patient_id, doctor_id, consultancy_fees):
    """
    Saves a visit record into the TblVisits table and records the payment in TblPayments.
    """
    try:
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # Insert the visit data into TblVisits and retrieve the generated VisitID
        visit_query = """
            INSERT INTO TblVisits (PatientID, DoctorID, VisitDate)
            VALUES (?, ?, GETDATE());
        """
        cursor.execute(visit_query, (patient_id, doctor_id))

        # Retrieve the last inserted VisitID using SCOPE_IDENTITY()
        visit_id_query = "SELECT SCOPE_IDENTITY();"
        cursor.execute(visit_id_query)
        visit_id = cursor.fetchone()[0]  # Get the generated VisitID

        # Insert payment data into TblPayments
        payment_query = """
            INSERT INTO TblPayments (PatientID, VisitID, CheckupFee)
            VALUES (?, ?, ?);
        """
        cursor.execute(payment_query, (patient_id, visit_id, consultancy_fees))

        # Commit the transaction
        connection.commit()

        return True  # Indicate that the visit and payment data were saved successfully

    except Exception as e:
        print(f"Error in save_visit_data: {e}")
        if 'connection' in locals() and connection:
            connection.rollback()  # Rollback if any error occurs
        return False  # Indicate failure

    finally:
        # Ensure the connection is always closed
        if 'connection' in locals() and connection:
            connection.close()

def submit_patient_data(first_name, last_name, cnic, dob, gender, contact_number, email, address, date_registered, referred_doctor, consultancy_fees):
    try:
        # Ensure consultancy fees are not negative
        if consultancy_fees < 0:
            raise ValueError("Checkup fee cannot be negative.")

        # Get doctor ID
        doctor_id = get_doctor_id_from_full_name(referred_doctor)
        if not doctor_id:
            raise ValueError("Doctor ID not found.")
        print(doctor_id)

        # Connect to the database
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        cursor.execute("SET NOCOUNT ON;")

        # Insert patient data
        patient_query = """
            INSERT INTO TblPatients (FirstName, LastName, CNIC, DateOfBirth, Gender, ContactNumber, Email, Address, DateRegistered)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            SELECT SCOPE_IDENTITY();
        """
        cursor.execute(patient_query, (first_name, last_name, cnic, dob, gender, contact_number, email, address, date_registered))
        patient_id = cursor.fetchone()[0]

        # Insert visit data
        visit_query = """
            INSERT INTO TblVisits (PatientID, DoctorID, VisitDate)
            VALUES (?, ?, ?);
            SELECT SCOPE_IDENTITY();
        """
        cursor.execute(visit_query, (patient_id, doctor_id, date_registered))
        visit_id = cursor.fetchone()[0]

        # Insert payment data
        payment_query = """
            INSERT INTO TblPayments (PatientID, VisitID, CheckupFee)
            VALUES (?, ?, ?);
        """
        cursor.execute(payment_query, (patient_id, visit_id, consultancy_fees))

        # Commit transaction
        connection.commit()

        return True  # Success

    except Exception as e:
        print(f"Error in submit_patient_data: {e}")
        if 'connection' in locals() and connection:
            connection.rollback()  # Rollback if any error occurs
        return False  # Failure

    finally:
        if 'connection' in locals() and connection:
            connection.close()  # Ensure the connection is always closed

def search_patient_by_cnic(cnic):
    try:
        # Open a connection to the database
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # Query to search for the patient by CNIC
        query = "SELECT * FROM TblPatients WHERE CNIC = ?"
        cursor.execute(query, (cnic,))
        patient = cursor.fetchone()  # Fetch the first matching record

        # Return the patient record
        return patient

    except Exception as e:
        show_error(f"An error occurred while searching for the patient: {e}")
        return None

    finally:
        # Ensure the connection is closed properly
        if 'connection' in locals() and connection:
            connection.close()

def update_patient_data(patient_id, first_name, last_name, dob, gender, contact_number, email, address, date_registered):
    connection = None
    try:
        # Open a fresh connection
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # Query to update patient details
        query = """
            UPDATE TblPatients
            SET FirstName = ?, LastName = ?, DateOfBirth = ?, Gender = ?, 
                ContactNumber = ?, Email = ?, Address = ?, DateRegistered = ?
            WHERE PatientID = ?
        """
        cursor.execute(query, (first_name, last_name, dob, gender, contact_number, email, address, date_registered, patient_id))

        # Commit the changes
        connection.commit()
        return True  # Indicate success

    except Exception as e:
        # Catch and log the exception
        show_error(f"An error occurred while updating the patient data: {e}")
        return False  # Indicate failure

    finally:
        # Ensure the connection is always closed
        if 'connection' in locals() and connection:
            connection.close()

def delete_patient_by_cnic(cnic):
    try:
        # Open a connection to the database
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # Check if the patient exists
        query_check = "SELECT * FROM TblPatients WHERE CNIC = ?"
        cursor.execute(query_check, (cnic,))
        patient = cursor.fetchone()

        if not patient:
            show_error(f"No patient found with CNIC {cnic}.")
            return False

        # Query to delete the patient
        query_delete = "DELETE FROM TblPatients WHERE CNIC = ?"
        cursor.execute(query_delete, (cnic,))

        # Commit the changes
        connection.commit()

        # Show success message
        show_success(f"Patient with CNIC {cnic} has been successfully deleted.")
        return True

    except Exception as e:
        # Catch and log the exception
        show_error(f"An error occurred while deleting the patient: {e}")
        return False

    finally:
        # Ensure the connection is always closed
        if 'connection' in locals() and connection:
            connection.close()

def view_patient_data():
    """
    Retrieve all patient data from the TblPatients table.

    Returns:
        list: A list of tuples where each tuple represents a patient's record.
        None: If an error occurs.
    """
    try:
        # Establish a connection to the database
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # Query to retrieve all patient data
        query = "SELECT * FROM TblPatients"
        cursor.execute(query)

        # Fetch all records
        patients = cursor.fetchall()

        # Return the retrieved data
        return patients

    except Exception as e:
        # Show error if an exception occurs
        show_error(f"An error occurred while retrieving patient data: {e}")
        return None

    finally:
        # Ensure the connection is closed
        if 'connection' in locals() and connection:
            connection.close()