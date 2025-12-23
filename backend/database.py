import sqlite3

def execute_query(query):
    """
    Executes a raw SQL query and returns the result (if applicable).

    :param query: Raw SQL query to execute.
    :return: Results of the query as a list of rows for SELECT statements, None for others.
    """
    try:
        # Connect to SQLite database
        connection = sqlite3.connect("../my_database.db")
        cursor = connection.cursor()

        # Execute the query
        cursor.execute(query)

        # Fetch results if the query is a SELECT statement
        if query.strip().upper().startswith("SELECT"):
            result = cursor.fetchall()
        else:
            # Commit changes for other queries (INSERT, UPDATE, DELETE)
            connection.commit()
            result = None

        # Close cursor and connection
        cursor.close()
        connection.close()

        return result

    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return None