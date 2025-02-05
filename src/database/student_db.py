# # import sqlite3
# # from typing import Dict, List, Optional, Tuple
# # import logging
# # from datetime import datetime
# # import os

# # class StudentDatabase:
# #     def __init__(self, db_path: str = "data/database/students.db", log_dir: str = "logs"):
# #         self.db_path = db_path
# #         self.setup_logging(log_dir)
# #         self.initialize_database()

# #     def setup_logging(self, log_dir: str) -> None:
# #         os.makedirs(log_dir, exist_ok=True)
# #         log_file = os.path.join(log_dir, f'student_db_{datetime.now().strftime("%Y%m%d")}.log')
# #         logging.basicConfig(
# #             filename=log_file,
# #             level=logging.INFO,
# #             format='%(asctime)s - %(levelname)s - %(message)s'
# #         )
# #         self.logger = logging.getLogger(__name__)

# #     def initialize_database(self) -> None:
# #         try:
# #             os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
# #             with sqlite3.connect(self.db_path) as conn:
# #                 cursor = conn.cursor()
                
# #                 # Students table
# #                 cursor.execute('''
# #                     CREATE TABLE IF NOT EXISTS students (
# #                         student_id TEXT PRIMARY KEY,
# #                         name TEXT NOT NULL,
# #                         class TEXT NOT NULL,
# #                         roll_number TEXT NOT NULL,
# #                         email TEXT,
# #                         phone TEXT,
# #                         registration_date DATE NOT NULL,
# #                         status TEXT DEFAULT 'active',
# #                         face_encoding_path TEXT,
# #                         last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# #                     )
# #                 ''')
                
# #                 # Face recognition data table
# #                 cursor.execute('''
# #                     CREATE TABLE IF NOT EXISTS face_data (
# #                         student_id TEXT PRIMARY KEY,
# #                         face_encoding BLOB NOT NULL,
# #                         confidence_score FLOAT,
# #                         last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
# #                         FOREIGN KEY (student_id) REFERENCES students(student_id)
# #                     )
# #                 ''')
                
# #                 # Attendance records table
# #                 cursor.execute('''
# #                     CREATE TABLE IF NOT EXISTS attendance (
# #                         id INTEGER PRIMARY KEY AUTOINCREMENT,
# #                         student_id TEXT NOT NULL,
# #                         date DATE NOT NULL,
# #                         time TIME NOT NULL,
# #                         match_confidence FLOAT,
# #                         attendance_type TEXT DEFAULT 'regular',
# #                         verified BOOLEAN DEFAULT FALSE,
# #                         FOREIGN KEY (student_id) REFERENCES students(student_id)
# #                     )
# #                 ''')
                
# #                 conn.commit()
# #                 self.logger.info("Database initialized successfully")
# #         except Exception as e:
# #             self.logger.error(f"Database initialization error: {str(e)}")
# #             raise

# #     def add_student(self, student_data: Dict) -> bool:
# #         try:
# #             required_fields = ['student_id', 'name', 'class', 'roll_number']
# #             if not all(field in student_data for field in required_fields):
# #                 self.logger.error("Missing required student fields")
# #                 return False

# #             with sqlite3.connect(self.db_path) as conn:
# #                 cursor = conn.cursor()
                
# #                 cursor.execute('''
# #                     INSERT INTO students (
# #                         student_id, name, class, roll_number, email, phone,
# #                         registration_date, status, face_encoding_path
# #                     ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
# #                 ''', (
# #                     student_data['student_id'],
# #                     student_data['name'],
# #                     student_data['class'],
# #                     student_data['roll_number'],
# #                     student_data.get('email'),
# #                     student_data.get('phone'),
# #                     datetime.now().date(),
# #                     'active',
# #                     student_data.get('face_encoding_path')
# #                 ))
                
# #                 if 'face_encoding' in student_data:
# #                     cursor.execute('''
# #                         INSERT INTO face_data (student_id, face_encoding, confidence_score)
# #                         VALUES (?, ?, ?)
# #                     ''', (
# #                         student_data['student_id'],
# #                         student_data['face_encoding'],
# #                         student_data.get('confidence_score', 0.0)
# #                     ))
                
# #                 conn.commit()
# #                 self.logger.info(f"Added student: {student_data['student_id']}")
# #                 return True
                
# #         except sqlite3.IntegrityError:
# #             self.logger.error(f"Student ID already exists: {student_data['student_id']}")
# #             return False
# #         except Exception as e:
# #             self.logger.error(f"Error adding student: {str(e)}")
# #             return False

# #     def update_student(self, student_id: str, update_data: Dict) -> bool:
# #         try:
# #             with sqlite3.connect(self.db_path) as conn:
# #                 cursor = conn.cursor()
                
# #                 # Update student information
# #                 if any(k for k in update_data.keys() if k != 'face_encoding'):
# #                     fields = []
# #                     values = []
# #                     for key, value in update_data.items():
# #                         if key != 'face_encoding':
# #                             fields.append(f"{key} = ?")
# #                             values.append(value)
                    
# #                     values.append(student_id)
# #                     query = f'''
# #                         UPDATE students 
# #                         SET {", ".join(fields)}, last_updated = CURRENT_TIMESTAMP
# #                         WHERE student_id = ?
# #                     '''
# #                     cursor.execute(query, values)
                
# #                 # Update face data if provided
# #                 if 'face_encoding' in update_data:
# #                     cursor.execute('''
# #                         INSERT OR REPLACE INTO face_data 
# #                         (student_id, face_encoding, confidence_score, last_updated)
# #                         VALUES (?, ?, ?, CURRENT_TIMESTAMP)
# #                     ''', (
# #                         student_id,
# #                         update_data['face_encoding'],
# #                         update_data.get('confidence_score', 0.0)
# #                     ))
                
# #                 conn.commit()
# #                 self.logger.info(f"Updated student: {student_id}")
# #                 return True
                
# #         except Exception as e:
# #             self.logger.error(f"Error updating student: {str(e)}")
# #             return False

# #     def get_student(self, student_id: str) -> Optional[Dict]:
# #         try:
# #             with sqlite3.connect(self.db_path) as conn:
# #                 conn.row_factory = sqlite3.Row
# #                 cursor = conn.cursor()
                
# #                 cursor.execute('''
# #                     SELECT s.*, f.face_encoding, f.confidence_score
# #                     FROM students s
# #                     LEFT JOIN face_data f ON s.student_id = f.student_id
# #                     WHERE s.student_id = ?
# #                 ''', (student_id,))
                
# #                 result = cursor.fetchone()
# #                 if result:
# #                     return dict(result)
# #                 return None
                
# #         except Exception as e:
# #             self.logger.error(f"Error retrieving student: {str(e)}")
# #             return None

# #     def get_all_students(self, active_only: bool = True) -> List[Dict]:
# #         try:
# #             with sqlite3.connect(self.db_path) as conn:
# #                 conn.row_factory = sqlite3.Row
# #                 cursor = conn.cursor()
                
# #                 query = '''
# #                     SELECT s.*, f.confidence_score
# #                     FROM students s
# #                     LEFT JOIN face_data f ON s.student_id = f.student_id
# #                 '''
# #                 if active_only:
# #                     query += " WHERE s.status = 'active'"
                
# #                 cursor.execute(query)
# #                 return [dict(row) for row in cursor.fetchall()]
                
# #         except Exception as e:
# #             self.logger.error(f"Error retrieving students: {str(e)}")
# #             return []

# #     def deactivate_student(self, student_id: str) -> bool:
# #         try:
# #             with sqlite3.connect(self.db_path) as conn:
# #                 cursor = conn.cursor()
# #                 cursor.execute('''
# #                     UPDATE students 
# #                     SET status = 'inactive', last_updated = CURRENT_TIMESTAMP
# #                     WHERE student_id = ?
# #                 ''', (student_id,))
                
# #                 conn.commit()
# #                 self.logger.info(f"Deactivated student: {student_id}")
# #                 return True
                
# #         except Exception as e:
# #             self.logger.error(f"Error deactivating student: {str(e)}")
# #             return False

# #     def record_attendance(self, attendance_data: Dict) -> bool:
# #         try:
# #             required_fields = ['student_id', 'date', 'time']
# #             if not all(field in attendance_data for field in required_fields):
# #                 self.logger.error("Missing required attendance fields")
# #                 return False

# #             with sqlite3.connect(self.db_path) as conn:
# #                 cursor = conn.cursor()
                
# #                 # Check if attendance already recorded
# #                 cursor.execute('''
# #                     SELECT COUNT(*) FROM attendance 
# #                     WHERE student_id = ? AND date = ? AND attendance_type = ?
# #                 ''', (
# #                     attendance_data['student_id'],
# #                     attendance_data['date'],
# #                     attendance_data.get('attendance_type', 'regular')
# #                 ))
                
# #                 if cursor.fetchone()[0] > 0:
# #                     self.logger.info(f"Attendance already recorded for student {attendance_data['student_id']}")
# #                     return False
                
# #                 cursor.execute('''
# #                     INSERT INTO attendance (
# #                         student_id, date, time, match_confidence,
# #                         attendance_type, verified
# #                     ) VALUES (?, ?, ?, ?, ?, ?)
# #                 ''', (
# #                     attendance_data['student_id'],
# #                     attendance_data['date'],
# #                     attendance_data['time'],
# #                     attendance_data.get('match_confidence', 0.0),
# #                     attendance_data.get('attendance_type', 'regular'),
# #                     attendance_data.get('verified', False)
# #                 ))
                
# #                 conn.commit()
# #                 self.logger.info(f"Recorded attendance for student: {attendance_data['student_id']}")
# #                 return True
                
# #         except Exception as e:
# #             self.logger.error(f"Error recording attendance: {str(e)}")
# #             return False

# #     def get_attendance_report(self, 
# #                             start_date: datetime,
# #                             end_date: datetime,
# #                             class_name: Optional[str] = None) -> List[Dict]:
# #         try:
# #             with sqlite3.connect(self.db_path) as conn:
# #                 conn.row_factory = sqlite3.Row
# #                 cursor = conn.cursor()
                
# #                 query = '''
# #                     SELECT 
# #                         a.*,
# #                         s.name,
# #                         s.class,
# #                         s.roll_number
# #                     FROM attendance a
# #                     JOIN students s ON a.student_id = s.student_id
# #                     WHERE a.date BETWEEN ? AND ?
# #                 '''
# #                 params = [start_date.date(), end_date.date()]
                
# #                 if class_name:
# #                     query += " AND s.class = ?"
# #                     params.append(class_name)
                
# #                 cursor.execute(query, params)
# #                 return [dict(row) for row in cursor.fetchall()]
                
# #         except Exception as e:
# #             self.logger.error(f"Error generating attendance report: {str(e)}")
# #             return []

# #     def get_student_attendance(self, 
# #                              student_id: str,
# #                              start_date: Optional[datetime] = None,
# #                              end_date: Optional[datetime] = None) -> List[Dict]:
# #         try:
# #             with sqlite3.connect(self.db_path) as conn:
# #                 conn.row_factory = sqlite3.Row
# #                 cursor = conn.cursor()
                
# #                 query = '''
# #                     SELECT * FROM attendance
# #                     WHERE student_id = ?
# #                 '''
# #                 params = [student_id]
                
# #                 if start_date:
# #                     query += " AND date >= ?"
# #                     params.append(start_date.date())
# #                 if end_date:
# #                     query += " AND date <= ?"
# #                     params.append(end_date.date())
                
# #                 cursor.execute(query, params)
# #                 return [dict(row) for row in cursor.fetchall()]
                
# #         except Exception as e:
# #             self.logger.error(f"Error retrieving student attendance: {str(e)}")
# #             return []

# #     def verify_attendance(self, attendance_id: int) -> bool:
# #         try:
# #             with sqlite3.connect(self.db_path) as conn:
# #                 cursor = conn.cursor()
# #                 cursor.execute('''
# #                     UPDATE attendance 
# #                     SET verified = TRUE
# #                     WHERE id = ?
# #                 ''', (attendance_id,))
                
# #                 conn.commit()
# #                 return True
                
# #         except Exception as e:
# #             self.logger.error(f"Error verifying attendance: {str(e)}")
# #             return False

# #     def get_class_list(self) -> List[str]:
# #         try:
# #             with sqlite3.connect(self.db_path) as conn:
# #                 cursor = conn.cursor()
# #                 cursor.execute('SELECT DISTINCT class FROM students WHERE status = "active"')
# #                 return [row[0] for row in cursor.fetchall()]
                
# #         except Exception as e:
# #             self.logger.error(f"Error retrieving class list: {str(e)}")
# #             return []

# import sqlite3
# import os
# from typing import List, Dict

# class StudentDatabase:
#     def __init__(self, db_path='data/database/students.db'):
#         self.db_path = db_path
#         self.connection = sqlite3.connect(self.db_path)
#         self.connection.row_factory = sqlite3.Row  # To enable dictionary-like cursor
#         self.initialize_database()

#     def initialize_database(self):
#         cursor = self.connection.cursor()
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS students (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT NOT NULL,
#                 face_encoding BLOB NOT NULL
#             )
#         ''')
#         self.connection.commit()

#     def add_student(self, name: str, face_encoding: bytes):
#         try:
#             with sqlite3.connect(self.db_path) as conn:
#                 cursor = conn.cursor()
#                 cursor.execute('''
#                     INSERT INTO students (name, face_encoding)
#                     VALUES (?, ?)
#                 ''', (name, face_encoding))
#                 conn.commit()
#         except Exception as e:
#             print(f"Error adding student: {str(e)}")

#     def get_student(self, student_id: int) -> Dict:
#         try:
#             with sqlite3.connect(self.db_path) as conn:
#                 cursor = conn.cursor()
#                 cursor.execute('''
#                     SELECT * FROM students WHERE id = ?
#                 ''', (student_id,))
                
#                 result = cursor.fetchone()
#                 if result:
#                     return dict(result)
#                 return None
                
#         except Exception as e:
#             print(f"Error retrieving student: {str(e)}")
#             return None

#     def get_all_students(self, active_only: bool = True) -> List[Dict]:
#         try:
#             with sqlite3.connect(self.db_path) as conn:
#                 cursor = conn.cursor()
#                 cursor.execute('''
#                     SELECT * FROM students
#                 ''')
                
#                 results = cursor.fetchall()
#                 return [dict(row) for row in results]
                
#         except Exception as e:
#             print(f"Error retrieving all students: {str(e)}")
#             return []

#     def __del__(self):
#         self.connection.close()

import sqlite3
import os
from typing import List, Dict, Optional

class StudentDatabase:
    def __init__(self, db_path='data/database/students.db'):
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.initialize_database()

    def initialize_database(self):
        """Create tables if they don't exist."""
        cursor = self.connection.cursor()
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
        self.connection.commit()

    def add_student(self, 
                    name: str, 
                    face_encoding: bytes, 
                    class_name: Optional[str] = None, 
                    roll_number: Optional[str] = None):
        """
        Add a new student to the database.
        
        Args:
            name: Student's full name
            face_encoding: Encoded face data
            class_name: Optional class name
            roll_number: Optional roll number
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO students (name, face_encoding, class, roll_number)
                VALUES (?, ?, ?, ?)
            ''', (name, face_encoding, class_name, roll_number))
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Student {name} already exists.")
            return None
        except Exception as e:
            print(f"Error adding student: {str(e)}")
            return None

    def get_student(self, student_id: int) -> Optional[Dict]:
        """
        Retrieve a student by their ID.
        
        Args:
            student_id: Unique identifier of the student
        
        Returns:
            Dictionary of student details or None
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
        except Exception as e:
            print(f"Error retrieving student: {str(e)}")
            return None

    def get_all_students(self, active_only: bool = True) -> List[Dict]:
        """
        Retrieve all students from the database.
        
        Args:
            active_only: Flag to filter active students (not implemented in this version)
        
        Returns:
            List of student dictionaries
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM students')
            results = cursor.fetchall()
            return [dict(row) for row in results]
        except Exception as e:
            print(f"Error retrieving all students: {str(e)}")
            return []

    def update_student(self, 
                       student_id: int, 
                       name: Optional[str] = None,
                       class_name: Optional[str] = None,
                       roll_number: Optional[str] = None,
                       face_encoding: Optional[bytes] = None):
        """
        Update student information.
        
        Args:
            student_id: Unique identifier of the student
            name: Updated name
            class_name: Updated class name
            roll_number: Updated roll number
            face_encoding: Updated face encoding
        """
        try:
            # Prepare update fields
            update_fields = []
            params = []
            
            if name:
                update_fields.append('name = ?')
                params.append(name)
            if class_name:
                update_fields.append('class = ?')
                params.append(class_name)
            if roll_number:
                update_fields.append('roll_number = ?')
                params.append(roll_number)
            if face_encoding:
                update_fields.append('face_encoding = ?')
                params.append(face_encoding)
            
            if not update_fields:
                return False
            
            # Add student ID to params
            params.append(student_id)
            
            # Construct and execute query
            query = f'UPDATE students SET {", ".join(update_fields)} WHERE id = ?'
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating student: {str(e)}")
            return False

    def delete_student(self, student_id: int) -> bool:
        """
        Delete a student from the database.
        
        Args:
            student_id: Unique identifier of the student
        
        Returns:
            Success status of deletion
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting student: {str(e)}")
            return False

    def get_class_list(self) -> List[str]:
        """
        Retrieve unique class names.
        
        Returns:
            List of unique class names
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT DISTINCT class FROM students WHERE class IS NOT NULL')
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error retrieving class list: {str(e)}")
            return []

    def __del__(self):
        """Close database connection when object is deleted."""
        if hasattr(self, 'connection'):
            self.connection.close()