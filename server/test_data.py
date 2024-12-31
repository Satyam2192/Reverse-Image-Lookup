# test_data.py
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.image_processor import ImageProcessor
from app.core.search_engine import SearchEngine
import aiohttp
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def add_test_data():
    # Connect to MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.image_search
    
    # Initialize search engine
    search_engine = SearchEngine()
    
    # Sample image URLs (replace with actual working image URLs)
    test_images = [
        "https://picsum.photos/200/300",
        "https://picsum.photos/200/301",
        "https://picsum.photos/200/302",
    ]
    
    processor = ImageProcessor()
    
    async with aiohttp.ClientSession() as session:
        for url in test_images:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        img_data = await response.read()
                        img_hash, features = processor.process_image(img_data)
                        
                        # Save to MongoDB
                        doc = {
                            "url": url,
                            "hash": img_hash,
                            "feature_vector": features
                        }
                        result = await db.images.insert_one(doc)
                        
                        # Index in Redis
                        await search_engine.index_vector(str(result.inserted_id), features)
                        
                        logger.info(f"Added test image: {url}")
                    
            except Exception as e:
                logger.error(f"Error processing {url}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(add_test_data())