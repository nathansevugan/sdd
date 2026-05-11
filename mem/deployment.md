# deployment.md

## Containerization

-   Entire solution must be dockerized
-   Provide Dockerfile for backend service
-   Use lightweight base image (python:3.x-slim)

## Environment Variables

-   Pass all environment variables via docker runtime
-   Do not hardcode secrets
-   Support .env for local development

## Execution Script

-   Provide shell script: run.sh

### run.sh

``` bash
#!/bin/bash

docker build -t app-backend .
docker run --env-file .env -p 8000:8000 app-backend
```

## Dockerfile (example)

``` dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
