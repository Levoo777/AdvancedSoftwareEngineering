import sqlite3
import secrets

class DB_Manager:
    db_name: str
    table_name: str
    connection = None
    cursor = None

    def __init__(self, db_name, table_name):
        self.db_name = "/app/database/kundendatenbank.sql" # For python use db_name instead of the "/app/database/kundendatenbank.sql"
        self.table_name = table_name
    
    def change_table(self, table_name):
        self.table_name = table_name
    
    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()

    def insert_user(self, args, random_hex = None):
        customer_number, email, username, joining, password = args
        print(customer_number, email, username, joining, password)
        if not random_hex:
            random_hex = secrets.token_hex(32)
        sql_command = f'INSERT INTO {self.table_name} (customer_number, email, username, joining, password, salt) VALUES ({customer_number}, \"{email}\", \"{username}\", \"{joining}\", \"{password}\", \"{random_hex}\");'
        self.cursor.execute(sql_command)
        self.connection.commit()
    
    def update_user(self, args):
        customer_number, colname, new_val = args
        sql_command = f"UPDATE {self.table_name} SET {colname} = \"{new_val}\" WHERE customer_number = {customer_number}"
        self.cursor.execute(sql_command)
        self.connection.commit()

    def clear_lobby(self, lobby_id, user_id):
        sql_command = f"UPDATE {self.table_name} SET lobby = 0 WHERE lobby = {lobby_id} AND customer_number != {user_id}"
        self.cursor.execute(sql_command)
        self.connection.commit()

    def get_user(self, customer_number):
        sql_command = f"SELECT * FROM {self.table_name} where customer_number = {customer_number}"
        self.cursor.execute(sql_command)
        return self.cursor.fetchone()
    
    def get_highscore(self, customer_number):
        sql_command = f"SELECT highscore FROM {self.table_name} where customer_number = {customer_number}"
        self.cursor.execute(sql_command)
        return self.cursor.fetchone()
    
    def get_login_data_by_mail(self, mail):
        sql_command = f"SELECT password, salt, customer_number FROM {self.table_name} where email = \"{mail}\""
        self.cursor.execute(sql_command)
        return self.cursor.fetchone()

    def get_mfa_by_id(self, id):
        sql_command = f"SELECT mfa FROM {self.table_name} where customer_number = {id}"
        self.cursor.execute(sql_command)
        return self.cursor.fetchone()

    def remove_mfa(self, customer_number):
        sql_command = f"UPDATE {self.table_name} SET mfa = NULL WHERE customer_number = {customer_number}"
        self.cursor.execute(sql_command)
        self.connection.commit()

    def get_mail_and_name_by_id(self, id):
        sql_command = f"SELECT email, username FROM {self.table_name} where customer_number = {id}"
        self.cursor.execute(sql_command)
        return self.cursor.fetchone()

    def get_id_by_mail(self, mail):
        sql_command = f"SELECT customer_number FROM {self.table_name} where email = \"{mail}\""
        self.cursor.execute(sql_command)
        return self.cursor.fetchone()
    
    def get_lobby(self, id):
        sql_command = f"SELECT lobby FROM {self.table_name} where customer_number = {id}"
        self.cursor.execute(sql_command)
        return self.cursor.fetchone()
    
    def get_users_in_lobby(self, id):
        sql_command = f"SELECT email FROM {self.table_name} where lobby = {id}"
        self.cursor.execute(sql_command)
        return self.cursor.fetchall()

    def show_all_users(self):
        sql_command = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(sql_command)
        print(self.cursor.fetchall())
    
    def delete_user(self, customer_number):
        sql_command = f"DELETE FROM {self.table_name} where customer_number = {customer_number}"
        self.cursor.execute(sql_command)
        self.connection.commit()
    
if __name__ == "__main__":
    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    #DB.insert_user(("NULL", "Sercan@B", "Sercan", "Berg", "2000-08-17", "1234567abc"))
    #DB.show_all_users()
    #DB.update_user((2, "lname", "Testo"))
    #DB.show_all_users()
    #DB.update_user((3, "role", "Testo"))
    #DB.get_login_data_by_mail("William@S")
    #DB.delete_user(2)
    lb =DB.get_lobby(1)
    print(lb)
    DB.show_all_users()
