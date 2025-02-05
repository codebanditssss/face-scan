# settings.py

# Database Configuration
DATABASE = {
    'path': 'data/database/students.db',
    'backup_dir': 'data/database/backups'
}

# Face Recognition Settings
FACE_RECOGNITION = {
    'min_face_size': (30, 30),
    'scale_factor': 1.1,
    'min_neighbors': 5,
    'match_threshold': 70.0,
    'target_size': (100, 100),
    'detection_model': 'hog',  # or 'cnn' for GPU
}

# Camera Settings
CAMERA = {
    'device_id': 0,
    'frame_width': 640,
    'frame_height': 480,
    'fps': 30
}

# File Storage
STORAGE = {
    'student_images': 'data/student_images',
    'attendance_reports': 'data/attendance',
    'logs': 'logs',
    'temp': 'data/temp'
}

# Attendance Rules
ATTENDANCE = {
    'late_threshold': 15,  # minutes
    'half_day_threshold': 240,  # minutes
    'minimum_attendance': 75,  # percentage
    'verification_required': True,
    'allow_multiple_entries': False
}

# UI Settings
UI = {
    'window_title': 'Face Recognition Attendance System',
    'theme': 'light',
    'font_size': 12,
    'success_color': (0, 255, 0),
    'error_color': (0, 0, 255),
    'warning_color': (0, 255, 255)
}

# Email Notifications
EMAIL = {
    'enabled': False,
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': '',
    'password': '',
    'use_tls': True
}

# Backup Settings
BACKUP = {
    'auto_backup': True,
    'backup_interval': 24,  # hours
    'keep_backups': 7,  # days
    'compress_backup': True
}

# Logging Configuration
LOGGING = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file_rotation': 7,  # days
    'max_size': 10485760  # 10MB
}

# Security Settings
SECURITY = {
    'require_login': True,
    'session_timeout': 30,  # minutes
    'max_login_attempts': 3,
    'password_expiry': 90,  # days
    'min_password_length': 8
}

# Report Generation
REPORTS = {
    'default_format': 'xlsx',
    'include_photos': False,
    'chart_type': 'bar',
    'date_format': '%Y-%m-%d',
    'time_format': '%H:%M:%S'
}

# System Maintenance
MAINTENANCE = {
    'cleanup_interval': 30,  # days
    'archive_old_records': True,
    'archive_after': 365,  # days
    'optimize_db': True
}