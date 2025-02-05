import cv2
import numpy as np
from typing import Tuple, List, Optional, Dict
import logging
import os
from datetime import datetime

class FaceDetector:
    """A class to handle face detection operations."""
    
    def __init__(self, 
                 min_confidence: float = 0.7,
                 min_face_size: Tuple[int, int] = (30, 30),
                 scale_factor: float = 1.1,
                 min_neighbors: int = 5,
                 target_size: Tuple[int, int] = (100, 100),
                 log_dir: str = "logs"):
        """
        Initialize the FaceDetector.
        
        Args:
            min_confidence: Minimum confidence threshold for face detection
            min_face_size: Minimum size of face to detect (width, height)
            scale_factor: Scale factor for cascade classifier
            min_neighbors: Minimum neighbors parameter for cascade classifier
            target_size: Target size for face normalization
            log_dir: Directory for logging
        """
        # Initialize cascade classifier
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        if not os.path.exists(cascade_path):
            raise FileNotFoundError(f"Cascade classifier not found at {cascade_path}")
        
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        # Detection parameters
        self.min_confidence = min_confidence
        self.min_face_size = min_face_size
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.target_size = target_size
        
        # Setup logging
        self.setup_logging(log_dir)
        
    def setup_logging(self, log_dir: str) -> None:
        """Setup logging configuration."""
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_file = os.path.join(log_dir, f'face_detector_{datetime.now().strftime("%Y%m%d")}.log')
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def detect_faces(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in the given frame.
        
        Args:
            frame: Input image frame
            
        Returns:
            List of face locations as (x, y, width, height)
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=self.scale_factor,
                minNeighbors=self.min_neighbors,
                minSize=self.min_face_size,
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            self.logger.info(f"Detected {len(faces)} faces in frame")
            return faces
            
        except Exception as e:
            self.logger.error(f"Error in face detection: {str(e)}")
            return []

    def extract_face(self, 
                    frame: np.ndarray, 
                    face_location: Tuple[int, int, int, int],
                    margin: float = 0.0) -> Optional[np.ndarray]:
        """
        Extract face region from frame with optional margin.
        
        Args:
            frame: Input image frame
            face_location: Face location as (x, y, width, height)
            margin: Margin to add around face (percentage of face size)
            
        Returns:
            Extracted face image or None if extraction fails
        """
        try:
            x, y, w, h = face_location
            
            # Calculate margins
            margin_x = int(w * margin)
            margin_y = int(h * margin)
            
            # Calculate boundaries with margins
            top = max(0, y - margin_y)
            bottom = min(frame.shape[0], y + h + margin_y)
            left = max(0, x - margin_x)
            right = min(frame.shape[1], x + w + margin_x)
            
            return frame[top:bottom, left:right]
            
        except Exception as e:
            self.logger.error(f"Error extracting face: {str(e)}")
            return None

    def preprocess_face(self, 
                       face_img: np.ndarray,
                       target_size: Optional[Tuple[int, int]] = None) -> Optional[np.ndarray]:
        """
        Preprocess face image for recognition.
        
        Args:
            face_img: Input face image
            target_size: Optional target size for resizing
            
        Returns:
            Preprocessed face image or None if preprocessing fails
        """
        try:
            if face_img is None:
                return None
                
            # Use instance target size if none provided
            if target_size is None:
                target_size = self.target_size
            
            # Convert to grayscale if needed
            if len(face_img.shape) == 3:
                face_gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            else:
                face_gray = face_img
                
            # Resize
            face_resized = cv2.resize(face_gray, target_size)
            
            # Normalize lighting
            face_normalized = cv2.equalizeHist(face_resized)
            
            # Apply additional preprocessing
            face_preprocessed = self.enhance_face(face_normalized)
            
            return face_preprocessed
            
        except Exception as e:
            self.logger.error(f"Error preprocessing face: {str(e)}")
            return None

    def enhance_face(self, face_img: np.ndarray) -> np.ndarray:
        """
        Apply enhancement techniques to face image.
        
        Args:
            face_img: Input face image
            
        Returns:
            Enhanced face image
        """
        # Denoise
        denoised = cv2.fastNlMeansDenoising(face_img)
        
        # Enhance contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        return enhanced

    def detect_and_process(self, 
                         frame: np.ndarray,
                         margin: float = 0.1) -> Tuple[List[Tuple[int, int, int, int]], 
                                                     List[np.ndarray]]:
        """
        Detect faces and return their locations and preprocessed images.
        
        Args:
            frame: Input image frame
            margin: Margin to add around detected faces
            
        Returns:
            Tuple of (face_locations, processed_faces)
        """
        try:
            # Detect faces
            face_locations = self.detect_faces(frame)
            processed_faces = []
            
            # Process each detected face
            for face_location in face_locations:
                # Extract face with margin
                face = self.extract_face(frame, face_location, margin)
                
                # Preprocess face
                if face is not None:
                    processed_face = self.preprocess_face(face)
                    if processed_face is not None:
                        processed_faces.append(processed_face)
            
            self.logger.info(f"Successfully processed {len(processed_faces)} faces")
            return face_locations, processed_faces
            
        except Exception as e:
            self.logger.error(f"Error in detect_and_process: {str(e)}")
            return [], []

    def draw_detections(self, 
                       frame: np.ndarray,
                       face_locations: List[Tuple[int, int, int, int]],
                       labels: Optional[List[str]] = None,
                       scores: Optional[List[float]] = None) -> np.ndarray:
        """
        Draw detection boxes and labels on frame.
        
        Args:
            frame: Input image frame
            face_locations: List of face locations
            labels: Optional list of labels for each face
            scores: Optional list of confidence scores
            
        Returns:
            Frame with drawings
        """
        try:
            frame_copy = frame.copy()
            
            for idx, (x, y, w, h) in enumerate(face_locations):
                # Draw rectangle
                cv2.rectangle(frame_copy, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Add label and score if provided
                if labels is not None and idx < len(labels):
                    label = labels[idx]
                    score_text = f" ({scores[idx]:.1f}%)" if scores and idx < len(scores) else ""
                    text = f"{label}{score_text}"
                    
                    cv2.putText(frame_copy, text, (x, y-10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            return frame_copy
            
        except Exception as e:
            self.logger.error(f"Error drawing detections: {str(e)}")
            return frame
            
    def get_face_features(self, 
                         face_img: np.ndarray) -> Optional[Dict[str, float]]:
        """
        Extract facial features for additional analysis.
        
        Args:
            face_img: Preprocessed face image
            
        Returns:
            Dictionary of facial features or None if extraction fails
        """
        try:
            features = {}
            
            # Calculate average brightness
            features['brightness'] = cv2.mean(face_img)[0]
            
            # Calculate contrast
            features['contrast'] = face_img.std()
            
            # Calculate symmetry score
            center = face_img.shape[1] // 2
            left_side = face_img[:, :center]
            right_side = cv2.flip(face_img[:, center:], 1)
            features['symmetry'] = 100 - np.mean(np.abs(left_side - right_side))
            
            return features
            
        except Exception as e:
            self.logger.error(f"Error extracting face features: {str(e)}")
            return None