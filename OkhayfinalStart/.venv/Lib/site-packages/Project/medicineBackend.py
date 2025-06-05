from DatabaseConnection import DatabaseConnection  # type: ignore

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

