import sqlite3

def execute_query(query):
    """
        Executes a raw SQL query and returns the result.

        :param query: Raw SQL query to execute.
        :return: Results of the query as a list of rows for SELECT statements
    """
    try:
        # Connect to SQLite database
        connection = sqlite3.connect("resources/my_database.db")
        cursor = connection.cursor()

        # Fetch results if the query is a SELECT statement
        if query.strip().upper().startswith("SELECT"):
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            results_dict = [dict(zip(columns, row)) for row in result]
        else:
            return {"error": "Only SELECT queries are allowed"}

        # Close cursor and connection
        cursor.close()
        connection.close()

        return results_dict

    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return None