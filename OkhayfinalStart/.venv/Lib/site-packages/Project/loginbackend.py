from DatabaseConnection import DatabaseConnection  # type: ignore
import hashlib

# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def fetch_login(username, password):
    try:
        # Establish connection to the database
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # Query to check if the provided username and hashed password match
        query = """
            SELECT RoleID 
            FROM TblCredentials 
            WHERE Username = ? AND PasswordHash = ?
        """

        # Execute the query with the provided username and hashed password
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        # Check if a matching record was found
        if result:
            return result[0]  # RoleID should be the first column in the result
        else:
            return None  # Return None if no match is found

    except Exception as e:
        print("Error fetching data:", e)
        return None
    finally:
        # Ensure the database connection is closed
        if 'connection' in locals() and connection:
            connection.close()

# Example usage

id = fetch_login('misbah', '123')
print(id)
