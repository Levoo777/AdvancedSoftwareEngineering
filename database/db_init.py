import sqlite3
connection = sqlite3.connect("database/kundendatenbank.sql")
cursor = connection.cursor()

try:
    cursor.execute("""DROP TABLE users;""")
except:
    pass

sql_command = """
CREATE TABLE users ( 
customer_number INTEGER PRIMARY KEY,
email VARCHAR(30),
username VARCHAR(20), 
joining DATE,
password VARCHAR(64),
salt VARCHAR(64),
lobby INTEGER DEFAULT 0);"""
cursor.execute(sql_command)


sql_command = """INSERT INTO users (customer_number, email, username, joining, password, salt)
    VALUES (NULL, "Frank@S", "Frank", "1961-10-25", "abcdef12345", "abc");"""
cursor.execute(sql_command)

connection.commit()
connection.close()