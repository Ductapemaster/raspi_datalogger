import secrets
import MySQLdb

db = MySQLdb.connect("localhost", secrets.sql_username, secrets.sql_password, "datalogger")
cursor = db.cursor()

# Get some data
try:
    cursor.execute("SELECT * FROM measurement_type")
    for m_type in cursor.fetchall():
        print(m_type)

except Exception as e:
    print(e)
