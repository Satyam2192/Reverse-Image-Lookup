import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.database import db
import app.core.engine_instance as eng  

app = FastAPI(title="Image Search Engine")

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting application...")
    try:
        # Connect to MongoDB
        await db.connect_db()
        logger.info("MongoDB connection established")

        # Initialize search engine
        logger.info("Initializing search engine...")
        eng.init_search_engine()  # <--- Use the function from eng
        if eng.search_engine:
            logger.info("Search engine initialized successfully")
        else:
            logger.error("Search engine initialization failed")

    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    await db.close_db()
    logger.info("Application shutdown complete.")

# Include API routes
app.include_router(router, prefix="/api")
