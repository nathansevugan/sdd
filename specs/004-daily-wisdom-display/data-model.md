# Data Model: Daily Wisdom Display

**Feature**: Daily Wisdom Display  
**Date**: 2026-05-10  
**Phase**: 1 - Design & Contracts

## Entity Overview

The daily wisdom feature requires a single primary entity for storing wisdom content, with supporting logic for daily rotation and scheduling.

## Core Entities

### Wisdom Entry

**Purpose**: Stores individual wisdom content with title and description  
**Table**: `app.wisdom_entries`  
**Lifecycle**: Created once, rarely updated, soft deleted only

#### Attributes

| Name | Type | Constraints | Description |
|------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique identifier |
| `title` | VARCHAR(255) | NOT NULL, LENGTH 255 | Wisdom title (max 255 chars) |
| `description` | TEXT | NOT NULL | Wisdom description (unlimited length) |
| `created_at` | TIMESTAMP | DEFAULT NOW(), NOT NULL | Creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT NOW(), NOT NULL | Last update timestamp |
| `deleted_at` | TIMESTAMP | NULLABLE | Soft delete timestamp |

#### Validation Rules

- `title`: Required, max 255 characters, cannot be empty string
- `description`: Required, cannot be empty string
- Soft deletes enforced via `deleted_at IS NULL` in all queries

#### Relationships

- No foreign key relationships (standalone entity)
- One-to-many with daily schedule (logical, not physical)

## Derived Entities (Logical)

### Daily Wisdom Schedule

**Purpose**: Tracks which wisdom is assigned to each UTC date  
**Implementation**: Computed at runtime using deterministic algorithm  
**Storage**: No physical table needed

#### Algorithm

```python
def get_wisdom_for_date(target_date: datetime, total_wisdom: int) -> int:
    """Deterministic wisdom selection based on UTC date"""
    epoch = datetime(1970, 1, 1)
    days_since_epoch = (target_date - epoch).days
    return days_since_epoch % total_wisdom
```

#### Attributes (Computed)

| Name | Type | Source | Description |
|------|------|--------|-------------|
| `date` | DATE | UTC current date | Calendar date for wisdom |
| `wisdom_id` | UUID | Computed via algorithm | Selected wisdom entry ID |
| `sequence` | INTEGER | Computed modulo | Position in rotation cycle |

## Data Access Patterns

### Primary Queries

1. **Get Today's Wisdom** (Most frequent)
   ```sql
   SELECT id, title, description 
   FROM app.wisdom_entries 
   WHERE deleted_at IS NULL 
   ORDER BY id 
   LIMIT 1 OFFSET $computed_index;
   ```

2. **Get Total Wisdom Count** (For rotation)
   ```sql
   SELECT COUNT(*) 
   FROM app.wisdom_entries 
   WHERE deleted_at IS NULL;
   ```

3. **Get Wisdom by ID** (Admin interface)
   ```sql
   SELECT id, title, description, created_at, updated_at
   FROM app.wisdom_entries 
   WHERE id = $uuid AND deleted_at IS NULL;
   ```

### Write Operations

1. **Create Wisdom** (Admin interface)
   ```sql
   INSERT INTO app.wisdom_entries (title, description) 
   VALUES ($title, $description);
   ```

2. **Update Wisdom** (Admin interface)
   ```sql
   UPDATE app.wisdom_entries 
   SET title = $title, description = $description, updated_at = NOW()
   WHERE id = $uuid AND deleted_at IS NULL;
   ```

3. **Soft Delete Wisdom** (Admin interface)
   ```sql
   UPDATE app.wisdom_entries 
   SET deleted_at = NOW() 
   WHERE id = $uuid AND deleted_at IS NULL;
   ```

## Database Schema

### Table Definition

```sql
CREATE TABLE app.wisdom_entries (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW() NOT NULL,
    deleted_at TIMESTAMP NULL
);

-- Indexes for performance
CREATE INDEX idx_wisdom_entries_deleted_at ON app.wisdom_entries(deleted_at) WHERE deleted_at IS NULL;
CREATE INDEX idx_wisdom_entries_id ON app.wisdom_entries(id) WHERE deleted_at IS NULL;
```

### Constraints

```sql
-- Ensure title is not empty
ALTER TABLE app.wisdom_entries 
ADD CONSTRAINT chk_wisdom_entries_title_not_empty 
CHECK (length(trim(title)) > 0);

-- Ensure description is not empty  
ALTER TABLE app.wisdom_entries 
ADD CONSTRAINT chk_wisdom_entries_description_not_empty 
CHECK (length(trim(description)) > 0);
```

## SQLAlchemy Models

### Python Model Definition

```python
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uuid import UUID
from datetime import datetime

class Base(DeclarativeBase):
    __table_args__ = {"schema": "app"}

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

class WisdomEntry(Base, TimestampMixin):
    __tablename__ = "wisdom_entries"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    def __repr__(self):
        return f"WisdomEntry(id={self.id}, title={self.title[:50]}...)"
```

## State Transitions

### Wisdom Entry Lifecycle

```
[Created] → [Active] → [Updated] → [Active] → [Deleted] → [Archived]
     ↑           ↓           ↑           ↓           ↓
   (only)    (read/write) (only)    (read/write) (read-only)
```

**States**:
- **Created**: Entry exists but not yet visible (created_at set)
- **Active**: Entry is visible for daily rotation (deleted_at IS NULL)
- **Updated**: Entry modified but still active (updated_at changed)
- **Deleted**: Entry soft deleted (deleted_at set)
- **Archived**: Entry permanently deleted (future cleanup)

**Transitions**:
- Create → Active: Automatic on successful INSERT
- Active → Updated: Via UPDATE operations
- Active → Deleted: Via soft delete (set deleted_at)
- Deleted → Active: Via restore (set deleted_at = NULL)

## Data Integrity

### Business Rules

1. **Uniqueness**: No two active entries should have identical title+description
2. **Rotation**: Each wisdom appears at most once per 365-day period
3. **Availability**: At least one active wisdom entry must exist
4. **Content Quality**: Title and description must contain meaningful content

### Enforcement

```sql
-- Prevent duplicate wisdom content
CREATE UNIQUE INDEX uq_wisdom_entries_content 
ON app.wisdom_entries(title, description) 
WHERE deleted_at IS NULL;

-- Ensure at least one wisdom exists (application-level check)
-- This is enforced in the service layer, not database constraints
```

## Performance Considerations

### Query Optimization

1. **Today's Wisdom Query**: Uses OFFSET with computed index - O(1) complexity
2. **Count Query**: Uses filtered index on deleted_at - O(log n) complexity  
3. **ID Lookup**: Uses primary key index - O(1) complexity

### Caching Strategy

- **Application Level**: Cache total wisdom count (5 minutes)
- **Database Level**: Query result caching for today's wisdom (1 hour)
- **Browser Level**: HTTP cache headers for API responses

### Scaling Factors

- **Read Load**: High (every page load)
- **Write Load**: Low (admin operations only)
- **Storage**: Minimal (text content only)
- **Memory**: Low (small dataset, simple queries)

## Migration Strategy

### Initial Setup

```python
# Alembic migration
def upgrade():
    # Create schema if not exists
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
```

### Data Seeding

```python
# Initial wisdom content (admin interface or migration)
def seed_wisdom():
    wisdom_data = [
        ("The only way to do great work is to love what you do.", "Steve Jobs"),
        ("Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
        # ... more wisdom entries
    ]
    
    for title, description in wisdom_data:
        session.add(WisdomEntry(title=title, description=description))
```

## Conclusion

The data model provides a simple, robust foundation for the daily wisdom feature:

- **Single entity** design minimizes complexity
- **Soft delete** pattern preserves data integrity
- **Deterministic rotation** ensures consistent behavior
- **Performance optimized** for high-read, low-write patterns
- **Constitution compliant** with established patterns

The model supports all functional requirements while maintaining simplicity and performance.
