# ==============================================================================
# Dockerfile for Review System CI/CD Project
# Multi-version container packaging for V1, V2, and V3
# ==============================================================================

# Base image: Official lightweight Python 3.11 Slim Linux distribution
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Optimize layer caching: copy requirements and install dependencies first
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Build-time argument to inject target version (v1, v2, v3)
ARG APP_VERSION=v1
ENV APP_VERSION=${APP_VERSION}
ENV PORT=5000
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy application code, HTML templates, and static CSS
COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/

# Expose internal Flask port
EXPOSE 5000

# Container entrypoint
# Production Note for Assignment Review:
# In this college demonstration, we execute 'python app.py' directly.
# This runs Flask's built-in server with single-process synchronous request handling,
# which is ideal for classroom demos, lightweight memory footprints, and debugging.
# In enterprise production environments, an asynchronous WSGI server such as Gunicorn
# or uWSGI with multiple worker processes should be deployed behind an Nginx reverse proxy.
CMD ["python", "app.py"]
