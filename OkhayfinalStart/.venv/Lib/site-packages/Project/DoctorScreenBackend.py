from DatabaseConnection import DatabaseConnection  # type: ignore
from PyQt5.QtWidgets import QMessageBox  # type: ignore
from datetime import datetime

def show_error(message):
    """Displays an error message in a pop-up."""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Error")
    msg.setText(message)
    msg.exec_()

def show_success(message):
    """Displays a success message in a pop-up."""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Success")
    msg.setText(message)
    msg.exec_()

def format_date(value):
    """Helper function to format datetime objects or convert strings to datetime."""
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")  # Format as YYYY-MM-DD
    return value  # Return as is if not a datetime object


def search_patient_by_visitID(visitID):
    """Search for a patient using VisitID and retrieve their details."""
    try:
        # Open a connection to the database
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # Query to find PatientID from TblVisits
        query_visit = "SELECT PatientID FROM TblVisits WHERE VisitID = ?"
        cursor.execute(query_visit, (visitID,))
        patient = cursor.fetchone()  # Fetch the first matching record
        print(f"Patient lookup by VisitID: {visitID}")

        if not patient:
            show_error("No patient found with the given VisitID.")
            return None

        patient_id = patient[0]  # Extract PatientID from the result
        print(f"PatientID found: {patient_id}")

        # Query to fetch full patient details from TblPatients
        query_patient = """
            SELECT PatientID, FirstName, LastName, CNIC, DateOfBirth, Gender, 
                   ContactNumber, Email, Address, DateRegistered
            FROM TblPatients
            WHERE PatientID = ?
        """
        cursor.execute(query_patient, (patient_id,))
        patient_details = cursor.fetchone()

        if not patient_details:
            show_error("No details found for the given PatientID.")
            return None

        print("Patient Details Fetched:")
        for field, value in zip(["PatientID", "First Name", "Last Name", "CNIC", "Date of Birth",
                                 "Gender", "Contact Number", "Email", "Address", "Date Registered"], patient_details):
            print(f"{field}: {value}")

        # Return full patient details as a dictionary, leaving the dates as datetime objects
        return {
            "PatientID": patient_details[0],
            "FirstName": patient_details[1],
            "LastName": patient_details[2],
            "CNIC": patient_details[3],
            "DateOfBirth": patient_details[4],  # Return as a datetime object
            "Gender": patient_details[5],
            "ContactNumber": patient_details[6],
            "Email": patient_details[7],
            "Address": patient_details[8],
            "DateRegistered": patient_details[9],  # Return as a datetime object
        }

    except Exception as e:
        show_error(f"An error occurred while retrieving patient data: {e}")
        return None

    finally:
        # Ensure the cursor and connection are closed properly
        try:
            if cursor:
                cursor.close()
        except Exception as close_error:
            print(f"Error closing cursor: {close_error}")
        finally:
            if 'connection' in locals() and connection:
                connection.close()


######################## medicine Page ############################

def get_medicines():
    # Connect to the database
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()

    # Query to fetch medicine names from the database
    cursor.execute("SELECT MedicineName FROM TblMedicines")
    medicines = cursor.fetchall()

    # Extract medicine names from query result
    medicine_names = [medicine[0] for medicine in medicines]

    # Close the connection
    conn.close()

    return medicine_names

def search_medicines(self, search_text):
    """Searches for medicines based on user input"""
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()

    # Use the stored procedure to search for medicines based on text input
    cursor.execute("EXEC search_medicine_by_name @medicine_name=?", (search_text,))
    medicines = cursor.fetchall()

    # Extract medicine names from query result
    medicine_names = [medicine[0] for medicine in medicines]

    # Close the connection
    conn.close()

    return medicine_names

def get_test():
    # Connect to the database
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()

    # Query to fetch medicine names from the database
    cursor.execute("SELECT TestName FROM TblTests")
    tests = cursor.fetchall()

    # Extract medicine names from query result
    tests_names = [tests[0] for tests in tests]

    # Close the connection
    conn.close()

    return tests_names

def search_tests(self, search_text):
        """Searches for medicines based on user input"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        # Query to search for medicines based on text input
        cursor.execute("EXEC search_test_by_name @test_name=?")
        tests = cursor.fetchall()

        # Extract medicine names from query result
        tests_names = [tests[0] for tests in tests]

        # Close the connection
        conn.close()

        return tests_names

def fetch_medicine_ids(selected_medicines):
    """Fetch the medicine IDs based on the selected medicine names"""
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    medicine_ids = []

    try:
        for med_name in selected_medicines:
            # Prepare the procedure call with output parameter
            cursor.execute("""
                DECLARE @MedID INT;
                EXEC GetMedID @Medname=?, @MedID=@MedID OUTPUT;
                SELECT @MedID;
            """, med_name)
            
            # Fetch the result
            result = cursor.fetchone()

            if result and result[0] is not None:
                medicine_ids.append(result[0])
            else:
                print(f"Medicine ID not found for {med_name}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()

    return medicine_ids

def fetch_test_ids(selected_tests):
    """Fetch the test IDs based on the selected test names"""
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    test_ids = []

    try:
        for test_name in selected_tests:
            # Prepare the procedure call with output parameter
            cursor.execute("""
                DECLARE @TestID INT;
                EXEC GetTestID @Testname=?, @TestID=@TestID OUTPUT;
                SELECT @TestID;
            """, test_name)
            
            # Fetch the result
            result = cursor.fetchone()

            if result and result[0] is not None:
                test_ids.append(result[0])
            else:
                print(f"Test ID not found for {test_name}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()

    return test_ids


################ Diagnosis backend ###########################
def get_symptoms():
    # Connect to the database
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()

    # Query to fetch SymptomName from the database
    cursor.execute("SELECT SymptomName FROM TblSymptoms")
    symptoms = cursor.fetchall()

    # Extract symptoms names from query result
    symptoms_names = [symptom[0] for symptom in symptoms]

    # Close the connection
    conn.close()

    return symptoms_names

def search_symptoms(self, search_text):
    """Searches for symptoms based on user input"""
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()

    # Query to search for symptoms based on text input
    cursor.execute("EXEC search_symptoms_by_name @symptoms_name=?", (search_text,))
    symptoms = cursor.fetchall()

    # Extract symptoms names from query result
    symptoms_names = [symptom[0] for symptom in symptoms]

    # Close the connection
    conn.close()

    return symptoms_names

def get_diagnosis():
    # Connect to the database
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()

    # Query to fetch diagnosis names from the database
    cursor.execute("SELECT DiagnosisName FROM TblDiagnoses")
    diagnosis = cursor.fetchall()

    # Extract diagnosis names from query result
    diagnosis_names = [diag[0] for diag in diagnosis]

    # Close the connection
    conn.close()

    return diagnosis_names

def search_diagnosis(self, search_text):
    """Searches for diagnosis based on user input"""
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()

    # Query to search for diagnosis based on text input
    cursor.execute("EXEC search_diagnosis_by_name @diagnosis_name=?", (search_text,))
    diagnosis = cursor.fetchall()

    # Extract diagnosis names from query result
    diagnosis_names = [diag[0] for diag in diagnosis]

    # Close the connection
    conn.close()

    return diagnosis_names
def fetch_diagnosis_ids(selected_diagnoses):
    """Fetch the diagnosis IDs based on the selected diagnosis names"""
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    diagnosis_ids = []

    try:
        for diag_name in selected_diagnoses:
            # Prepare the procedure call with output parameter
            cursor.execute("""
                DECLARE @DiagnosisID INT;
                EXEC GetDiagnosisID @DiagnosisName=?, @DiagnosisID=@DiagnosisID OUTPUT;
                SELECT @DiagnosisID;
            """, diag_name)
            
            # Fetch the result
            result = cursor.fetchone()

            if result and result[0] is not None:
                diagnosis_ids.append(result[0])
            else:
                print(f"Diagnosis ID not found for {diag_name}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()

    return diagnosis_ids

def fetch_symptom_ids(selected_symptoms):
    """Fetch the symptom IDs based on the selected symptom names"""
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    symptom_ids = []

    try:
        for symptom_name in selected_symptoms:
            # Prepare the procedure call with output parameter
            cursor.execute("""
                DECLARE @SymptomID INT;
                EXEC GetSymptomID @SymptomName=?, @SymptomID=@SymptomID OUTPUT;
                SELECT @SymptomID;
            """, symptom_name)
            
            # Fetch the result
            result = cursor.fetchone()

            if result and result[0] is not None:
                symptom_ids.append(result[0])
            else:
                print(f"Symptom ID not found for {symptom_name}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()

    return symptom_ids

def create_prescription(visit_id, medicine_id):
    """Insert a record into TblPrescriptions."""
    query = """INSERT INTO TblPrescriptions (VisitID,  MedicineID) VALUES (?, ?)"""
    values = (visit_id, medicine_id)
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        print(f"Executing query: {query} with values: {values}")  # Debug print
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        print(f"Error while creating prescription: {e}")
    finally:
        cursor.close()
        conn.close()

def create_test_prescription(visit_id, test_id):
    """Insert a record into TblTestPrescriptions."""
    query = """INSERT INTO TblTestPrescriptions (VisitID, TestID) VALUES (?, ?)"""
    values = (visit_id, test_id)
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        print(f"Error while creating test prescription: {e}")
    finally:
        cursor.close()
        conn.close()

def create_symptom_record(visit_id, symptom_id):
    """Insert a record into TblVisitSymptoms."""
    query = """INSERT INTO TblVisitSymptoms (VisitID, SymptomID) VALUES (?, ?)"""
    values = (visit_id, symptom_id)
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        print(f"Error while creating test prescription: {e}")
    finally:
        cursor.close()
        conn.close()

def create_diagnosis_record(visit_id, diagnosis_id):
    """Insert a record into TblTestPrescriptions."""
    query = """INSERT INTO TblVisitDiagnoses (VisitID, DiagnosisID) VALUES (?, ?)"""
    values = (visit_id, diagnosis_id)
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        print(f"Error while creating test prescription: {e}")
    finally:
        cursor.close()
        conn.close()



def get_patient_and_doctor_info(visit_id):
    """
    Fetches the patient's personal information and the doctor's name for a specific visit ID.
    """
    query = """
        SELECT 
            CONCAT(TblDoctors.FirstName, ' ', TblDoctors.LastName) AS DoctorName, -- Doctor's full name
            CONCAT(TblPatients.FirstName, ' ', TblPatients.LastName) AS PatientName,
            DATEDIFF(YEAR, TblPatients.DateOfBirth, GETDATE()) - 
                CASE 
                    WHEN MONTH(GETDATE()) < MONTH(TblPatients.DateOfBirth) OR 
                         (MONTH(GETDATE()) = MONTH(TblPatients.DateOfBirth) AND DAY(GETDATE()) < DAY(TblPatients.DateOfBirth)) 
                    THEN 1 ELSE 0 END AS Age,
            TblPatients.Gender,
            TblPatients.ContactNumber
        FROM 
            TblVisits
        INNER JOIN 
            TblPatients ON TblVisits.PatientID = TblPatients.PatientID
        INNER JOIN 
            TblDoctors ON TblVisits.DoctorID = TblDoctors.DoctorID
        WHERE 
            TblVisits.VisitID = ?;
    """
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, visit_id)
        result = cursor.fetchone()  # Fetch a single row
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Error fetching patient and doctor info for VisitID {visit_id}:", e)
        return None


def get_medicines_by_visit(visit_id):
    """
    Fetches the names of medicines for a specific visit ID.
    """
    query = """
        SELECT 
            TblMedicines.MedicineName,
            TblPrescriptions.Dosage,
            TblPrescriptions.Duration
        FROM 
            TblPrescriptions
        INNER JOIN 
            TblMedicines ON TblPrescriptions.MedicineID = TblMedicines.MedicineID
        WHERE 
            TblPrescriptions.VisitID = ?;
    """
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, visit_id)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Error fetching medicines for VisitID {visit_id}:", e)
        return None


def get_tests_by_visit(visit_id):
    """
    Fetches the names of tests for a specific visit ID.
    """
    query = """
        SELECT 
            TblTests.TestName,
            TblTestPrescriptions.TestInstructions
        FROM 
            TblTestPrescriptions
        INNER JOIN 
            TblTests ON TblTestPrescriptions.TestID = TblTests.TestID
        WHERE 
            TblTestPrescriptions.VisitID = ?;
    """
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, visit_id)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Error fetching tests for VisitID {visit_id}:", e)
        return None


def get_diagnoses_by_visit(visit_id):
    """
    Fetches the diagnoses for a specific visit ID.
    """
    query = """
        SELECT 
            TblDiagnoses.DiagnosisName
        FROM 
            TblVisitDiagnoses
        INNER JOIN 
            TblDiagnoses ON TblVisitDiagnoses.DiagnosisID = TblDiagnoses.DiagnosisID
        WHERE 
            TblVisitDiagnoses.VisitID = ?;
    """
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, visit_id)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Error fetching diagnoses for VisitID {visit_id}:", e)
        return None


def get_symptoms_by_visit(visit_id):
    """
    Fetches the symptoms for a specific visit ID.
    """
    query = """
        SELECT 
            TblSymptoms.SymptomName
        FROM 
            TblVisitSymptoms
        INNER JOIN 
            TblSymptoms ON TblVisitSymptoms.SymptomID = TblSymptoms.SymptomID
        WHERE 
            TblVisitSymptoms.VisitID = ?;
    """
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, visit_id)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Error fetching symptoms for VisitID {visit_id}:", e)
        return None
