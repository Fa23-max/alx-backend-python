import sqlite3

class ExecuteQuery:
    def _init_(self, db_name, query,par):
        self.db_name = db_name
        self.connection = None
        self.query = query
        self.par = par
    def _enter_(self):
        self.connection = sqlite3.connect(self.db_name)
        c = self.connection.cursor()
        c.execute(self.query,(self.par,))
        print(c.fetchall())
        return self.connection
    def _exit_(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()
        if exc_type is not None:
            print(f"An error occurred: {exc_value}")
        return False
    
with DatabaseConnection('users.db', "SELECT * FROM users WHERE id = ?", 1) as conn:
    print("Connection established and query executed successfully.")

    