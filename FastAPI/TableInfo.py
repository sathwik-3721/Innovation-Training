import mysql.connector

config = { 
    'host' : "localhost",
    'user' : "root",
    'password' : "root", 
    'database' : "pydb"
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("DESCRIBE Employee")
    td = cursor.fetchall()
    for col in td:
        print(col)

except Exception as e:
    print(e)