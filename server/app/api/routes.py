from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import List
import logging
from app.core.face_processor import FaceProcessor, WebImageSearcher
from app.models.image import ImageMatch

router = APIRouter()
logger = logging.getLogger(__name__)

face_processor = FaceProcessor()
web_searcher = WebImageSearcher()

@router.post("/search", response_model=List[ImageMatch])
async def search_face(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        contents = await file.read()
        
        # Extract face embedding
        embedding, face_boxes = face_processor.extract_face_embedding(contents)
        
        if not embedding.any():
            raise HTTPException(status_code=400, detail="No face detected in the image")
        
        # Search for similar faces
        results = await web_searcher.search_similar_faces(embedding)
        
        # Sort by similarity score
        results.sort(key=lambda x: x['similarity'], reverse=True)
        
        return results
        
    except Exception as e:
        logger.error(f"Error in face search: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))