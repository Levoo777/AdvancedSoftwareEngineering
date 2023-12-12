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
mfa VARCHAR(64) NULL,
lobby INTEGER DEFAULT 0,
highscore INTEGER DEFAULT 0);"""
cursor.execute(sql_command)


sql_command = """INSERT INTO users (customer_number, email, username, joining, password, salt)
    VALUES (NULL, 'test@test', 'test', '2023-12-12', '7e82cc4635defca639dd9512e3278c6d10dfecc1acc8fc136b5050d4696324ae', '8f24470d9010b856c06d3b972726c150defd033b3991ca41a2143c2a0f1ad5cb');"""
cursor.execute(sql_command)

connection.commit()
connection.close()