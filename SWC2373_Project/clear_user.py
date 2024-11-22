import sqlite3

def clear_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")  # Delete all rows from the 'users' table
    conn.commit()
    conn.close()
    print("Cleared all users from the 'users' table.")

if __name__ == "__main__":
    clear_users()
