# API Contracts: Daily Wisdom Display

**Feature**: Daily Wisdom Display  
**Date**: 2026-05-10  
**Phase**: 1 - Design & Contracts

## Overview

RESTful API contracts for the daily wisdom feature, following FastAPI and OpenAPI standards. All endpoints return JSON responses with standard HTTP status codes.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

**Current Scope**: Public endpoints (no authentication required)  
**Future Scope**: Admin endpoints will require JWT authentication

## Endpoints

### GET /wisdom/today

Get the wisdom content for the current UTC date.

#### Request

```http
GET /api/v1/wisdom/today
```

**Headers**:
```
Accept: application/json
```

**Query Parameters**: None

#### Response

**Success (200 OK)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "The only way to do great work is to love what you do.",
  "description": "Passion is the key to excellence and fulfillment in your work.",
  "date": "2026-05-10"
}
```

**Error Responses**:

*404 Not Found* (No wisdom available):
```json
{
  "error": "WISDOM_NOT_FOUND",
  "message": "No wisdom content is currently available",
  "timestamp": "2026-05-10T12:00:00Z",
  "retry_after": 300
}
```

*500 Internal Server Error*:
```json
{
  "error": "INTERNAL_ERROR",
  "message": "An unexpected error occurred",
  "timestamp": "2026-05-10T12:00:00Z",
  "request_id": "req_123456789"
}
```

#### Response Headers

```
Cache-Control: public, max-age=3600
ETag: "abc123"
X-Request-ID: req_123456789
```

### GET /wisdom/health

Health check endpoint for the wisdom service.

#### Request

```http
GET /api/v1/wisdom/health
```

#### Response

**Success (200 OK)**:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-10T12:00:00Z",
  "version": "1.0.0",
  "database": "connected",
  "total_wisdom": 42
}
```

**Error (503 Service Unavailable)**:
```json
{
  "status": "unhealthy",
  "timestamp": "2026-05-10T12:00:00Z",
  "error": "Database connection failed"
}
```

## Admin Endpoints (Future)

These endpoints will require JWT authentication and are planned for the admin interface.

### POST /wisdom

Create a new wisdom entry.

#### Request

```http
POST /api/v1/wisdom
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Body**:
```json
{
  "title": "Your wisdom title here",
  "description": "Your wisdom description here"
}
```

#### Response

**Success (201 Created)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Your wisdom title here",
  "description": "Your wisdom description here",
  "created_at": "2026-05-10T12:00:00Z"
}
```

### PUT /wisdom/{id}

Update an existing wisdom entry.

#### Request

```http
PUT /api/v1/wisdom/550e8400-e29b-41d4-a716-446655440000
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Body**:
```json
{
  "title": "Updated wisdom title",
  "description": "Updated wisdom description"
}
```

#### Response

**Success (200 OK)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated wisdom title",
  "description": "Updated wisdom description",
  "updated_at": "2026-05-10T12:00:00Z"
}
```

### DELETE /wisdom/{id}

Soft delete a wisdom entry.

#### Request

```http
DELETE /api/v1/wisdom/550e8400-e29b-41d4-a716-446655440000
Authorization: Bearer <jwt_token>
```

#### Response

**Success (204 No Content)**: No response body

## Data Models

### WisdomResponse

```json
{
  "id": "string (UUID)",
  "title": "string (max 255 chars)",
  "description": "string",
  "date": "string (ISO 8601 date)"
}
```

### ErrorResponse

```json
{
  "error": "string (error code)",
  "message": "string (human readable)",
  "timestamp": "string (ISO 8601 datetime)",
  "request_id": "string (optional)",
  "retry_after": "number (seconds, optional)"
}
```

### HealthResponse

```json
{
  "status": "string (healthy|unhealthy)",
  "timestamp": "string (ISO 8601 datetime)",
  "version": "string (semantic version)",
  "database": "string (connected|disconnected)",
  "total_wisdom": "number (optional)"
}
```

### CreateWisdomRequest

```json
{
  "title": "string (max 255 chars, required)",
  "description": "string (required)"
}
```

### UpdateWisdomRequest

```json
{
  "title": "string (max 255 chars, required)",
  "description": "string (required)"
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `WISDOM_NOT_FOUND` | 404 | No wisdom content available for current date |
| `INTERNAL_ERROR` | 500 | Unexpected server error |
| `VALIDATION_ERROR` | 400 | Request validation failed |
| `UNAUTHORIZED` | 401 | Authentication required/invalid |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `RATE_LIMITED` | 429 | Too many requests |

## Rate Limiting

**Public Endpoints**: 100 requests per minute per IP  
**Admin Endpoints**: 1000 requests per minute per authenticated user

**Headers**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1642694400
```

## Caching Strategy

### Client-Side Caching

**GET /wisdom/today**:
- `Cache-Control: public, max-age=3600` (1 hour)
- `ETag` header for conditional requests
- `Last-Modified` header for browser caching

### Server-Side Caching

- **Application Cache**: 5 minutes for total wisdom count
- **Database Query Cache**: 1 hour for today's wisdom
- **CDN Cache**: 1 hour for API responses

## OpenAPI Specification

```yaml
openapi: 3.0.0
info:
  title: Daily Wisdom API
  version: 1.0.0
  description: API for daily wisdom display feature

paths:
  /api/v1/wisdom/today:
    get:
      summary: Get today's wisdom
      tags: [Wisdom]
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WisdomResponse'
        '404':
          description: Wisdom not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '500':
          description: Internal server error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

components:
  schemas:
    WisdomResponse:
      type: object
      required: [id, title, description, date]
      properties:
        id:
          type: string
          format: uuid
        title:
          type: string
          maxLength: 255
        description:
          type: string
        date:
          type: string
          format: date

    ErrorResponse:
      type: object
      required: [error, message, timestamp]
      properties:
        error:
          type: string
        message:
          type: string
        timestamp:
          type: string
          format: date-time
        request_id:
          type: string
        retry_after:
          type: number
```

## Integration Examples

### JavaScript/Fetch

```javascript
async function getTodaysWisdom() {
  try {
    const response = await fetch('/api/v1/wisdom/today');
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message);
    }
    
    const wisdom = await response.json();
    return wisdom;
  } catch (error) {
    console.error('Failed to fetch wisdom:', error);
    throw error;
  }
}
```

### Python/Requests

```python
import requests

def get_todays_wisdom():
    response = requests.get('http://localhost:8000/api/v1/wisdom/today')
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
```

### React/TanStack Query

```javascript
import { useQuery } from '@tanstack/react-query';

function useWisdom() {
  return useQuery({
    queryKey: ['wisdom', 'today'],
    queryFn: async () => {
      const response = await fetch('/api/v1/wisdom/today');
      if (!response.ok) throw new Error('Failed to fetch wisdom');
      return response.json();
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 60 * 60 * 1000, // 1 hour
  });
}
```

## Testing

### Unit Tests

- Test endpoint responses with mock data
- Test error handling scenarios
- Test validation logic

### Integration Tests

- Test full request/response cycle
- Test database integration
- Test caching behavior

### Contract Tests

- Test OpenAPI specification compliance
- Test backward compatibility
- Test error format consistency

## Versioning

**Current Version**: v1  
**Versioning Strategy**: Semantic versioning in URL path  
**Backward Compatibility**: Maintain v1 endpoints when adding v2

**Deprecation Policy**:
- Announce deprecation 6 months in advance
- Provide migration guide
- Support old version for 12 months after deprecation

## Security Considerations

### Input Validation

- All inputs validated using Pydantic models
- SQL injection prevention via ORM
- XSS prevention via output encoding

### Rate Limiting

- IP-based rate limiting for public endpoints
- User-based rate limiting for authenticated endpoints
- Distributed rate limiting for scalability

### Monitoring

- Log all API requests with request IDs
- Monitor error rates and response times
- Alert on unusual activity patterns

## Conclusion

The API contracts provide:

- **Clear interface** for frontend integration
- **Comprehensive error handling** for robust client experience
- **Performance optimization** through caching strategies
- **Security considerations** for production deployment
- **Extensibility** for future admin functionality

The contracts follow REST principles and FastAPI best practices while maintaining simplicity for the current feature scope.
