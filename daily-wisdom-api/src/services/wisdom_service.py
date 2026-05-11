from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.models.wisdom import WisdomEntry
from src.core.logging import logger

class WisdomService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_todays_wisdom(self) -> WisdomEntry | None:
        """Get wisdom for current UTC date using deterministic rotation"""
        try:
            # Get total count of wisdom entries
            count_result = await self.session.execute(
                select(func.count(WisdomEntry.id))
            )
            total_count = count_result.scalar()
            
            if total_count == 0:
                logger.warning("No wisdom entries found in database")
                return None
            
            # Calculate deterministic index
            today = datetime.utcnow().date()
            epoch = date(1970, 1, 1)
            days_since_epoch = (today - epoch).days
            wisdom_index = days_since_epoch % total_count
            
            logger.info(f"Selected wisdom index {wisdom_index} for {today}")
            
            # Get wisdom at calculated index
            result = await self.session.execute(
                select(WisdomEntry)
                .order_by(WisdomEntry.id)
                .offset(wisdom_index)
                .limit(1)
            )
            
            wisdom = result.scalar_one_or_none()
            if wisdom:
                logger.info(f"Retrieved wisdom: {wisdom.title[:50]}...")
            
            return wisdom
            
        except Exception as e:
            logger.error(f"Error getting today's wisdom: {e}")
            raise
    
    async def get_total_wisdom_count(self) -> int:
        """Get total count of wisdom entries"""
        try:
            result = await self.session.execute(
                select(func.count(WisdomEntry.id))
            )
            count = result.scalar()
            logger.info(f"Total wisdom count: {count}")
            return count
        except Exception as e:
            logger.error(f"Error getting wisdom count: {e}")
            raise
