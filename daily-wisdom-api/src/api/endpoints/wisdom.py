from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from src.core.database import get_session
from src.services.wisdom_service import WisdomService
from src.schemas.wisdom import WisdomResponse, HealthResponse
from src.core.exceptions import WisdomNotFoundError, DatabaseConnectionError
from src.core.logging import logger

router = APIRouter(prefix="/api/v1/wisdom", tags=["wisdom"])

@router.get("/today", response_model=WisdomResponse)
async def get_todays_wisdom(session: AsyncSession = Depends(get_session)):
    """Get wisdom content for current UTC date"""
    try:
        service = WisdomService(session)
        wisdom = await service.get_todays_wisdom()
        
        if wisdom is None:
            raise WisdomNotFoundError()
        
        return WisdomResponse(
            id=wisdom.id,
            title=wisdom.title,
            description=wisdom.description
        )
        
    except WisdomNotFoundError:
        logger.warning("No wisdom found for today")
        raise
    except Exception as e:
        logger.error(f"Error fetching today's wisdom: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )

@router.get("/health")
async def health_check(session: AsyncSession = Depends(get_session)):
    """Health check endpoint"""
    try:
        service = WisdomService(session)
        total_wisdom = await service.get_total_wisdom_count()
        
        return HealthResponse(
            status="healthy",
            timestamp=datetime.utcnow().isoformat(),
            version="1.0.0",
            database="connected",
            total_wisdom=total_wisdom
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.utcnow().isoformat(),
            version="1.0.0",
            database="disconnected",
            total_wisdom=None
        )
