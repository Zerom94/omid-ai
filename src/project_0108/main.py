import mysql.connector
from mysql.connector import Error

def query_database():
    config = {
        'host': 'localhost',
        'user': 'your_user',
        'password': 'your_password',
        'database': 'your_database',
    }
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM sample_table LIMIT 10")
        rows = (row for row in cursor)  # lazy generator
        results = [f"id={r[0]}, name={r[1]}" for r in rows]
        return results
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        if conn.is_connected():
            conn.close()

if __name__ == "__main__":
    for line in query_database():
        print(line)
