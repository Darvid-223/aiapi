import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def connect_to_database():
    """Connect to the PostgreSQL database."""
    try:
        connection = psycopg2.connect(
            dbname=os.environ.get("POSTGRESQL_DB"),
            user=os.environ.get("POSTGRESQL_USER"),
            password=os.environ.get("POSTGRESQL_PASSWORD"),
            host=os.environ.get("POSTGRESQL_HOST"),
            port=os.environ.get("POSTGRESQL_PORT", "5432")
        )
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def query_database(query, params=None):
    """Execute a SQL query and return results."""
    connection = connect_to_database()
    if connection is None:
        return "Could not connect to the database."

    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        return results
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    # Test database query
    test_query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
    result = query_database(test_query)
    if isinstance(result, list):  # If result is a list
        print("Query successful! Tables in the database:")
        for row in result:
            print(row[0])  # Print table name
    else:
        print(f"Query failed: {result}")

