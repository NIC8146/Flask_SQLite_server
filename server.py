from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)
DB_NAME = "database.db"

# Function to connect to the database
def connect_db():
    try:
        return sqlite3.connect(DB_NAME)
    except sqlite3.Error as e:
        print("Database connection error:", e)
        return None

# Create a table dynamically
@app.route('/create_table', methods=['POST'])
def create_table():
    try:
        data = request.json  
        table_name = data.get("table_name")
        columns = data.get("columns", [])

        if not table_name or not columns:
            return jsonify({"error": "Table name and columns are required"}), 400

        # connect to database
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()

        # Check if table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"error": f"Table '{table_name}' already exists"}), 409

        # create table with given columns entries
        query = f"CREATE TABLE {table_name} ({', '.join(columns)})"
        cursor.execute(query)

        # save changes to database
        conn.commit()
        conn.close()

        return jsonify({"message": f"Table '{table_name}' created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Insert data into any table
@app.route('/insert', methods=['POST'])
def insert_data():
    try:
        data = request.json  
        table_name = data.get("table_name")
        record = data.get("data")

        if not table_name or not record:
            return jsonify({"error": "Table name and record are required"}), 400

        keys = ", ".join(record.keys())
        values = tuple(record.values())
        placeholders = ", ".join(["?" for _ in record])

        query = f"INSERT INTO {table_name} ({keys}) VALUES ({placeholders})"

        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute(query, values)

        # save changes to database
        conn.commit()
        conn.close()

        return jsonify({"message": f"Data inserted into '{table_name}'"}), 201

    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Read all data from a table
@app.route('/read', methods=['POST'])
def read_data():
    try:
        data = request.json  
        table_name = data.get("table_name")
        
        if not table_name:
            return jsonify({"error": "Table name is required"}), 400

        query = f"SELECT * FROM {table_name}"

        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()

        data = [dict(zip(columns, row)) for row in rows]
        return jsonify(data)

    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update data in a table
@app.route('/update', methods=['PUT'])
def update_data():
    try:
        data = request.json  
        table_name = data.get("table_name")
        row_id = data.get("row_id")
        updates = data.get("data")

        if not table_name or not row_id or not updates:
            return jsonify({"error": "Table name, row_id, and updates are required"}), 400

        update_str = ", ".join([f"{key} = ?" for key in updates])
        values = list(updates.values()) + [row_id]

        query = f"UPDATE {table_name} SET {update_str} WHERE id = ?"

        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        conn.close()

        return jsonify({"message": f"Row {row_id} updated in '{table_name}'"}), 200

    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a record from a table
@app.route('/delete', methods=['DELETE'])
def delete_data():
    try:
        data = request.json  
        table_name = data.get("table_name")
        row_id = data.get("row_id")

        if not table_name or not row_id:
            return jsonify({"error": "Table name and row_id are required"}), 400

        query = f"DELETE FROM {table_name} WHERE id = ?"

        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute(query, (row_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": f"Row {row_id} deleted from '{table_name}'"}), 200

    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# List all tables in the database
@app.route('/tables', methods=['GET'])
def list_tables():
    try:
        query = "SELECT name FROM sqlite_master WHERE type='table'"

        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute(query)
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()

        return jsonify({"tables": tables})

    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
