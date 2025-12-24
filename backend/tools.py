import json

from typing import List, Dict, Any
from database.database import execute_query
from database.schema import get_schema_context

# Define the SQL query tool for function calling
SQL_QUERY_TOOL = {
    "type": "function",
    "function": {
        "name": "execute_sql_query",
        "description": (
            "Execute a SQL query on the database to retrieve information. "
            "Use this function when you need to get data from the database to answer user questions. "
            "Only use SELECT queries are allowed. INSERT, UPDATE, DELETE or ALTER are not allowed. "
            f"\n\n{get_schema_context()}"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "The SQL SELECT query to execute. Must be a valid SQL query. "
                        "Always use LIMIT clause to prevent returning too many rows (max 100). "
                        "Example: SELECT * FROM users WHERE is_active = true LIMIT 10"
                    )
                },
                "explanation": {
                    "type": "string",
                    "description": "Brief explanation of what this query does and why it's needed"
                }
            },
            "required": ["query", "explanation"]
        }
    }
}

def execute_sql_query(query: str, explanation: str) -> Dict[str, Any]:
    """
    Execute a SQL query and return results.

    Args:
        query: SQL query string
        explanation: Explanation of what the query does

    Returns:
        Dictionary containing query results or error information
    """
    # Security check: only allow SELECT queries
    query_upper = query.strip().upper()
    if not query_upper.startswith("SELECT"):
        return {
            "error": "Only SELECT queries are allowed",
            "query": query
        }

    # Check for dangerous keywords
    dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER", "CREATE", "INSERT", "UPDATE"]
    for keyword in dangerous_keywords:
        if keyword in query_upper:
            return {
                "error": f"Query contains forbidden keyword: {keyword}",
                "query": query
            }

    try:
        results = execute_query(query)
        return {
            "success": True,
            "explanation": explanation,
            "query": query,
            "results": results,
            "row_count": len(results)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "query": query
        }


def get_tools() -> List[Dict]:
    """Return list of available tools for function calling."""
    return [SQL_QUERY_TOOL]


def execute_function_call(function_name: str, arguments: Dict[str, Any]) -> str:
    """
    Execute a function call based on the function name and arguments.

    Args:
        function_name: Name of the function to call
        arguments: Dictionary of arguments for the function

    Returns:
        JSON string with function results
    """
    if function_name == "execute_sql_query":
        result = execute_sql_query(
            query=arguments.get("query", ""),
            explanation=arguments.get("explanation", "")
        )
        return json.dumps(result, indent=2, default=str)
    else:
        return json.dumps({"error": f"Unknown function: {function_name}"})