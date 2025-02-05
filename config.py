import os
import cv2

class settings:
    # Base directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Data directories
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    STUDENT_IMAGES_DIR = os.path.join(DATA_DIR, 'student_images')
    ATTENDANCE_DIR = os.path.join(DATA_DIR, 'attendance')
    DATABASE_DIR = os.path.join(DATA_DIR, 'database')
    
    # Database
    DATABASE_PATH = os.path.join(DATABASE_DIR, 'students.db')
    DATABASE_BACKUP_DIR = os.path.join(DATABASE_DIR, 'backups')
    
    # Logs
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Face Recognition
    FACE_DETECTION_MODEL = 'hog'  # 'hog' or 'cnn'
    FACE_MATCH_THRESHOLD = 70.0
    MIN_FACE_SIZE = (30, 30)
    TARGET_FACE_SIZE = (100, 100)
    
    # Camera
    CAMERA_ID = 0
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    FPS = 30
    
    # Attendance Rules
    LATE_THRESHOLD = 15  # minutes
    HALF_DAY_THRESHOLD = 240  # minutes
    MINIMUM_ATTENDANCE = 75  # percentage
    
    # UI
    WINDOW_TITLE = 'Face Recognition Attendance System'
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.6
    FONT_THICKNESS = 2
    
    # Colors (BGR)
    SUCCESS_COLOR = (0, 255, 0)
    ERROR_COLOR = (0, 0, 255)
    WARNING_COLOR = (0, 255, 255)
    
    # File Extensions
    ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
    
    # Create required directories
    @classmethod
    def setup(cls):
        for directory in [cls.DATA_DIR, cls.STUDENT_IMAGES_DIR, 
                         cls.ATTENDANCE_DIR, cls.DATABASE_DIR,
                         cls.DATABASE_BACKUP_DIR, cls.LOG_DIR]:
            os.makedirs(directory, exist_ok=True)

# Initialize directories
settings.setup()