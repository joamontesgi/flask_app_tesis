FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    tcpdump sudo \
    && rm -rf /var/lib/apt/lists/*

COPY services/capture_service/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && pip install --no-cache-dir cicflowmeter==0.1.6 || true

COPY services/capture_service /app/capture_pkg

ENV PYTHONPATH=/app/capture_pkg

EXPOSE 8002

CMD ["python", "-m", "capture_service.app"]
