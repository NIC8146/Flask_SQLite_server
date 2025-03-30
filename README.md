Flask_SQLite_server is a python based database server which provide web interface to perform CRUD operation database.

## Requirments

To install required pakages
```bash
pip install flask
```
# Setup
Clone the project

```bash
git clone https://github.com/NIC8146/Flask_SQLite_server.git
```

Go to the project directory

```bash
cd Flask_SQLite_server
```


# Run server
```bash
python3 server.py
```

# API Docs
## **1. Create a Table**  
### **Endpoint**
```
POST /create_table
```
### **Description**
Creates a new table in the database with the specified columns.

### **Request Body (JSON)**
```json
{
  "table_name": "users",
  "columns": ["id INTEGER PRIMARY KEY", "name TEXT", "age INTEGER"]
}
```
### **Success Response (201)**
```json
{
  "message": "Table 'users' created successfully"
}
```
### **JavaScript Example**
```javascript
const response = await fetch("http://127.0.0.1:5000/create_table", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
        table_name: "users",
        columns: ["id INTEGER PRIMARY KEY", "name TEXT", "age INTEGER"]
    })
});

console.log(await response.json());
```
---

## **2. Insert Data into a Table**  
### **Endpoint**
```
POST /insert
```
### **Description**
Inserts a new row into the specified table.

### **Request Body (JSON)**
```json
{
  "table_name": "users",
  "data": { "name": "Alice", "age": 25 }
}
```
### **Success Response (201)**
```json
{
  "message": "Data inserted into 'users'"
}
```
### **JavaScript Example**
```javascript
const response = await fetch("http://127.0.0.1:5000/insert", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ table_name: "users", data: { name: "Alice", age: 25 } })
});

console.log(await response.json());

```
---

## **3. Read Data from a Table**  
### **Endpoint**
```
POST /read
```
### **Description**
Fetches all rows from the specified table.

### **Request Body (JSON)**
```json
{
  "table_name": "users"
}
```
### **Success Response (200)**
```json
[
  { "id": 1, "name": "Alice", "age": 25 },
  { "id": 2, "name": "Bob", "age": 30 }
]
```
### **JavaScript Example**
```javascript
const response = await fetch("http://127.0.0.1:5000/read", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ table_name: "users" })
});

console.log(await response.json());

```
---

## **4. Update a Record in a Table**  
### **Endpoint**
```
PUT /update
```
### **Description**
Updates a record in the table based on the given `row_id`.

### **Request Body (JSON)**
```json
{
  "table_name": "users",
  "row_id": 1,
  "data": { "name": "Bob", "age": 30 }
}
```
### **Success Response (200)**
```json
{
  "message": "Row 1 updated in 'users'"
}
```
### **JavaScript Example**
```javascript
const response = await fetch("http://127.0.0.1:5000/update", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ table_name: "users", row_id: 1, data: { name: "Bob", age: 30 } })
});

console.log(await response.json());

```
---

## **5. Delete a Record from a Table**  
### **Endpoint**
```
DELETE /delete
```
### **Description**
Deletes a record from the table based on `row_id`.

### **Request Body (JSON)**
```json
{
  "table_name": "users",
  "row_id": 1
}
```
### **Success Response (200)**
```json
{
  "message": "Row 1 deleted from 'users'"
}
```
### **JavaScript Example**
```javascript
const response = await fetch("http://127.0.0.1:5000/delete", {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ table_name: "users", row_id: 1 })
});

console.log(await response.json());

```
---

## **6. List All Tables**  
### **Endpoint**
```
GET /tables
```
### **Description**
Fetches a list of all tables in the database.

### **Success Response (200)**
```json
{
  "tables": ["users", "orders"]
}
```
### **JavaScript Example**
```javascript
const response = await fetch("http://127.0.0.1:5000/tables");

console.log(await response.json());
```
---

## **Error Handling**
If an error occurs, the API returns a JSON error message:

```
{
  "error": "Table not found"
}
```
or  

```
{
  "error": "Database connection failed"
}
```
---

## Data types

| **Storage Class** | **Value Stores** |
|-------------------|------------------|
| `NULL` | NULL |
| `INTEGER` | Signed Integer (1, 2, 3, 4, 5, or 8 bytes depending on magnitude) |
| `REAL` | Floating point value |
| `TEXT` | TEXT string |
| `BLOB (Binary Large Object)` | Data stored exactly the way it was input, generally in binary format |

## Summary
| **Method** | **Endpoint**       | **Description**           |
|-----------|------------------|-----------------------|
| `POST`   | `/create_table`   | Create a new table   |
| `POST`   | `/insert`         | Insert data          |
| `POST`   | `/read`           | Fetch all data       |
| `PUT`    | `/update`         | Update a record      |
| `DELETE` | `/delete`         | Delete a record      |
| `GET`    | `/tables`         | List all tables      |

---
