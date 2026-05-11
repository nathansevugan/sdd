from fastapi import HTTPException, status

class WisdomNotFoundError(HTTPException):
    def __init__(self, detail: str = "No wisdom content is currently available"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class DatabaseConnectionError(HTTPException):
    def __init__(self, detail: str = "Database connection failed"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail
        )
