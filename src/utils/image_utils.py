import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime
import os

class ImageUtils:
    def __init__(self, log_dir: str = "logs"):
        self.setup_logging(log_dir)

    def setup_logging(self, log_dir: str) -> None:
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f'image_utils_{datetime.now().strftime("%Y%m%d")}.log')
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def resize_image(self, 
                    image: np.ndarray, 
                    target_size: Tuple[int, int],
                    keep_aspect_ratio: bool = True) -> np.ndarray:
        try:
            if keep_aspect_ratio:
                h, w = image.shape[:2]
                target_w, target_h = target_size
                aspect = w / h
                
                if w > h:
                    new_w = target_w
                    new_h = int(target_w / aspect)
                else:
                    new_h = target_h
                    new_w = int(target_h * aspect)
                    
                resized = cv2.resize(image, (new_w, new_h))
                
                # Pad if necessary
                delta_w = target_w - new_w
                delta_h = target_h - new_h
                top, bottom = delta_h//2, delta_h-(delta_h//2)
                left, right = delta_w//2, delta_w-(delta_w//2)
                
                padded = cv2.copyMakeBorder(resized, top, bottom, left, right,
                                          cv2.BORDER_CONSTANT, value=[0, 0, 0])
                return padded
            else:
                return cv2.resize(image, target_size)
                
        except Exception as e:
            self.logger.error(f"Error resizing image: {str(e)}")
            return image

    def enhance_image(self, 
                     image: np.ndarray,
                     brightness: float = 1.0,
                     contrast: float = 1.0) -> np.ndarray:
        try:
            # Convert to float for calculations
            enhanced = image.astype(float)
            
            # Adjust brightness
            enhanced *= brightness
            
            # Adjust contrast
            enhanced = (enhanced - 128) * contrast + 128
            
            # Clip values and convert back to uint8
            enhanced = np.clip(enhanced, 0, 255).astype(np.uint8)
            
            return enhanced
            
        except Exception as e:
            self.logger.error(f"Error enhancing image: {str(e)}")
            return image

    def normalize_lighting(self, image: np.ndarray) -> np.ndarray:
        try:
            # Convert to LAB color space
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            
            # Apply CLAHE to L channel
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            cl = clahe.apply(l)
            
            # Merge channels
            normalized = cv2.merge([cl, a, b])
            
            # Convert back to BGR
            return cv2.cvtColor(normalized, cv2.COLOR_LAB2BGR)
            
        except Exception as e:
            self.logger.error(f"Error normalizing lighting: {str(e)}")
            return image

    def remove_noise(self, 
                    image: np.ndarray,
                    method: str = 'gaussian') -> np.ndarray:
        try:
            if method == 'gaussian':
                return cv2.GaussianBlur(image, (5, 5), 0)
            elif method == 'median':
                return cv2.medianBlur(image, 5)
            elif method == 'bilateral':
                return cv2.bilateralFilter(image, 9, 75, 75)
            else:
                return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
                
        except Exception as e:
            self.logger.error(f"Error removing noise: {str(e)}")
            return image

    def align_face(self, 
                  image: np.ndarray,
                  landmarks: List[Tuple[int, int]]) -> Optional[np.ndarray]:
        try:
            if len(landmarks) < 2:
                return image
                
            # Get eyes coordinates
            left_eye = landmarks[0]
            right_eye = landmarks[1]
            
            # Calculate angle for rotation
            dy = right_eye[1] - left_eye[1]
            dx = right_eye[0] - left_eye[0]
            angle = np.degrees(np.arctan2(dy, dx))
            
            # Get center point between eyes
            eye_center = ((left_eye[0] + right_eye[0])//2,
                         (left_eye[1] + right_eye[1])//2)
            
            # Get rotation matrix
            M = cv2.getRotationMatrix2D(eye_center, angle, 1.0)
            
            # Perform rotation
            height, width = image.shape[:2]
            aligned = cv2.warpAffine(image, M, (width, height),
                                   flags=cv2.INTER_CUBIC)
            
            return aligned
            
        except Exception as e:
            self.logger.error(f"Error aligning face: {str(e)}")
            return image

    def crop_face(self, 
                 image: np.ndarray,
                 bbox: Tuple[int, int, int, int],
                 margin: float = 0.3) -> Optional[np.ndarray]:
        try:
            x, y, w, h = bbox
            
            # Calculate margins
            margin_x = int(w * margin)
            margin_y = int(h * margin)
            
            # Calculate crop boundaries
            top = max(0, y - margin_y)
            bottom = min(image.shape[0], y + h + margin_y)
            left = max(0, x - margin_x)
            right = min(image.shape[1], x + w + margin_x)
            
            return image[top:bottom, left:right]
            
        except Exception as e:
            self.logger.error(f"Error cropping face: {str(e)}")
            return None

    def draw_face_box(self,
                     image: np.ndarray,
                     bbox: Tuple[int, int, int, int],
                     name: Optional[str] = None,
                     confidence: Optional[float] = None,
                     color: Tuple[int, int, int] = (0, 255, 0)) -> np.ndarray:
        try:
            x, y, w, h = bbox
            annotated = image.copy()
            
            # Draw bounding box
            cv2.rectangle(annotated, (x, y), (x+w, y+h), color, 2)
            
            # Add text if provided
            if name or confidence:
                text = []
                if name:
                    text.append(name)
                if confidence:
                    text.append(f"{confidence:.1f}%")
                    
                label = " | ".join(text)
                
                # Calculate text size and position
                font = cv2.FONT_HERSHEY_SIMPLEX
                scale = 0.6
                thickness = 2
                (text_w, text_h), baseline = cv2.getTextSize(label, font, scale, thickness)
                
                # Draw text background
                cv2.rectangle(annotated, 
                            (x, y - text_h - baseline - 10),
                            (x + text_w, y),
                            color, 
                            cv2.FILLED)
                
                # Draw text
                cv2.putText(annotated, 
                           label,
                           (x, y - baseline - 5),
                           font,
                           scale,
                           (255, 255, 255),
                           thickness)
            
            return annotated
            
        except Exception as e:
            self.logger.error(f"Error drawing face box: {str(e)}")
            return image

    def save_image(self,
                  image: np.ndarray,
                  filename: str,
                  output_dir: str = "data/processed_images") -> bool:
        try:
            os.makedirs(output_dir, exist_ok=True)
            filepath = os.path.join(output_dir, filename)
            return cv2.imwrite(filepath, image)
            
        except Exception as e:
            self.logger.error(f"Error saving image: {str(e)}")
            return False

    @staticmethod
    def get_image_quality(image: np.ndarray) -> Dict[str, float]:
        """Calculate various image quality metrics."""
        try:
            metrics = {}
            
            # Calculate brightness
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            metrics['brightness'] = np.mean(gray)
            
            # Calculate contrast
            metrics['contrast'] = np.std(gray)
            
            # Calculate sharpness using Laplacian
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            metrics['sharpness'] = np.var(laplacian)
            
            # Calculate noise level
            noise = np.std(gray) / np.mean(gray) if np.mean(gray) > 0 else 0
            metrics['noise_level'] = noise
            
            return metrics
            
        except Exception as e:
            logging.error(f"Error calculating image quality: {str(e)}")
            return {}