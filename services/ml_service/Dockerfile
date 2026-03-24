FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc g++ \
    && rm -rf /var/lib/apt/lists/*

COPY services/ml_service/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY services/shared /app/shared
COPY services/ml_service /app/ml_service

ENV PYTHONPATH=/app/ml_service:/app

EXPOSE 8001

CMD ["python", "-m", "ml_service.app"]
