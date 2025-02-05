# import sqlite3
# import os

# def init_db():
#     db_path = os.path.join('data', 'database', 'students.db')
#     os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
#     # Remove the existing database file if it exists to avoid corruption issues
#     if os.path.exists(db_path):
#         os.remove(db_path)
    
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
    
#     # Create the students table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS students (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             face_encoding BLOB NOT NULL
#         )
#     ''')
    
#     conn.commit()
#     conn.close()

# if __name__ == "__main__":
#     init_db()

import sqlite3
import os

def init_db():
    db_path = os.path.join('data', 'database', 'students.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Remove the existing database file if it exists to avoid corruption issues
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the students table with the correct schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            face_encoding BLOB NOT NULL,
            class TEXT,
            roll_number TEXT,
            registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()