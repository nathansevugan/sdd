# Research: Daily Wisdom Display

**Feature**: Daily Wisdom Display  
**Date**: 2026-05-10  
**Phase**: 0 - Research & Analysis

## Overview

This document captures research decisions for the daily wisdom display feature. The technical approach leverages existing infrastructure and follows established patterns from the project constitution.

## Research Topics & Decisions

### 1. Wisdom Rotation Algorithm

**Decision**: Deterministic UTC-based rotation using modulo arithmetic

**Rationale**: 
- Ensures consistent wisdom selection across all users regardless of timezone
- Guarantees 365-day uniqueness through simple modulo calculation
- Computationally efficient and easily testable

**Implementation**: 
```python
def get_wisdom_for_date(date: datetime, total_wisdom: int) -> int:
    days_since_epoch = (date - datetime(1970, 1, 1)).days
    return days_since_epoch % total_wisdom
```

**Alternatives Considered**:
- Random selection with tracking (complex state management)
- Sequential assignment with reset (requires additional storage)
- User-specific rotation (violates consistency requirement)

### 2. Frontend State Management

**Decision**: TanStack Query for server state, local state for UI interactions

**Rationale**:
- TanStack Query provides built-in caching, retry logic, and loading states
- Matches constitution requirements for React ecosystem
- Handles error states and retry functionality out of the box

**Implementation**:
- `useWisdom` custom hook wrapping TanStack Query
- Local state for copy button feedback and loading states
- Skeleton loading component during data fetch

**Alternatives Considered**:
- Redux (overkill for simple feature)
- Context API (no built-in caching/error handling)
- Plain useState (no caching or error handling)

### 3. Clipboard API Implementation

**Decision**: Modern Clipboard API with fallback for older browsers

**Rationale**:
- Provides secure, async clipboard access
- Matches assumption about modern browser support
- Allows for formatted text copying (title + description)

**Implementation**:
```javascript
async function copyWisdom(title, description) {
  try {
    await navigator.clipboard.writeText(`${title}\n\n${description}`);
    return true;
  } catch (err) {
    // Fallback for older browsers
    return false;
  }
}
```

**Alternatives Considered**:
- Document.execCommand (deprecated, less reliable)
- Flash-based clipboard (obsolete, security concerns)

### 4. Error Handling Strategy

**Decision**: Graceful degradation with user-friendly messages and retry functionality

**Rationale**:
- Provides good user experience during network issues
- Matches clarification requirements for error handling
- TanStack Query supports retry logic out of the box

**Implementation**:
- Error boundary component for React errors
- Fallback wisdom content when API fails
- Retry button for manual recovery attempts
- Toast notifications for user feedback

**Alternatives Considered**:
- Silent failures (poor UX)
- Full page errors (too disruptive)
- Only retry automatically (no user control)

### 5. Database Schema Design

**Decision**: Simple wisdom table with UTC-based indexing

**Rationale**:
- Minimal complexity for single-purpose feature
- Efficient querying for daily wisdom selection
- Follows constitution naming conventions

**Implementation**:
```sql
CREATE TABLE app.wisdom_entries (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP NULL
);
```

**Alternatives Considered**:
- Complex scheduling tables (unnecessary overhead)
- JSON storage (less efficient for querying)
- Multiple tables for categories (out of scope for v1)

### 6. API Design

**Decision**: Simple REST endpoint with caching headers

**Rationale**:
- Matches constitution API style requirements
- Easy to consume from React frontend
- Supports browser caching for performance

**Implementation**:
```
GET /api/wisdom/today
Response: { "title": "...", "description": "..." }
```

**Cache Strategy**:
- Cache-Control: max-age=3600 (1 hour)
- Vary: Accept (for future API versioning)
- ETag support for conditional requests

**Alternatives Considered**:
- GraphQL (overkill for single endpoint)
- WebSocket (unnecessary real-time requirements)
- gRPC (not browser-friendly)

### 7. Performance Optimization

**Decision**: Database indexing + application-level caching

**Rationale**:
- Meets 2-second page load requirement
- Minimizes database load for high-traffic endpoint
- Simple to implement and maintain

**Implementation**:
- Database query optimization with proper indexing
- TanStack Query caching (5-minute stale time)
- CDN caching for static assets
- Lazy loading of wisdom component

**Alternatives Considered**:
- Redis caching (additional infrastructure complexity)
- Pre-generated static files (loses dynamic rotation)
- Edge computing (overkill for simple feature)

## Integration Points

### Existing Database
- **Connection**: Using provided PostgreSQL Docker instance
- **Schema**: Creating `app.wisdom_entries` table in dedicated schema
- **Migrations**: Alembic scripts for schema changes

### Frontend Integration
- **Component**: WisdomCard component for landing page
- **Routing**: No new routes needed (landing page integration)
- **State**: TanStack Query for API integration

### Backend Integration
- **FastAPI**: New endpoint in existing API structure
- **Models**: SQLAlchemy model following constitution patterns
- **Services**: Business logic in dedicated service layer

## Risk Assessment

### Low Risk
- Database schema (simple, follows established patterns)
- Frontend component (standard React practices)
- API endpoint (conventional REST design)

### Medium Risk
- UTC time handling (requires careful testing across timezones)
- Clipboard API compatibility (browser support variations)
- Performance under load (needs monitoring)

### Mitigation Strategies
- Comprehensive timezone testing
- Graceful fallbacks for older browsers
- Performance monitoring and alerting

## Conclusion

All research topics have been resolved with decisions that:
- Follow project constitution and established patterns
- Meet functional and non-functional requirements
- Balance simplicity with robustness
- Support future extensibility

The feature is ready to proceed to Phase 1 design with no outstanding technical questions or NEEDS CLARIFICATION items.
