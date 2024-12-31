import logging
from app.core.search_engine import SearchEngine

logger = logging.getLogger(__name__)

# We define search_engine as a global variable here
search_engine = None

def init_search_engine():
    """
    Create and store a global SearchEngine instance.
    Call this once at startup.
    """
    global search_engine
    try:
        logger.info("Initializing SearchEngine...")
        engine = SearchEngine()
        search_engine = engine
        logger.info("SearchEngine initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize SearchEngine: {str(e)}")
        raise