"""
Script to update existing items with gfx_id extracted from raw_data

Usage:
    python worker/update_gfx_ids.py

Or via Docker:
    docker exec -it wakfu-builder-assistant-worker-1 python update_gfx_ids.py
"""

import os
import sys
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://wakfu:wakfu123@db:5432/wakfu_builder")

def update_gfx_ids():
    """Update items with gfx_id extracted from raw_data"""
    logger.info("Starting gfx_id update...")
    logger.info(f"Database URL: {DATABASE_URL}")
    
    try:
        # Create engine
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        
        # Create session
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Get items without gfx_id
        result = session.execute(
            text("SELECT item_id, raw_data FROM items WHERE gfx_id IS NULL AND raw_data IS NOT NULL")
        )
        
        items = result.fetchall()
        total_items = len(items)
        logger.info(f"Found {total_items} items to update")
        
        if total_items == 0:
            logger.info("No items need updating. All items already have gfx_id!")
            return
        
        updated_count = 0
        failed_count = 0
        
        for idx, (item_id, raw_data) in enumerate(items, 1):
            try:
                # Extract gfx_id from raw_data
                if raw_data and isinstance(raw_data, dict):
                    gfx_id = (
                        raw_data.get('definition', {})
                        .get('item', {})
                        .get('graphicParameters', {})
                        .get('gfxId')
                    )
                    
                    if gfx_id:
                        # Update item
                        session.execute(
                            text("UPDATE items SET gfx_id = :gfx_id WHERE item_id = :item_id"),
                            {"gfx_id": gfx_id, "item_id": item_id}
                        )
                        updated_count += 1
                        
                        if updated_count % 100 == 0:
                            session.commit()
                            logger.info(f"Progress: {idx}/{total_items} items processed, {updated_count} updated")
                    else:
                        logger.debug(f"Item {item_id}: No gfx_id found in raw_data")
                        failed_count += 1
                else:
                    logger.debug(f"Item {item_id}: raw_data is empty or invalid")
                    failed_count += 1
                    
            except Exception as e:
                logger.error(f"Error processing item {item_id}: {e}")
                failed_count += 1
                continue
        
        # Final commit
        session.commit()
        session.close()
        
        logger.info("=" * 60)
        logger.info(f"Update completed!")
        logger.info(f"Total items processed: {total_items}")
        logger.info(f"Successfully updated: {updated_count}")
        logger.info(f"Failed/Skipped: {failed_count}")
        logger.info("=" * 60)
        
        if updated_count > 0:
            logger.info("✅ Items successfully updated with gfx_id")
        
        if failed_count > 0:
            logger.warning(f"⚠️ {failed_count} items could not be updated (missing gfxId in raw_data)")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    update_gfx_ids()

