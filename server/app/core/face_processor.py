# app/core/face_processor.py
import numpy as np
from PIL import Image
from io import BytesIO
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
import requests
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

class FaceProcessor:
    def __init__(self):
        # Initialize face detection and recognition models
        self.mtcnn = MTCNN(keep_all=True)
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval()

    def extract_face_embedding(self, image_data: bytes) -> Tuple[np.ndarray, List[tuple]]:
        """Extract face embedding from image"""
        try:
            # Convert bytes to PIL Image
            image = Image.open(BytesIO(image_data)).convert('RGB')

            # Detect faces
            boxes, _ = self.mtcnn.detect(image)

            if boxes is None or len(boxes) == 0:
                raise ValueError("No faces detected in the image")

            # Get the largest face (assuming it's the main subject)
            box = boxes[0]
            face = image.crop((int(box[0]), int(box[1]), int(box[2]), int(box[3]))) # Ensure integer coordinates

            # Convert to tensor and get embedding
            face_tensor = self.mtcnn(face)
            if face_tensor is None:
                raise ValueError("Failed to process face")

            # Print the shape for debugging
            logger.info(f"Shape of face_tensor before processing: {face_tensor.shape}")

            # Remove unnecessary dimensions of size 1
            face_tensor = torch.squeeze(face_tensor)

            # Print the shape after squeezing
            logger.info(f"Shape of face_tensor after squeezing: {face_tensor.shape}")

            # Add a batch dimension if necessary (resnet expects 4D input)
            if face_tensor.ndim == 3:
                face_tensor = face_tensor.unsqueeze(0)

            with torch.no_grad():
                embedding = self.resnet(face_tensor)

            return embedding.numpy()[0], boxes.tolist()

        except Exception as e:
            logger.error(f"Error processing face: {str(e)}")
            raise

class WebImageSearcher:
    def __init__(self):
        self.search_apis = {
            "google": "YOUR_GOOGLE_SEARCH_API_KEY",
            "bing": "YOUR_BING_SEARCH_API_KEY"
        }

    async def search_similar_faces(self, embedding: np.ndarray, limit: int = 20) -> List[dict]:
        """Search for similar faces using web APIs"""
        # This is a placeholder - you would need to implement actual API calls
        # For now, returning mock data
        return [
            {
                "url": "https://example.com/face1.jpg",
                "source_url": "https://example.com/profile1",
                "similarity": 95.5
            },
            # Add more results...
        ]

    async def download_and_process_image(self, url: str) -> bytes:
        """Download and return image bytes"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.read()
        return None