import secrets
import MySQLdb

db = MySQLdb.connect("localhost", secrets.sql_username, secrets.sql_password, "datalogger")
cursor = db.cursor()

# Attempt to create tables in DB
statements = []
temp = ""
for line in open("./schema.sql"):
    l = line.strip()
    temp += l
    if l.endswith(";"):
        statements.append(temp)
        temp = ""

for statement in statements:
    print(statement)
    try:
        cursor.execute(statement)
    except Exception as e:
        print(e)
