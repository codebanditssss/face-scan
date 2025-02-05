# thresholds.py

# Face Recognition Thresholds
FACE_DETECTION = {
    'MIN_FACE_SIZE': (30, 30),
    'SCALE_FACTOR': 1.1,
    'MIN_NEIGHBORS': 5,
    'CONFIDENCE_THRESHOLD': 0.7,
    'MAX_FACES_PER_FRAME': 10,
    'DETECTION_INTERVAL': 100  # milliseconds
}

# Face Matching Thresholds
FACE_MATCHING = {
    'MIN_MATCH_SCORE': 70.0,  # percentage
    'HIGH_CONFIDENCE': 85.0,
    'LOW_CONFIDENCE': 60.0,
    'MAX_ANGLE_DEVIATION': 30,  # degrees
    'MIN_FACE_QUALITY': 0.5
}

# Image Quality Thresholds
IMAGE_QUALITY = {
    'MIN_BRIGHTNESS': 40,
    'MAX_BRIGHTNESS': 240,
    'MIN_CONTRAST': 30,
    'MIN_SHARPNESS': 50,
    'MAX_BLUR': 100,
    'MIN_FACE_SIZE_PIXELS': 50,
    'OPTIMAL_FACE_SIZE': (100, 100)
}

# Attendance Time Thresholds (in minutes)
ATTENDANCE_TIME = {
    'LATE_THRESHOLD': 15,
    'HALF_DAY_THRESHOLD': 240,
    'MINIMUM_HOURS': 6,
    'GRACE_PERIOD': 5,
    'MIN_TIME_BETWEEN_ENTRIES': 30
}

# System Performance Thresholds
PERFORMANCE = {
    'MAX_PROCESSING_TIME': 2000,  # milliseconds
    'MAX_MEMORY_USAGE': 1024,     # MB
    'MAX_CPU_USAGE': 80,          # percentage
    'FRAME_RATE': 30,
    'RESOLUTION': (640, 480)
}

# Database Thresholds
DATABASE = {
    'MAX_CONNECTIONS': 100,
    'TIMEOUT': 30,              # seconds
    'MAX_RETRY_ATTEMPTS': 3,
    'BACKUP_FREQUENCY': 24,     # hours
    'MAX_BATCH_SIZE': 1000
}

# Storage Thresholds
STORAGE = {
    'MAX_IMAGE_SIZE': 1024 * 1024,  # 1MB
    'MAX_VIDEO_LENGTH': 60,         # seconds
    'MAX_LOG_SIZE': 100 * 1024 * 1024,  # 100MB
    'MIN_FREE_SPACE': 500 * 1024 * 1024  # 500MB
}

# Alert Thresholds
ALERTS = {
    'CONSECUTIVE_FAILURES': 3,
    'ERROR_RATE_THRESHOLD': 0.1,
    'WARNING_MEMORY_USAGE': 70,  # percentage
    'CRITICAL_MEMORY_USAGE': 90  # percentage
}

# Security Thresholds
SECURITY = {
    'MAX_LOGIN_ATTEMPTS': 3,
    'SESSION_TIMEOUT': 30,      # minutes
    'PASSWORD_EXPIRY': 90,      # days
    'MIN_PASSWORD_LENGTH': 8
}

# Maintenance Thresholds
MAINTENANCE = {
    'LOG_RETENTION': 30,        # days
    'TEMP_FILE_AGE': 24,        # hours
    'ARCHIVE_AGE': 365,         # days
    'CLEANUP_INTERVAL': 7       # days
}

# Report Generation Thresholds
REPORTS = {
    'MAX_ROWS_PER_PAGE': 50,
    'MAX_CHART_DATA_POINTS': 1000,
    'THUMBNAIL_SIZE': (100, 100),
    'MAX_REPORT_SIZE': 10 * 1024 * 1024  # 10MB
}