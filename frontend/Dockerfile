FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && addgroup -S app \
    && adduser -S -G app app

COPY app.py openapi.yaml swagger.html ./
USER app

EXPOSE 5000
CMD ["python", "app.py"]
