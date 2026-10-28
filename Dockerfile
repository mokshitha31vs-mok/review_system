FROM python:3.11-slim
WORKDIR /app
ARG APP_VERSION=v1
ENV APP_VERSION=${APP_VERSION}
ENV PORT=5000
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
