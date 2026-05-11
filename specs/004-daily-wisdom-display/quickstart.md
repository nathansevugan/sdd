# Quick Start Guide: Daily Wisdom Display

**Feature**: Daily Wisdom Display  
**Date**: 2026-05-10  
**Phase**: 1 - Design & Contracts

## Overview

This guide provides step-by-step instructions for setting up and running the daily wisdom display feature locally. It covers database setup, backend API, and frontend integration.

## Prerequisites

### System Requirements

- **Docker**: Required for PostgreSQL database
- **Node.js 18+**: For React frontend development
- **Python 3.12**: For FastAPI backend development
- **Git**: For version control

### Database Setup

**IMPORTANT**: Do NOT create or install PostgreSQL locally. Use the existing Docker instance.

```bash
# Verify PostgreSQL is running in Docker
docker ps | grep postgres

# Should show a running container with PostgreSQL
```

**Connection String** (from constitution):
```
postgresql+asyncpg://daily_wisdom_user:daily_wisdom_user@localhost:5432/daily_wisdom
```

## Project Setup

### 1. Repository Structure

```bash
daily-wisdom/
├── daily-wisdom-api/          # FastAPI backend
├── daily-wisdom-ui/           # React frontend
├── db-scripts/                # Database setup scripts
└── specs/                     # Feature specifications
```

### 2. Backend Setup (FastAPI)

```bash
cd daily-wisdom-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi sqlalchemy asyncpg alembic uvicorn
pip install pytest httpx  # For testing

# Create environment file
cat > .env << EOF
DATABASE_URL=postgresql+asyncpg://daily_wisdom_user:daily_wisdom_user@localhost:5432/daily_wisdom
ENVIRONMENT=development
LOG_LEVEL=info
EOF

# Create project structure
mkdir -p src/{models,services,api/endpoints,schemas,core}
mkdir -p tests/{unit,integration}
```

### 3. Frontend Setup (React)

```bash
cd daily-wisdom-ui

# Initialize React app (if not exists)
npx create-react-app . --template minimal
# Or use existing React setup

# Install additional dependencies
npm install @tanstack/react-query react-router-dom zustand
npm install --save-dev @testing-library/react @testing-library/jest-dom

# Create project structure
mkdir -p src/{components/{WisdomCard,common},pages,services,hooks,utils}
```

## Database Setup

### 1. Create Database Schema

```bash
cd daily-wisdom-api

# Initialize Alembic
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Create wisdom_entries table"
```

### 2. Migration File Content

Edit `alembic/versions/001_create_wisdom_entries.py`:

```python
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Create schema
    op.execute('CREATE SCHEMA IF NOT EXISTS app')
    
    # Create wisdom_entries table
    op.create_table(
        'wisdom_entries',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='app'
    )
    
    # Create indexes
    op.create_index('idx_wisdom_entries_deleted_at', 'wisdom_entries', ['deleted_at'], 
                   unique=False, schema='app', postgresql_where=sa.text('deleted_at IS NULL'))

def downgrade():
    op.drop_table('wisdom_entries', schema='app')
```

### 3. Apply Migration

```bash
# Apply migration to database
alembic upgrade head
```

### 4. Seed Initial Data

Create `seed_wisdom.py`:

```python
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.models.wisdom import WisdomEntry
from src.core.config import settings

async def seed_wisdom():
    engine = create_async_engine(settings.database_url)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    async with async_session() as session:
        wisdom_entries = [
            WisdomEntry(
                title="The only way to do great work is to love what you do.",
                description="Passion is the key to excellence and fulfillment in your work."
            ),
            WisdomEntry(
                title="Innovation distinguishes between a leader and a follower.",
                description="True leadership comes from creating new paths, not following existing ones."
            ),
            WisdomEntry(
                title="Stay hungry, stay foolish.",
                description="Maintain curiosity and embrace the unknown throughout your journey."
            ),
            # Add more wisdom entries...
        ]
        
        for wisdom in wisdom_entries:
            session.add(wisdom)
        
        await session.commit()
        print(f"Seeded {len(wisdom_entries)} wisdom entries")

if __name__ == "__main__":
    asyncio.run(seed_wisdom())
```

```bash
# Run seed script
python seed_wisdom.py
```

## Backend Implementation

### 1. Database Models

Create `src/models/wisdom.py`:

```python
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uuid import UUID, uuid4
from datetime import datetime

class Base(DeclarativeBase):
    __table_args__ = {"schema": "app"}

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

class WisdomEntry(Base, TimestampMixin):
    __tablename__ = "wisdom_entries"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    def __repr__(self):
        return f"WisdomEntry(id={self.id}, title={self.title[:50]}...)"
```

### 2. Database Configuration

Create `src/core/database.py`:

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.core.config import settings

engine = create_async_engine(
    settings.database_url,
    pool_size=10,
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    echo=settings.log_level == "debug",
)

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with async_session_factory() as session:
        yield session
```

### 3. Wisdom Service

Create `src/services/wisdom_service.py`:

```python
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.models.wisdom import WisdomEntry

class WisdomService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_todays_wisdom(self) -> WisdomEntry | None:
        """Get wisdom for current UTC date using deterministic rotation"""
        # Get total count of active wisdom entries
        count_result = await self.session.execute(
            select(func.count(WisdomEntry.id))
            .where(WisdomEntry.deleted_at.is_(None))
        )
        total_count = count_result.scalar()
        
        if total_count == 0:
            return None
        
        # Calculate deterministic index
        today = date.utcnow()
        epoch = date(1970, 1, 1)
        days_since_epoch = (today - epoch).days
        wisdom_index = days_since_epoch % total_count
        
        # Get wisdom at calculated index
        result = await self.session.execute(
            select(WisdomEntry)
            .where(WisdomEntry.deleted_at.is_(None))
            .order_by(WisdomEntry.id)
            .offset(wisdom_index)
            .limit(1)
        )
        
        return result.scalar_one_or_none()
    
    async def get_total_wisdom_count(self) -> int:
        """Get total count of active wisdom entries"""
        result = await self.session.execute(
            select(func.count(WisdomEntry.id))
            .where(WisdomEntry.deleted_at.is_(None))
        )
        return result.scalar()
```

### 4. API Endpoints

Create `src/api/endpoints/wisdom.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_session
from src.services.wisdom_service import WisdomService
from src.schemas.wisdom import WisdomResponse, ErrorResponse

router = APIRouter(prefix="/api/v1/wisdom", tags=["wisdom"])

@router.get("/today", response_model=WisdomResponse)
async def get_todays_wisdom(session: AsyncSession = Depends(get_session)):
    """Get wisdom content for current UTC date"""
    service = WisdomService(session)
    wisdom = await service.get_todays_wisdom()
    
    if wisdom is None:
        raise HTTPException(
            status_code=404,
            detail="No wisdom content is currently available"
        )
    
    return WisdomResponse(
        id=str(wisdom.id),
        title=wisdom.title,
        description=wisdom.description,
        date=wisdom.created_at.date().isoformat()
    )

@router.get("/health")
async def health_check(session: AsyncSession = Depends(get_session)):
    """Health check endpoint"""
    service = WisdomService(session)
    try:
        total_wisdom = await service.get_total_wisdom_count()
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "database": "connected",
            "total_wisdom": total_wisdom
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }
```

### 5. Pydantic Schemas

Create `src/schemas/wisdom.py`:

```python
from pydantic import BaseModel
from datetime import date
from typing import Optional

class WisdomResponse(BaseModel):
    id: str
    title: str
    description: str
    date: str
    
    class Config:
        from_attributes = True

class ErrorResponse(BaseModel):
    error: str
    message: str
    timestamp: str
    request_id: Optional[str] = None
    retry_after: Optional[int] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    database: str
    total_wisdom: Optional[int] = None
```

### 6. Main Application

Create `main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints import wisdom
from src.core.config import settings

app = FastAPI(
    title="Daily Wisdom API",
    version="1.0.0",
    description="API for daily wisdom display feature"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(wisdom.router)

@app.get("/")
async def root():
    return {"message": "Daily Wisdom API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Frontend Implementation

### 1. Wisdom Service

Create `src/services/wisdomService.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000/api/v1';

export const wisdomService = {
  async getTodaysWisdom() {
    const response = await fetch(`${API_BASE_URL}/wisdom/today`);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Failed to fetch wisdom');
    }
    
    return response.json();
  },
  
  async checkHealth() {
    const response = await fetch(`${API_BASE_URL}/wisdom/health`);
    return response.json();
  }
};
```

### 2. Custom Hook

Create `src/hooks/useWisdom.js`:

```javascript
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { wisdomService } from '../services/wisdomService';

export function useWisdom() {
  const queryClient = useQueryClient();
  
  const result = useQuery({
    queryKey: ['wisdom', 'today'],
    queryFn: wisdomService.getTodaysWisdom,
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 60 * 60 * 1000, // 1 hour
    retry: 3,
    retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000),
  });
  
  const refetch = () => {
    queryClient.invalidateQueries({ queryKey: ['wisdom', 'today'] });
  };
  
  return { ...result, refetch };
}
```

### 3. Wisdom Card Component

Create `src/components/WisdomCard/WisdomCard.jsx`:

```jsx
import React, { useState } from 'react';
import { useWisdom } from '../../hooks/useWisdom';
import './WisdomCard.css';

function WisdomCard() {
  const { data: wisdom, isLoading, error, refetch } = useWisdom();
  const [copySuccess, setCopySuccess] = useState(false);
  
  const handleCopy = async () => {
    if (!wisdom) return;
    
    try {
      await navigator.clipboard.writeText(`${wisdom.title}\n\n${wisdom.description}`);
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = `${wisdom.title}\n\n${wisdom.description}`;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    }
  };
  
  if (isLoading) {
    return (
      <div className="wisdom-card wisdom-card--loading">
        <div className="wisdom-card__skeleton">
          <div className="wisdom-card__skeleton-title"></div>
          <div className="wisdom-card__skeleton-description"></div>
          <div className="wisdom-card__skeleton-button"></div>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="wisdom-card wisdom-card--error">
        <div className="wisdom-card__error">
          <h3>Wisdom Unavailable</h3>
          <p>{error.message}</p>
          <button onClick={refetch} className="wisdom-card__retry-button">
            Try Again
          </button>
        </div>
      </div>
    );
  }
  
  if (!wisdom) {
    return (
      <div className="wisdom-card wisdom-card--empty">
        <div className="wisdom-card__empty">
          <h3>No Wisdom Today</h3>
          <p>Check back later for today's wisdom!</p>
        </div>
      </div>
    );
  }
  
  return (
    <div className="wisdom-card">
      <div className="wisdom-card__content">
        <h2 className="wisdom-card__title">{wisdom.title}</h2>
        <p className="wisdom-card__description">{wisdom.description}</p>
      </div>
      <div className="wisdom-card__actions">
        <button 
          onClick={handleCopy}
          className={`wisdom-card__copy-button ${copySuccess ? 'wisdom-card__copy-button--success' : ''}`}
        >
          {copySuccess ? 'Copied!' : 'Copy Wisdom'}
        </button>
      </div>
    </div>
  );
}

export default WisdomCard;
```

### 4. Wisdom Card Styles

Create `src/components/WisdomCard/WisdomCard.css`:

```css
.wisdom-card {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  color: white;
  position: relative;
  overflow: hidden;
}

.wisdom-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  z-index: 1;
}

.wisdom-card__content {
  position: relative;
  z-index: 2;
}

.wisdom-card__title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  line-height: 1.3;
}

.wisdom-card__description {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
  opacity: 0.95;
}

.wisdom-card__actions {
  position: relative;
  z-index: 2;
  text-align: center;
}

.wisdom-card__copy-button {
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.wisdom-card__copy-button:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.wisdom-card__copy-button--success {
  background: rgba(76, 175, 80, 0.3);
  border-color: rgba(76, 175, 80, 0.5);
}

/* Loading State */
.wisdom-card--loading {
  min-height: 300px;
}

.wisdom-card__skeleton {
  position: relative;
  z-index: 2;
}

.wisdom-card__skeleton-title,
.wisdom-card__skeleton-description,
.wisdom-card__skeleton-button {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  animation: pulse 1.5s ease-in-out infinite;
}

.wisdom-card__skeleton-title {
  height: 2rem;
  width: 80%;
  margin-bottom: 1rem;
}

.wisdom-card__skeleton-description {
  height: 4rem;
  width: 100%;
  margin-bottom: 2rem;
}

.wisdom-card__skeleton-button {
  height: 3rem;
  width: 120px;
  margin: 0 auto;
}

@keyframes pulse {
  0%, 100% { opacity: 0.1; }
  50% { opacity: 0.3; }
}

/* Error State */
.wisdom-card--error {
  background: linear-gradient(135deg, #f44336 0%, #e91e63 100%);
}

.wisdom-card__error {
  position: relative;
  z-index: 2;
  text-align: center;
}

.wisdom-card__retry-button {
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1rem;
}

/* Empty State */
.wisdom-card--empty {
  background: linear-gradient(135deg, #9e9e9e 0%, #757575 100%);
}

.wisdom-card__empty {
  position: relative;
  z-index: 2;
  text-align: center;
}

/* Responsive Design */
@media (max-width: 768px) {
  .wisdom-card {
    margin: 1rem;
    padding: 1.5rem;
  }
  
  .wisdom-card__title {
    font-size: 1.3rem;
  }
  
  .wisdom-card__description {
    font-size: 1rem;
  }
}
```

### 5. Landing Page Integration

Update `src/pages/LandingPage.jsx`:

```jsx
import React from 'react';
import WisdomCard from '../components/WisdomCard/WisdomCard';

function LandingPage() {
  return (
    <div className="landing-page">
      <header className="landing-page__header">
        <h1>Daily Wisdom</h1>
        <p>Your daily dose of inspiration</p>
      </header>
      
      <main className="landing-page__main">
        <WisdomCard />
      </main>
      
      <footer className="landing-page__footer">
        <p>© 2026 Daily Wisdom. Spreading inspiration daily.</p>
      </footer>
    </div>
  );
}

export default LandingPage;
```

## Running the Application

### 1. Start Backend

```bash
cd daily-wisdom-api

# Activate virtual environment
source venv/bin/activate

# Start FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# API will be available at http://localhost:8000
# Documentation at http://localhost:8000/docs
```

### 2. Start Frontend

```bash
cd daily-wisdom-ui

# Start React development server
npm start

# Application will be available at http://localhost:3000
```

### 3. Test API Endpoints

```bash
# Test health endpoint
curl http://localhost:8000/api/v1/wisdom/health

# Test today's wisdom endpoint
curl http://localhost:8000/api/v1/wisdom/today
```

## Testing

### Backend Tests

Create `tests/test_wisdom_api.py`:

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_todays_wisdom():
    response = client.get("/api/v1/wisdom/today")
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "description" in data
    assert "date" in data

def test_health_check():
    response = client.get("/api/v1/wisdom/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "total_wisdom" in data

def test_wisdom_not_found():
    # Mock empty database scenario
    # This test would require mocking the database service
    pass
```

Run tests:
```bash
cd daily-wisdom-api
pytest tests/ -v
```

### Frontend Tests

Create `src/components/WisdomCard/WisdomCard.test.jsx`:

```jsx
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import WisdomCard from './WisdomCard';

// Mock the wisdom service
jest.mock('../../services/wisdomService', () => ({
  wisdomService: {
    getTodaysWisdom: jest.fn(),
  },
}));

const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false },
  },
});

describe('WisdomCard', () => {
  it('displays loading state initially', () => {
    const queryClient = createTestQueryClient();
    
    render(
      <QueryClientProvider client={queryClient}>
        <WisdomCard />
      </QueryClientProvider>
    );
    
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });
  
  it('displays wisdom when loaded', async () => {
    const queryClient = createTestQueryClient();
    const mockWisdom = {
      id: '1',
      title: 'Test Wisdom',
      description: 'Test description',
      date: '2026-05-10',
    };
    
    jest.spyOn(require('../../services/wisdomService').wisdomService, 'getTodaysWisdom')
      .mockResolvedValue(mockWisdom);
    
    render(
      <QueryClientProvider client={queryClient}>
        <WisdomCard />
      </QueryClientProvider>
    );
    
    await waitFor(() => {
      expect(screen.getByText('Test Wisdom')).toBeInTheDocument();
      expect(screen.getByText('Test description')).toBeInTheDocument();
    });
  });
});
```

Run tests:
```bash
cd daily-wisdom-ui
npm test
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Verify PostgreSQL Docker container is running
   - Check connection string in `.env` file
   - Ensure database `daily_wisdom` exists

2. **Migration Errors**
   - Run `alembic current` to check migration status
   - Drop and recreate schema if needed
   - Check for syntax errors in migration files

3. **Frontend API Errors**
   - Verify backend server is running on port 8000
   - Check CORS settings in FastAPI app
   - Ensure API endpoints are correctly configured

4. **Wisdom Not Displaying**
   - Check database has wisdom entries
   - Verify UTC date calculation logic
   - Check browser console for JavaScript errors

### Debug Commands

```bash
# Check database connection
psql "postgresql://daily_wisdom_user:daily_wisdom_user@localhost:5432/daily_wisdom" -c "\dt app.*"

# Check Alembic status
alembic current
alembic history

# Test API directly
curl -v http://localhost:8000/api/v1/wisdom/today

# Check React app logs
npm start -- --verbose
```

## Next Steps

1. **Admin Interface**: Build admin panel for wisdom management
2. **Enhanced Styling**: Improve visual design and animations
3. **Performance Monitoring**: Add logging and metrics
4. **Deployment**: Set up production deployment pipeline
5. **Additional Features**: User preferences, wisdom sharing, etc.

This quick start guide provides everything needed to get the daily wisdom feature running locally. The implementation follows the project constitution and best practices for both React and FastAPI development.
