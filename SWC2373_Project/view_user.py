import sqlite3

def view_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Check if the 'users' table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()

    if table_exists:
        # Fetch and display all rows from the 'users' table
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        if users:
            for user in users:
                print(user)
        else:
            print("No users found.")
    else:
        print("The 'users' table does not exist.")

    conn.close()

if __name__ == "__main__":
    view_users()
