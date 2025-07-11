import sqlite3
class DatabaseConnection:
    def _init_(self, db_name):
        self.db_name = db_name
        self.connection = None
    def _enter_(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection
    def _exit_(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()
        if exc_type is not None:
            print(f"An error occurred: {exc_value}")
        return False

with DatabaseConnection('users.db') as conn:
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    print(c.fetchall())

# ["__init__", "__enter__", "__exit__"]