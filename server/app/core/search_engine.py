# app/core/search_engine.py
import redis
import numpy as np
import logging
from app.config import get_settings

logger = logging.getLogger(__name__)

class SearchEngine:
    def __init__(self):
        self.settings = get_settings()
        self.index_name = "image_vectors"
        
        logger.info(f"Connecting to Redis at {self.settings.REDIS_HOST}:{self.settings.REDIS_PORT}")
        
        # Connect to Redis
        try:
            self.redis_client = redis.Redis(
                host=self.settings.REDIS_HOST,
                port=self.settings.REDIS_PORT,
                decode_responses=False,  # Changed to False for binary data
                socket_connect_timeout=5
            )
            # Test connection
            self.redis_client.ping()
            logger.info("Successfully connected to Redis")
            
            self._ensure_index()
            logger.info("Redis index initialization complete")
            
        except Exception as e:
            logger.error(f"Redis connection error: {str(e)}")
            raise

    def _ensure_index(self):
        try:
            # Check if index exists
            try:
                existing_indices = self.redis_client.execute_command("FT._LIST")
                logger.info(f"Existing indices: {existing_indices}")
            except redis.exceptions.ResponseError as e:
                if "unknown command" in str(e).lower():
                    logger.error("RediSearch module not loaded. Please ensure you're using Redis Stack.")
                    raise Exception("RediSearch module not available")
                raise

            if self.index_name.encode() not in existing_indices:
                logger.info(f"Creating new index: {self.index_name}")
                # Create index for vector similarity search
                self.redis_client.execute_command(
                    "FT.CREATE", self.index_name,
                    "ON", "HASH",
                    "PREFIX", "1", "image:",
                    "SCHEMA",
                    "vector", "VECTOR", "FLAT",
                    "6", "TYPE", "FLOAT32",
                    "DIM", str(self.settings.VECTOR_DIMENSION),
                    "DISTANCE_METRIC", "L2"
                )
                logger.info("Index created successfully")
            else:
                logger.info(f"Index {self.index_name} already exists")
                
        except redis.exceptions.ResponseError as e:
            if "Index already exists" not in str(e):
                logger.error(f"Error ensuring index: {str(e)}")
                raise
            logger.info("Index already exists, continuing...")

    async def index_vector(self, doc_id: str, vector: list):
        # Convert vector to bytes
        vector_bytes = np.array(vector, dtype=np.float32).tobytes()
        
        # Store in Redis
        self.redis_client.hset(
            f"image:{doc_id}",
            mapping={
                "vector": vector_bytes,
                "id": doc_id
            }
        )

    async def search(self, query_vector: list, limit: int = 10):
        # Convert query vector to bytes
        query_vector_bytes = np.array(query_vector, dtype=np.float32).tobytes()
        
        # Perform vector similarity search using the correct RediSearch syntax
        query = f"*=>[KNN {limit} @vector $BLOB AS distance]"
        
        try:
            results = self.redis_client.execute_command(
                "FT.SEARCH", self.index_name,
                query,
                "PARAMS", "2", "BLOB", query_vector_bytes,
                "RETURN", "2", "id", "distance",
                "SORTBY", "distance",
                "DIALECT", "2"
            )
            
            # Parse results
            matches = []
            if results and len(results) > 1:  # First element is result count
                for i in range(1, len(results), 2):  # Skip every other element (document ID)
                    doc_id = results[i].decode('utf-8').replace('image:', '')  # Remove prefix
                    doc_data = {k.decode('utf-8'): v for k, v in zip(results[i + 1][::2], results[i + 1][1::2])}
                    
                    if 'distance' in doc_data:
                        distance = float(doc_data['distance'])
                        matches.append((doc_id, distance))
            
            return matches

        except redis.exceptions.ResponseError as e:
            logger.error(f"Search error: {str(e)}")
            raise