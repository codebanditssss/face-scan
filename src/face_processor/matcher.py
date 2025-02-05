import cv2
import numpy as np
from typing import Dict, Tuple, Optional, List
import os
import logging
from datetime import datetime
import json

class FaceMatcher:
    """Class to handle face matching operations."""
    
    def __init__(self, 
                 match_threshold: float = 70.0,
                 feature_weights: Optional[Dict[str, float]] = None,
                 database_path: str = "data/known_faces.json",
                 log_dir: str = "logs"):
        """
        Initialize FaceMatcher.

        Args:
            match_threshold: Minimum percentage match required
            feature_weights: Weights for different comparison metrics
            database_path: Path to save known faces database
            log_dir: Directory for logging
        """
        self.known_faces: Dict[str, Dict] = {}
        self.match_threshold = match_threshold
        self.database_path = database_path
        self.feature_weights = feature_weights or {
            'template_matching': 0.6,
            'histogram_correlation': 0.2,
            'structural_similarity': 0.2
        }
        
        # Setup logging
        self.setup_logging(log_dir)
        
        # Load existing database if available
        self.load_database()

    def setup_logging(self, log_dir: str) -> None:
        """Setup logging configuration."""
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_file = os.path.join(log_dir, f'face_matcher_{datetime.now().strftime("%Y%m%d")}.log')
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def load_database(self) -> None:
        """Load known faces database from file."""
        try:
            if os.path.exists(self.database_path):
                with open(self.database_path, 'r') as f:
                    data = json.load(f)
                    
                for student_id, info in data.items():
                    # Convert base64 image data back to numpy array
                    face_data = np.array(info['face_data'], dtype=np.uint8)
                    self.known_faces[student_id] = {
                        'face_data': face_data,
                        'metadata': info.get('metadata', {})
                    }
                    
                self.logger.info(f"Loaded {len(self.known_faces)} faces from database")
        except Exception as e:
            self.logger.error(f"Error loading database: {str(e)}")

    def save_database(self) -> None:
        """Save known faces database to file."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.database_path), exist_ok=True)
            
            # Convert database to serializable format
            data = {}
            for student_id, info in self.known_faces.items():
                data[student_id] = {
                    'face_data': info['face_data'].tolist(),
                    'metadata': info.get('metadata', {})
                }
                
            with open(self.database_path, 'w') as f:
                json.dump(data, f)
                
            self.logger.info("Database saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving database: {str(e)}")

    def add_face(self, 
                student_id: str, 
                face_image: np.ndarray, 
                metadata: Optional[Dict] = None) -> bool:
        """
        Add a face to known faces database.
        
        Args:
            student_id: Unique identifier for the student
            face_image: Preprocessed face image
            metadata: Additional information about the student
            
        Returns:
            Success status
        """
        try:
            if face_image is not None:
                self.known_faces[student_id] = {
                    'face_data': face_image,
                    'metadata': metadata or {}
                }
                self.save_database()
                self.logger.info(f"Added face for student {student_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error adding face: {str(e)}")
            return False

    def load_faces_from_directory(self, 
                                directory: str, 
                                metadata_file: Optional[str] = None) -> None:
        """
        Load all face images from a directory.
        
        Args:
            directory: Directory containing face images
            metadata_file: Optional JSON file with student metadata
        """
        try:
            # Load metadata if provided
            metadata = {}
            if metadata_file and os.path.exists(metadata_file):
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
            
            for filename in os.listdir(directory):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    student_id = os.path.splitext(filename)[0]
                    image_path = os.path.join(directory, filename)
                    
                    # Load and preprocess image
                    face_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                    
                    if face_image is not None:
                        self.add_face(student_id, face_image, metadata.get(student_id))
                        
            self.logger.info(f"Loaded {len(self.known_faces)} faces from directory")
        except Exception as e:
            self.logger.error(f"Error loading faces from directory: {str(e)}")

    def calculate_histogram_correlation(self, 
                                     face1: np.ndarray, 
                                     face2: np.ndarray) -> float:
        """Calculate correlation between face histograms."""
        try:
            hist1 = cv2.calcHist([face1], [0], None, [256], [0, 256])
            hist2 = cv2.calcHist([face2], [0], None, [256], [0, 256])
            
            correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
            return max(0, correlation) * 100
        except Exception as e:
            self.logger.error(f"Error calculating histogram correlation: {str(e)}")
            return 0.0

    def calculate_structural_similarity(self, 
                                     face1: np.ndarray, 
                                     face2: np.ndarray) -> float:
        """Calculate structural similarity between faces."""
        try:
            if face1.shape != face2.shape:
                face2 = cv2.resize(face2, (face1.shape[1], face1.shape[0]))
            
            similarity = cv2.matchTemplate(face1, face2, cv2.TM_CCOEFF_NORMED)[0][0]
            return max(0, similarity) * 100
        except Exception as e:
            self.logger.error(f"Error calculating structural similarity: {str(e)}")
            return 0.0

    def compare_faces(self, 
                     face1: np.ndarray, 
                     face2: np.ndarray) -> float:
        """
        Compare two faces using multiple metrics.
        
        Args:
            face1: First face image
            face2: Second face image
            
        Returns:
            Weighted match percentage
        """
        try:
            # Ensure same size
            if face1.shape != face2.shape:
                face2 = cv2.resize(face2, (face1.shape[1], face1.shape[0]))

            # Calculate different similarity metrics
            template_match = cv2.matchTemplate(face1, face2, cv2.TM_CCOEFF_NORMED)[0][0] * 100
            histogram_corr = self.calculate_histogram_correlation(face1, face2)
            structural_sim = self.calculate_structural_similarity(face1, face2)

            # Calculate weighted average
            weighted_score = (
                self.feature_weights['template_matching'] * template_match +
                self.feature_weights['histogram_correlation'] * histogram_corr +
                self.feature_weights['structural_similarity'] * structural_sim
            )

            return max(0.0, min(100.0, weighted_score))

        except Exception as e:
            self.logger.error(f"Error comparing faces: {str(e)}")
            return 0.0

    def find_best_match(self, 
                       face: np.ndarray,
                       min_threshold: Optional[float] = None) -> Tuple[Optional[str], float, Optional[Dict]]:
        """
        Find best matching face from known faces.
        
        Args:
            face: Input face image
            min_threshold: Optional override for match threshold
            
        Returns:
            Tuple of (student_id, match_score, metadata)
        """
        try:
            best_match = None
            highest_score = 0.0
            match_metadata = None
            threshold = min_threshold or self.match_threshold

            for student_id, info in self.known_faces.items():
                known_face = info['face_data']
                score = self.compare_faces(face, known_face)
                
                if score > highest_score:
                    highest_score = score
                    best_match = student_id
                    match_metadata = info.get('metadata')

            if highest_score >= threshold:
                return best_match, highest_score, match_metadata
            return None, highest_score, None

        except Exception as e:
            self.logger.error(f"Error finding best match: {str(e)}")
            return None, 0.0, None

    def update_face(self, 
                   student_id: str, 
                   new_face: np.ndarray,
                   new_metadata: Optional[Dict] = None) -> bool:
        """
        Update existing face in database.
        
        Args:
            student_id: Student identifier
            new_face: New face image
            new_metadata: Optional updated metadata
            
        Returns:
            Success status
        """
        try:
            if student_id in self.known_faces:
                current_metadata = self.known_faces[student_id].get('metadata', {})
                updated_metadata = {**current_metadata, **(new_metadata or {})}
                
                self.known_faces[student_id] = {
                    'face_data': new_face,
                    'metadata': updated_metadata
                }
                
                self.save_database()
                self.logger.info(f"Updated face for student {student_id}")
                return True
                
            return False
        except Exception as e:
            self.logger.error(f"Error updating face: {str(e)}")
            return False

    def remove_face(self, student_id: str) -> bool:
        """
        Remove a face from known faces database.
        
        Args:
            student_id: Student identifier
            
        Returns:
            Success status
        """
        try:
            if student_id in self.known_faces:
                self.known_faces.pop(student_id)
                self.save_database()
                self.logger.info(f"Removed face for student {student_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error removing face: {str(e)}")
            return False

    def get_student_info(self, student_id: str) -> Optional[Dict]:
        """Get student information from database."""
        return self.known_faces.get(student_id, {}).get('metadata')

    def get_all_students(self) -> List[Dict]:
        """Get list of all students with their information."""
        return [
            {
                'student_id': student_id,
                'metadata': info.get('metadata', {})
            }
            for student_id, info in self.known_faces.items()
        ]

    def clear_database(self) -> None:
        """Clear all entries from the database."""
        self.known_faces.clear()
        self.save_database()
        self.logger.info("Database cleared")