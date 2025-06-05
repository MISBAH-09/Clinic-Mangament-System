
# Backend functions
from DatabaseConnection import DatabaseConnection  # type: ignore

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