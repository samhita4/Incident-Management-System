import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",          # XAMPP → empty password
    database="incident_db"
)

cursor = db.cursor(dictionary=True)
