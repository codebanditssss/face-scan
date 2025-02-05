import sqlite3
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, date, time
import os
import pandas as pd

class AttendanceDatabase:
    def __init__(self, db_path: str = "data/database/students.db", log_dir: str = "logs"):
        self.db_path = db_path
        self.setup_logging(log_dir)
        self.initialize_database()

    def setup_logging(self, log_dir: str) -> None:
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f'attendance_db_{datetime.now().strftime("%Y%m%d")}.log')
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def initialize_database(self) -> None:
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Daily attendance records
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS daily_attendance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id TEXT NOT NULL,
                        date DATE NOT NULL,
                        entry_time TIME,
                        exit_time TIME,
                        match_confidence FLOAT,
                        status TEXT CHECK(status IN ('present', 'absent', 'late', 'half-day')),
                        verification_status TEXT DEFAULT 'pending',
                        remarks TEXT,
                        FOREIGN KEY (student_id) REFERENCES students(student_id)
                    )
                ''')
                
                # Attendance settings
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS attendance_settings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        class TEXT NOT NULL,
                        start_time TIME NOT NULL,
                        late_threshold TIME NOT NULL,
                        half_day_threshold TIME NOT NULL,
                        minimum_hours FLOAT NOT NULL,
                        active BOOLEAN DEFAULT TRUE
                    )
                ''')
                
                # Holidays and events
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS holidays (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date DATE NOT NULL,
                        description TEXT,
                        holiday_type TEXT CHECK(holiday_type IN ('public', 'school', 'exam', 'event')),
                        applies_to TEXT
                    )
                ''')
                
                conn.commit()
                self.logger.info("Attendance database initialized successfully")
        except Exception as e:
            self.logger.error(f"Database initialization error: {str(e)}")
            raise

    def mark_attendance(self, attendance_data: Dict) -> bool:
        try:
            required_fields = ['student_id', 'date', 'entry_time', 'match_confidence']
            if not all(field in attendance_data for field in required_fields):
                self.logger.error("Missing required attendance fields")
                return False

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get attendance settings
                cursor.execute('''
                    SELECT start_time, late_threshold, half_day_threshold
                    FROM attendance_settings
                    WHERE class = (
                        SELECT class FROM students WHERE student_id = ?
                    ) AND active = TRUE
                ''', (attendance_data['student_id'],))
                
                settings = cursor.fetchone()
                if not settings:
                    self.logger.error("No attendance settings found")
                    return False
                
                start_time, late_threshold, half_day_threshold = settings
                entry_time = datetime.strptime(attendance_data['entry_time'], '%H:%M:%S').time()
                
                # Determine attendance status
                if entry_time <= datetime.strptime(start_time, '%H:%M:%S').time():
                    status = 'present'
                elif entry_time <= datetime.strptime(late_threshold, '%H:%M:%S').time():
                    status = 'late'
                elif entry_time <= datetime.strptime(half_day_threshold, '%H:%M:%S').time():
                    status = 'half-day'
                else:
                    status = 'absent'
                
                # Insert attendance record
                cursor.execute('''
                    INSERT INTO daily_attendance (
                        student_id, date, entry_time, match_confidence, 
                        status, verification_status
                    ) VALUES (?, ?, ?, ?, ?, 'pending')
                ''', (
                    attendance_data['student_id'],
                    attendance_data['date'],
                    attendance_data['entry_time'],
                    attendance_data['match_confidence'],
                    status
                ))
                
                conn.commit()
                self.logger.info(f"Marked attendance for student: {attendance_data['student_id']}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error marking attendance: {str(e)}")
            return False

    def update_exit_time(self, student_id: str, exit_time: time) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                today = date.today()
                
                cursor.execute('''
                    UPDATE daily_attendance 
                    SET exit_time = ?
                    WHERE student_id = ? AND date = ?
                ''', (exit_time, student_id, today))
                
                conn.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Error updating exit time: {str(e)}")
            return False

    def verify_attendance(self, attendance_id: int, status: str, remarks: Optional[str] = None) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE daily_attendance 
                    SET verification_status = ?, remarks = ?
                    WHERE id = ?
                ''', (status, remarks, attendance_id))
                
                conn.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Error verifying attendance: {str(e)}")
            return False

    def get_daily_attendance(self, class_name: str, date: date) -> List[Dict]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT 
                        da.*,
                        s.name,
                        s.roll_number,
                        s.class
                    FROM daily_attendance da
                    JOIN students s ON da.student_id = s.student_id
                    WHERE s.class = ? AND da.date = ?
                    ORDER BY s.roll_number
                ''', (class_name, date))
                
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            self.logger.error(f"Error retrieving daily attendance: {str(e)}")
            return []

    def get_student_attendance(self, 
                             student_id: str,
                             start_date: date,
                             end_date: date) -> List[Dict]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM daily_attendance
                    WHERE student_id = ? AND date BETWEEN ? AND ?
                    ORDER BY date
                ''', (student_id, start_date, end_date))
                
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            self.logger.error(f"Error retrieving student attendance: {str(e)}")
            return []

    def generate_monthly_report(self, 
                              class_name: str,
                              month: int,
                              year: int) -> pd.DataFrame:
        try:
            with sqlite3.connect(self.db_path) as conn:
                query = '''
                    SELECT 
                        s.roll_number,
                        s.name,
                        da.date,
                        da.status,
                        da.entry_time,
                        da.exit_time
                    FROM students s
                    LEFT JOIN daily_attendance da 
                        ON s.student_id = da.student_id
                        AND strftime('%m', da.date) = ?
                        AND strftime('%Y', da.date) = ?
                    WHERE s.class = ?
                    ORDER BY s.roll_number, da.date
                '''
                
                df = pd.read_sql_query(
                    query, 
                    conn, 
                    params=(f"{month:02d}", str(year), class_name)
                )
                
                # Pivot table for monthly view
                report = df.pivot_table(
                    index=['roll_number', 'name'],
                    columns='date',
                    values='status',
                    aggfunc='first',
                    fill_value='absent'
                )
                
                # Add summary columns
                report['Total Present'] = (report == 'present').sum(axis=1)
                report['Total Absent'] = (report == 'absent').sum(axis=1)
                report['Total Late'] = (report == 'late').sum(axis=1)
                report['Total Half-Day'] = (report == 'half-day').sum(axis=1)
                
                return report
                
        except Exception as e:
            self.logger.error(f"Error generating monthly report: {str(e)}")
            return pd.DataFrame()

    def add_holiday(self, holiday_data: Dict) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO holidays (date, description, holiday_type, applies_to)
                    VALUES (?, ?, ?, ?)
                ''', (
                    holiday_data['date'],
                    holiday_data['description'],
                    holiday_data['holiday_type'],
                    holiday_data.get('applies_to')
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Error adding holiday: {str(e)}")
            return False

    def update_attendance_settings(self, settings_data: Dict) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO attendance_settings (
                        class, start_time, late_threshold,
                        half_day_threshold, minimum_hours, active
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    settings_data['class'],
                    settings_data['start_time'],
                    settings_data['late_threshold'],
                    settings_data['half_day_threshold'],
                    settings_data['minimum_hours'],
                    settings_data.get('active', True)
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Error updating attendance settings: {str(e)}")
            return False

    def get_attendance_statistics(self, 
                                class_name: str,
                                start_date: date,
                                end_date: date) -> Dict:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_records,
                        SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present_count,
                        SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent_count,
                        SUM(CASE WHEN status = 'late' THEN 1 ELSE 0 END) as late_count,
                        SUM(CASE WHEN status = 'half-day' THEN 1 ELSE 0 END) as half_day_count,
                        AVG(CASE WHEN status = 'present' THEN 1 ELSE 0 END) * 100 as attendance_percentage
                    FROM daily_attendance da
                    JOIN students s ON da.student_id = s.student_id
                    WHERE s.class = ? AND da.date BETWEEN ? AND ?
                ''', (class_name, start_date, end_date))
                
                result = cursor.fetchone()
                return {
                    'total_records': result[0],
                    'present_count': result[1],
                    'absent_count': result[2],
                    'late_count': result[3],
                    'half_day_count': result[4],
                    'attendance_percentage': result[5]
                }
                
        except Exception as e:
            self.logger.error(f"Error calculating attendance statistics: {str(e)}")
            return {}